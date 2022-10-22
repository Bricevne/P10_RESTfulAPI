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

## Usage

Run the following code to access the api:

```bash
python manage.py migrate # Create the migrations
python manage.py runserver # Start the local server
```

You can then access the website with http://127.0.0.1:8000/api/

## License

[MIT](https://choosealicense.com/licenses/mit/)
