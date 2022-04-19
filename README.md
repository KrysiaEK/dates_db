# Dates Database
API to check what happened on a certain date.

## Deployment:
1.	Create docker-compose.yml file with the following contents in folder destined for this project:

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

2.  Create file docker.env with the following content:
```
DJANGO_SECRET_KEY=random_value
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
```
4. Run ```docker-compose pull```
5. Run test command to make sure everything is in order:
```docker-compose run web python manage.py test dates_db```
6. Start the server:
 ```docker-compose up```

The project works on port 8000.

## Server
