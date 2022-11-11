# Build a secure REST API using Django REST - OpenClassrooms project 10

This project is about developing a secure REST API enabling the three platforms (web, Android and iOS) to use this issue
tracking application.

## Installation

Clone [the repository](https://github.com/Bricevne/P10_RESTfulAPI.git) on your computer.

```
git clone https://github.com/Bricevne/P10_RESTfulAPI.git
```

Set your virtual environment under [python 3.10](https://www.python.org/downloads/release/python-3100/)

```bash
pipenv install # Create the virtual environment and install the dependencies
pipenv shell # Activate the virtual environment
pipenv install -r requirements.txt # Install the dependencies
```

Create a file where you'll put the django secret key:

```bash
touch .env # File for environment variables
```

Insert your django secret key in the .env file

`DJANGO_SECRET_KEY="DJANGO_SECRET_KEY"`


## Launch the local server

Enter the "src" folder and run the following code to access the api:

```bash
python manage.py migrate # Create the migrations
python manage.py runserver # Start the local server
```

## Use Postman to test the API's endpoints

### Install Postman
You can install Postman by following the instructions from the following url:

`https://www.postman.com/downloads/"`

### Authentication

The /signup and /login endpoints do not need an authentication token to access.

All the other endpoints are only accessible by an authenticated user after generation of a simple JWT access token. 
Moreover, a user has to be a contributor or a project author to have access to endpoints for specific projects, 
issues and comments.

### Collection test

You can either test all endpoints at once through the "Run collection" button, or one by one.

This collection is divided into several folders:
- "Authentication": /signup and /login endpoints which do not need an access token.
- "Projects": /projects endpoints for CRUD actions on projects. Needs an access token.
- "Users": /users endpoints for CRD actions on contributors. Needs an access token.
- "Issues": /issues endpoints for CRUD actions on issues. Needs an access token.
- "Comments": /comments endpoints for CRUD actions on comments. Needs an access token.

For ease of use, this API collection automatically add the JWT access token to environment variables after logging with
an account. This variable is thus inherited by the Projects, Users, Issues and Comments folders.

## License

[MIT](https://choosealicense.com/licenses/mit/)
