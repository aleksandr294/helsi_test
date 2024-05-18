

## Description

I have decided to split the application into two services. The first service will provide an API for retrieving currency exchange rate data, with the ability to select specific currencies for tracking. The second service will perform the functions of a worker, which will retrieve this information from the bank's API or other sources and write it to the database.

I believe that such division will simplify maintenance and scalability of the system, as well as increase its fault tolerance. Here's a more detailed description:

#### API Service:
- This service will provide an API for accessing currency exchange rate data.
- Users will be able to select the currencies they want to track.
- The API service will handle user requests, extract the corresponding data from the database, and return it to the users.

#### Worker Service:
- The worker service will operate independently and periodically retrieve information about currency exchange rates from the bank's API or other sources.
- After obtaining the data, the worker will write it to the database. 
- This service will ensure regular updates of the database with the latest currency exchange rate data.
- The worker will update the data every 30 minutes to ensure the accuracy of the information in the database.

By dividing responsibilities between the API service and the worker service, each component can focus on its specific task. This will simplify understanding, maintenance, and scalability of the system. Additionally, if one service experiences a failure, it won't necessarily affect the operation of the other service, thereby increasing the overall resilience of the system.

### Running via docker-compose:

```
docker-compose -f docker-compose.local.yml up --build
```



## Api

### Setup

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

### Usage

To run linters, formatters, and tests, use the following command:
```
source check_code.sh
```
Swagger: http://127.0.0.1:8000/api/schema/swagger-ui/

Command to create a test user:

```
python manage.py test_user
```

Email test user: ```test@mail.com```

Password test user: ```test_294```

To export exchange rates, enter the command:

The file will be saved in the default path: ```/path/to/helsti_test/current_currencies.csv```

```
python manage.py build_csv
```

To save using a custom path:

```
python manage.py build_csv /path/to/your/file
```



## Worker

### Setup

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

### Usage

To run linters, formatters, and tests, use the following command:
```
source check_code.sh
```

