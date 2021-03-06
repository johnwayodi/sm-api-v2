# Store Manager API

[![Coverage Status](https://coveralls.io/repos/github/johnwayodi/sm-api-v2/badge.svg?branch=develop)](https://coveralls.io/github/johnwayodi/sm-api-v2?branch=develop)
[![Build Status](https://travis-ci.org/johnwayodi/sm-api-v2.svg?branch=develop)](https://travis-ci.org/johnwayodi/sm-api-v2)
[![Maintainability](https://api.codeclimate.com/v1/badges/c23849e92db44dd7a9b2/maintainability)](https://codeclimate.com/github/johnwayodi/sm-api-v2/maintainability)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/johnwayodi/sm-api-v2/issues)

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/faa1bb2518cd81a3e91d)

Store Manager is a web application for use in a single store. There are two users: Administrator and Attendant.

The Administrator is the Store Owner and can add Store Attendants to the application. The Store Owner can also add, 
modify and delete products. The Store Owner will also be able to view all Sale Records created by the different Store Attendants.

The Store Attendant will be able to sell products and create Sale Records. The Attendant will also be able to view 
all his/her sale individual sale records.

The Front-End design of the application can be viewed here: [Store Manager UI](https://johnwayodi.github.io/store-manager/)

The API is hosted on heroku and can be found here: [Store Manager API](https://jw-store-manager-apiv2.herokuapp.com/apidocs/)
## Testing and Usage
To test the application locally, first configure the environment as follows:

1. Install [PostgreSQL](https://www.postgresql.org/) if not already installed and ensure it is up and running.
2. Ensure [Python3](https://www.python.org/) is installed
3. Create a folder on your computer, once in the newly created repository, clone the project by 
running the following command:
    
    `git clone https://github.com/johnwayodi/sm-api-v2.git`
3. Install [virtualenv](https://virtualenv.pypa.io/en/latest/) which will aid in the creation of a vitual environment.
Once virtual environment is installed, create a new virtual environment named *venv*
    
    `virtualenv venv`
4. Activate the created virtual environment and install all the packages for use in the app,
   
   The packages used by the flask app are contained in a `requirements.txt` file: 
    
    `source venv/bin/activate` 
    
    `pip install -r requirements.txt` 
6. Set up the environment variables, 
    
        export JWT_SECRET_KEY="your jwt secret key"
        export API_SECRET_KEY="your secret key"
        export DATABASE_NAME="name of database"
        export DATABASE_HOST="database host"
        export DATABASE_USER="database username"
        export DATABASE_PASS="database password"
        export FLASK_APP=run.py

7. After all is set, run the application, export the application and pass the following command:
        
        flask run
## Endpoints
The API exposes the following endpoints:
1. #### Auth Endpoints
    The `/auth` endpoint allow the registration of users and a login route to allow registered.
    users to log into the application
    
    The users can also logout of the application, doing so will revoke their access token and to access the 
    the protected endpoinnts they'll have to login again. 
    <table style="width:100%">
      <tr>
        <td>POST</td>
        <td>/auth/register</td>
        <td>Register new user, first user to register will automatically be the Admin</td>
      </tr>
      <tr>
        <td>POST</td>
        <td>/auth/login</td>
        <td>Users can login to the system</td>
      </tr>
      <tr>
        <td>DELETE</td>
        <td>/auth/logout</td>
        <td>Users can logout of the system</td>
      </tr>
    </table>

2. #### User Endpoints
    The `/api/v2/users` endpoint allows the management of attendants by the admin, the admin can add, update or remove an attendant accounts 
    <table style="width:100%">
      <tr>
        <td>POST</td>
        <td>/users</td>
        <td>Create a new attendant, only accessible to admin</td>
      </tr>
      <tr>
        <td>PUT</td>
        <td>/users/{user_id}</td>
        <td>Update details of a user account, only accessible to the admin</td>
      </tr>
      <tr>
        <td>DELETE</td>
        <td>/users/{user_id}</td>
        <td>Remove a user account, only accessible to the admin</td>
      </tr>
    </table>

2. #### Category Endpoints
    The `/api/v2/categories` endpoint allows all the CRUD operations on the category items.
    <table style="width:100%">
      <tr>
        <td>POST</td>
        <td>/categories</td>
        <td>Add new category, only accessible to the admin</td>
      </tr>
      <tr>
        <td>GET</td>
        <td>/categories</td>
        <td>Retrieve all categories, only accesible by admin</td>
      </tr>
      <tr>
        <td>GET</td>
        <td>/categories/{category_id}</td>
        <td>Retrieve a single category, only accesible by admin</td>
      </tr>
      <tr>
        <td>PUT
        <td>/categories/{category_id}</td>
        <td>Update a specific category, only accesible by admin</td>
      </tr>
      <tr>
        <td>DELETE
        <td>/categories/{category_id}</td>
        <td>Remove a category, only accesible by admin</td>
      </tr>
    </table>

3. #### Product Endpoints
    The `api/v2/products` endpoint allows all CRUD operations on product items
    <table style="width:100%">
      <tr>
        <td>POST</td>
        <td>/products</td>
        <td>Add new product, only accessible to the admin</td>
      </tr>
      <tr>
        <td>GET</td>
        <td>/products</td>
        <td>Retrieve all products</td>
      </tr>
      <tr>
        <td>GET</td>
        <td>/products/{product_id}</td>
        <td>Retrieve a specific product</td>
      </tr>
      <tr>
        <td>PUT
        <td>/products/{product_id}</td>
        <td>Update a specific product, only accessible to admin</td>
      </tr>
      <tr>
        <td>DELETE
        <td>/products/{product_id}</td>
        <td>Remove a product, only accesible by admin</td>
      </tr>
    </table>

4. #### Sales Endpoints
    The `api/v2/sales` endpoint allows the following operations on sale items
    <table style="width:100%">
      <tr>
        <td>POST</td>
        <td>/sales</td>
        <td>Add new sale, only accessible to the attendant</td>
      </tr>
      <tr>
        <td>GET</td>
        <td>/sales</td>
        <td>Retrieve all sales</td>
      </tr>
      <tr>
        <td>GET</td>
        <td>/sales/{sale_id}</td>
        <td>Retrieve a single sale, displays a list of sold products in the sale</td>
      </tr>
    </table>
 
## Technologies used
The following software tools were used in the development of this application:
1. [Python](https://www.python.org/): Programming language.
2. [Flask](http://flask.pocoo.org/): The underlying web framework.
3. [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/): For the development of the API.
4. [Flasgger](https://github.com/rochacbruno/flasgger): For the generation of the API Docs. 
5. [Pytest](https://docs.pytest.org/en/latest/): For testing and debugging.
6. [PostgreSQL](https://www.postgresql.org/): Database.

##### Contributors
[John Wayodi](https://github.com/johnwayodi)