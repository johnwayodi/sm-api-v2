from flask import request
from flask_expects_json import expects_json
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from storemanager.api.v2.database.queries import *
from storemanager.api.v2.models.category import CategoryModel
from storemanager.api.v2.models.schemas import CATEGORY_SCHEMA
from storemanager.api.v2.models.user import UserModel


class Category(Resource):
    """Allows crud on single category object"""

    @jwt_required
    def get(self, category_id):
        """
       Retrieve a Single Category item
       ---
       parameters:
         - in: path
           name: category_id
           type: string
           required: true
       responses:
         200:
           description: Displayed when user deleted successfully
         404:
           description: Displayed when no user is found with specified id
         403:
           description: Error shown to Attendant trying to delete product
            """

        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] == "admin":
            if category_id.isdigit():
                result = CategoryModel.get_by_id(GET_CATEGORY, (category_id,))
                if result is None:
                    return {'message': 'category with id does not exist'}, 404
                else:
                    category = CategoryModel()
                    category.id = result[0]
                    category.name = result[1]
                    category.description = result[2]
                return {'message': 'category details',
                        'category': category.as_dict()}, 200

            return {'message': 'provided id is not an integer'}, 400
        return {'message': 'only an admin can view categories'}

    @jwt_required
    def put(self, category_id):
        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] == "admin":
            if category_id.isdigit():
                data = request.get_json()
                name = data.get('name')
                description = data.get('description')
                result = CategoryModel.get_by_id(GET_CATEGORY, (category_id,))
                if result is None:
                    return {'message': 'category with id does not exist'}, 404

                category = CategoryModel()
                category.id = result[0]
                category.update(
                    UPDATE_CATEGORY, (name, description, category.id))
                return {'message': 'category updated successfully'}, 200

            return {'message': 'provided id is not an integer'}, 400
        return {'message': 'only an admin can update a category'}

    @jwt_required
    def delete(self, category_id):
        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] == "admin":
            if category_id.isdigit():
                result = CategoryModel.get_by_id(GET_CATEGORY, (category_id,))
                if result is None:
                    return {'message': 'category with id does not exist'}, 404

                category = CategoryModel()
                category.id = result[0]
                category.delete(DELETE_CATEGORY, (category_id,))
                return {'message': 'category deleted successfully'}, 200

            return {'message': 'provided id is not an integer'}, 400
        return {'message': 'only an admin can delete a product'}


class Categories(Resource):
    """Allows crud on categories"""

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] == "admin":
            categories = {}
            result = CategoryModel.get_all(GET_ALL_CATEGORIES)

            for i in range(len(result)):
                category = CategoryModel()
                category.id = result[i][0]
                category.name = result[i][1]
                category.description = result[i][2]
                categories[i + 1] = category.as_dict()
            if categories == {}:
                return {'message': 'no categories added yet'}
            return {'categories': categories}, 200
        return {'message': 'only an admin can view categories'}

    @jwt_required
    @expects_json(CATEGORY_SCHEMA)
    def post(self):
        current_user = get_jwt_identity()
        user_details = UserModel.get_by_name(GET_USER_BY_NAME, (current_user,))
        if user_details[3] == "admin":
            data = request.get_json()
            name = data.get('name')
            description = data.get('description')
            if name.isdigit():
                return {'message': 'name cannot be an integer value'}, 400
            if description.isdigit():
                return {'message': 'description cannot be an integer value'}, 400

            category = CategoryModel()
            result = category.save(CREATE_CATEGORY, (name, description))

            category.id = result[0]
            category.name = result[1]
            category.description = result[2]
            return {'message': 'category created',
                    'category': category.as_dict()}, 201
        return {'message': 'only an admin can add a category'}