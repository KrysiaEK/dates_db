# Dates Database
API to check what happened on a certain date.

## Tools explanation:
- Django, Django REST Framework - I have the most experience in using these frameworks. 
- PostgreSQL - I have the most experience in using this database.
- django-environ - I think that project configuration should be done through environment variables.
- Core API - I had to connect to an external api and this is .
- Django REST Framework API key - I had to use API key.
- Factory Boy - it is easier and faster than fixtures.
- Linters - code quality and security is important to me.
    + Flake8
    + Isort
    + Vulture
    + Django Migration Linter
    + Dotenv Linter
    + Safety
    + We Make Python Styleguide
- Unittest XML Reporting - to save test results in a file. 

## Local development:
1. Clone repository
2. Run ```docker-compose build```
3. Run migrations: 
```docker-compose run web python manage.py migrate```
4. Run test command to make sure everything is in order:
```docker-compose run web python manage.py test dates_db```
5. Start the development server with command: ```docker-compose up```

## Deployment:
1.	Create `docker-compose.yml` file with the following contents in folder destined for this project:

```
version: "3.9"

services:
  db:
    image: postgres
    volumes:
      - ./data/db:/var/lib/postgresql/data
    env_file:
      - docker.env

  web:
    image: krysiaek/dates_db
    ports:
      - "8000:8000"
    env_file:
      - docker.env
    depends_on:
      - db
```

2.  Create file `docker.env` with the following content:
```
DEBUG=False
ALLOWED_HOSTS=host1 host2
DJANGO_SECRET_KEY=random_value
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
```
4. Run:
```docker-compose pull```
5. Run migrations: 
```docker-compose run web python manage.py migrate```
6. Run test command to make sure everything is in order:
```docker-compose run web python manage.py test dates_db```
7. Generate API key: 
```docker-compose run web python manage.py generate_api_key```
8. Start the server:
 ```docker-compose up```

The project works on port 8000.

## Server

The test server runs on [dates.krysia.me](http://dates.krysia.me)
