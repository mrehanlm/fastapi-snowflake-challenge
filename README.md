# fastapi-snowflake-challenge

This repository provides a RESTful API built with FastAPI and Snowflake, implementing basic CRUD operations for a clients table. It’s a simple, unprotected API for managing client data, ideal for learning FastAPI and Snowflake integration.

## Getting started

This guides you through setting up this project in your local environment.

### Prerequisites
- Docker – https://docs.docker.com/engine/install/
- Docker Compose – https://docs.docker.com/compose/install/
- Make utility – `sudo apt-get -y install make`
  
You just need to run the following command in order to start web server which will be live at http://localhost:8888/docs.

```bash
make up
```
Next, you can visit http://localhost:8888/docs for API docs and try out the APIs.

The `make up` will:
1. start fast api service
2. initialize snowflake connection
3. apply database migrations

We are using `alembic` for declarative database migrations and `snowflake-sqlalchemy` as an ORM for snowflake transactions.


This project also has pretty good unit tests coverage via `pytest` and you can run them by:
```bash
make pytest
```

Moreover, this uses `pre-commit` hooks to enforce code linting and formatting and you can install them by `make pre-commit` and finally, please have a look at `makefile` in project root directory for convenient shortcut commands.


[Database schema](./docs/dev/database.md)

Thank you!
