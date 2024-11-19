# Agent Integration with PostgreSQL Data

This project demonstrates the integration of agents with PostgreSQL data, utilizing Python 3.10 and various dependencies. Agents are employed to insert and fetch employee data from a PostgreSQL database.


## Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed on your machine
- [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine
- [Poetry](https://python-poetry.org/docs/#installation) installed on your machine

## Dependencies
- Python >= 3.10
- psycopg2-binary >= 2.9.9
- uagents == 0.13.0 (compatible with Python >= 3.10, < 3.13)

## Project Structure
```
.postgres-database-with-an-agent 
├── docker-compose.yml
├── Dockerfile
├── README.md
└── src
    ├── constants.py
    ├── db
    │   ├── db_connection.py
    │   ├── __init__.py
    │   ├── models
    │   │   └── models.py
    │   └── schemas
    │       └── employees.sql
    └── main.py
```

## Usage with Docker

1. **Setup**: Ensure Docker is installed on your system.
2. **Configuration**: Update `.env` with necessary environment variables and configurations.
3. **Build**: Run `docker-compose build` to build the Docker images defined in the `docker-compose.yml` file.
4. **Run**: Execute `docker-compose up` to start the containers.
5. **Access**: Agents (`db_insert_agent`, `db_fetch_agent`) will interact with the PostgreSQL database as defined in `docker-compose.yml`.



## How run the project
- git clone  `https://github.com/fetchai/docs_examples.git`
- Navigate to the cloned repo.
- Update the constant file with new entries to store in the database
- Run `docker-compose build`
- Run `docker-compose up`