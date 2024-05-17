# Worker

## Setup

- Navigate to the api directory: Open a terminal (or command prompt) and navigate to the api directory of your project using the command ```cd path/helsi_test/worker```, where ```path/helsi_test/worker``` is the path to your API directory. 
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
POSTGRES_URL=postgresql+psycopg2://user:user@localhost:5432/helsi_test_db
BANK_URL=https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json
REDIS_URL=redis://localhost:6379/0
````
- Run the project:
```
celery -A main beat --loglevel=info & celery -A main worker --loglevel=info
```

## Usage

To run linters, formatters, and tests, use the following command:
```
source check_code.sh
```
