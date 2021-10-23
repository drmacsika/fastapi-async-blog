# ASYNC FASTAPI BLOG

This is a set of asynchronous production-ready endpoints tested and built for blogs and portfolio websites.

![Blog Posts](https://github.com/drmacsika/am-backend/blob/master/templates/Screenshot%202021-10-23%20at%2020.48.16.png)

![Blog Category](https://github.com/drmacsika/am-backend/blob/master/templates/Screenshot%202021-10-23%20at%2020.48.28.png)

![Contact](https://github.com/drmacsika/am-backend/blob/master/templates/Screenshot%202021-10-23%20at%2020.48.39.png)

![User Accounts](https://github.com/drmacsika/am-backend/blob/master/templates/Screenshot%202021-10-23%20at%2020.48.48.png)

![User Auth](https://github.com/drmacsika/am-backend/blob/master/templates/Screenshot%202021-10-23%20at%2020.48.57.png)

## Tools

- FastAPI
- SQLAlchemy 2.0 Models using AsyncSession and Async DB Statements
- Alembic with automatic Models Migration
- Pydantic with custom validation and Settings
- OAuth2 Authentication
- JWT
- CORS
- Uvicorn and Gunicorn for Python web server
- TestClient for texting.

## Features

- Asynchronous CRUD endpoints for blog posts and categories
- Asynchronous CRUD endpoints for contacts
- Asynchronous CRUD endpoints for user accounts
- Asynchronous endpoints for user authentication
- Production ready settings file using Pydantic
- Migrations using Alembic
- Secure password hashing by default.
- JWT token authentication.

## Installation and Usage

Use the package manager [pip](https://pip.pypa.io/en/stable/) for installation.

```bash
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- cd fastapi-async-blog
- alembic revision --autogenerate -m "Init"
- alembic upgrade head
- uvicorn main:app --reload
```

## Contributing

Pull requests and contributions are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to follow the <a href="https://github.com/drmacsika/fastapi-async-blog/blob/master/CONTRIBUTING.md">guidelines</a> and update tests as appropriate.

## Contributing

Pull requests and contributions are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to follow the [guidelines](https://github.com/drmacsika/fastapi-async-blog/blob/master/CONTRIBUTING.md) and update tests as appropriate.

## Credits

All thanks to Tiangolo, I found the [Project Generation - Template](https://github.com/tiangolo/full-stack-fastapi-postgresql) incredibly helpful.

## Additional Info

For an in-depth understanding of FastAPI or any of the tools used here including questions and collaborations, you can reach out to me.
