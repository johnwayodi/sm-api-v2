from flask import request, abort
from flask_expects_json import expects_json
from flask_jwt_extended import jwt_required, create_access_token, get_raw_jwt
from flask_restful import Resource
from flasgger import swag_from

from storemanager.api.v2.utils.validators import CustomValidator
from storemanager.api.v2.utils.custom_checks import *
from storemanager.api.v2.database.database import execute_query


USER_SCHEMA = {
    'type': 'object',
    'maxProperties': 2,
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['username', 'password']
}


class User(Resource):
    """Allows requests on single user"""

    @jwt_required
    @swag_from('docs/user_get.yml')
    def get(self, user_id):
        """get single user"""
        check_user_admin()
        check_id_integer(user_id)
        user_details = UserModel.get_by_id(GET_USER, (user_id,))
        if user_details is None:
            return {'message': 'user with id does not exist'}, 404

        user = UserModel()
        user.id = user_details[0]
        user.username = user_details[1]
        user.role = user_details[2]
        return {'user': user.as_dict()}, 200

    @jwt_required
    @swag_from('docs/user_delete.yml')
    def delete(self, user_id):
        """delete a user"""
        check_user_admin()
        check_id_integer(user_id)
        result = UserModel.get_by_id(GET_USER, (user_id,))
        if result is not None:
            user = UserModel()
            user.delete(DELETE_USER, (user_id,))
            return {'message': 'user deleted successfully'}, 200

        return {'message': 'user with id does not exist'}, 404


class UserList(Resource):
    """Allow requests on users"""

    @jwt_required
    @swag_from('docs/user_get_all.yml')
    def get(self):
        """get all users"""
        check_user_admin()
        users = []
        result = UserModel.get_all(GET_ALL_USERS)

        for i in range(len(result)):
            user = UserModel()
            user.id = result[i][0]
            user.username = result[i][1]
            user.role = result[i][2]
            users.append(user.as_dict())
        if not users:
            return {'message': 'no users in system yet'}, 404

        return {'users': users}, 200

    @expects_json(USER_SCHEMA)
    @jwt_required
    @swag_from('docs/user_post.yml')
    def post(self):
        """add new user"""
        check_user_admin()
        data = request.get_json()
        username = data['username']
        password = data['password']
        CustomValidator.validate_login_details(username, password)
        a_name = username.lower().strip()

        result = UserModel.get_by_name(GET_USER_BY_NAME, (a_name,))
        if result is None:
            user = UserModel()
            user.username = a_name
            user.password = password
            user.role = "attendant"
            user.save(CREATE_USER, (user.username, user.password, user.role))
            return {'message': 'attendant created successfully'}, 201

        abort(400, 'attendant with similar name exists')


class UserRegistration(Resource):
    """Allows registration of users"""

    @expects_json(USER_SCHEMA)
    @swag_from('docs/auth_register.yml')
    def post(self):
        """register a user"""
        check_admin_exists()
        data = request.get_json()
        username = data['username']
        password = data['password']
        role = "admin"

        u_name = username.lower().strip()
        CustomValidator.validate_register_details(u_name, password, role)

        user_result = UserModel.get_by_name(GET_USER_BY_NAME, (u_name,))
        if user_result is not None:
            return {'message': 'User already exists'}, 400

        user = UserModel()
        saved_user = user.save(CREATE_USER, (u_name, password, role))
        user.id = saved_user[0]
        user.username = saved_user[1]
        user.role = saved_user[2]
        return {'message': 'user created',
                'user': user.as_dict()}, 201


class UserLogin(Resource):
    """Allows user who is registered to log in"""

    @expects_json(USER_SCHEMA)
    @swag_from('docs/auth_login.yml')
    def post(self):
        """login a user"""

        data = request.get_json()
        username = data['username']
        password = data['password']

        uname = username.lower().strip()

        CustomValidator.validate_login_details(uname, password)

        user_result = UserModel.get_by_name(GET_USER_BY_NAME, (uname,))
        if user_result is None:
            return {'message': 'user does not exist'}, 404

        if user_result[1] == uname and user_result[2] == password:
            access_token = create_access_token(identity=uname, expires_delta=False)
            return {'message': 'login successful',
                    'user_role': user_result[3],
                    'access_token': access_token}, 200

        if user_result[1] == uname and user_result[2] != password:
            return {'message': 'wrong username or password, '
                               'Try Again'}, 400


class UserLogout(Resource):
    """Allows user to log out of application"""

    @jwt_required
    @swag_from('docs/auth_logout.yml')
    def delete(self):
        """logout a user"""
        token = get_raw_jwt()['jti']
        execute_query([REVOKE_TOKEN, (token,)], "one")
        return {"message": "logout successful"}, 200
