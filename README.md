# Full Stack API Final Project -- onlien drink store

## About the API
This web API is a new digita online drink store. 
Guests can see full drinks menu, number of drinks available in stock, and most popular drinks based on sales history. 
Bristas can "serve" drinks and update thhe transaction record and number of drinks in stock.  
Manager can restock drinks or add new drinks to the menu. Mananger is the only role that can see full transcation history of the store.

### API Link
Application is hosted on https://fsnd-moives.herokuapp.com/

### Authorization
User registration and login token acquired from here. 
https://ypdev.auth0.com/authorize?audience=coffeshop&response_type=token&client_id=cS494RG8HKdBhrEOkOXPekyhIQEEtIDG&redirect_uri=https://127.0.0.1:5000/login-results

User authourization needs to be assinged by the owner of the web API. 

### Roles type and access
1. Guest. Users without any token Will have permission for "get:/drinks" and "get:/transactions/popular".
2. Barista. In addition to guest permission, a Barista has permission for "delete:/transactions", "patch:/transactions", and "post:transactions". 
3. Manager. In addition to Barista permission, a manager has permission for "delete:/drinks", "patch:/drinks", "post:/drinks", and "get:/transactions".



## Getting Started
### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server

First ensure you are working using your created virtual environment.

Import environment varaible from  env_file

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

### Test cases
Test cases with sample token in test.py
In line21, set test database url and run python test.py 
