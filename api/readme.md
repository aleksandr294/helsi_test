# Api

## Setup

- Navigate to the api directory: Open a terminal (or command prompt) and navigate to the api directory of your project using the command ```cd path/helsi_test/api```, where ```path/helsi_test/api``` is the path to your API directory. 
- Create a virtual environment (venv): Run the following command to create a Python virtual environment.
- Install Poetry: Install the Poetry dependency management tool by executing:
```
pip install poetry
```
- Install project dependencies: After installing Poetry, execute the following command in your project directory to install dependencies:
````
poetry install
````
- Start the container with the database.
- Set .env. For example:
````
POSTGRES_URL=postgres://user:user@localhost:5432/helsi_test_db
SECRET_KEY=secret_key
DEBUG=True
````
- Run the project: To run the project, execute the following command:
```
source run.sh
```

## Usage

To run linters, formatters, and tests, use the following command:
```
source check_code.sh
```
Swagger: http://127.0.0.1:8000/api/schema/swagger-ui/

Email test user: ```test@mail.com```

Password test user: ```test_294```
