# Knowledge

Knowledge is the place Labcodes can always find great resources to read, answers to their questions
and best practices. Everything curated by the most awesome people in the world, our teammates.

## Project Setup

### Setting up .env file

Create a new file in the root folder called `.env`.
Inside it, create a variable `DEBUG` with value `True` and another called `SLACK_TOKEN` and you will
find the value for the token in this url: https://api.slack.com/docs/oauth-test-tokens

### Setting up the local_settings.py file

Inside the `knowledge` folder, there's a file called `local_settings.py.example`.
Create a new `local_settings.py` file and you will just have to change the `USER` and `password` keys.

### Installing Postgresql

Install the Postgresql database and it's dependencies with the following command:

```
sudo apt-get install python-dev libpq-dev postgresql postgresql-contrib
```

Access the Postgresql shell and create a new database:

```
sudo su - postgres
psql
CREATE DATABASE knowledge;
```

### Installing the requirements for the project

Install all the dependencies for the project:

```
python manage.py -r requirements.txt
```

### Migrating the existing apps

Now you need migrate the existing apps in the project:

```
python manage.py migrate
```

### Running the project

You should now be able to run the project. Run the following command to start the server:

```
python manage.py runserver
```

Open the index page in your browser:

```
http://localhost:8000/
```
