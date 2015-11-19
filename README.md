## Numbles

A Django-based web application for managing personal finances.

### Screenshot

[![Preview](http://i.stack.imgur.com/6gmbb.jpg)](http://i.stack.imgur.com/8uObu.png)

### Requirements

In order to use Numbles, you will need the following applications installed:

 - [Python 2.7+](http://python.org)
 - [pip](https://pypi.python.org/pypi/pip)
 - [PostgreSQL 9.1+](http://postgresql.org)

You will also need to install a number of Python packages. This can be done automatically by running the following command in the directory containing the source code for Numbles:

    pip install -r requirements.txt

### Installation

Please carefully follow the instructions below to install Numbles:

1. Create a PostgreSQL user and database:

        CREATE USER numbles WITH PASSWORD 'insert_password_here';
        CREATE DATABASE numbles WITH OWNER numbles;

2. Copy `numbles/local_settings.py.default` to `numbles/local_settings.py.`.

3. Open `numbles/local_settings.py` and edit the settings as needed.

4. Perform database migrations:

        ./manage.py migrate

5. Create a superuser:

        ./manage.py createsuperuser

6. To launch the development server, run the following command:

        ./manage.py runserver
