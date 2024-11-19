import os

employees_data = {
    "EmployeeID": "",
    "FirstName": "",
    "LastName": "",
    "BirthDate": "",
    "Salary": 0,
}

db_params = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": "db",
    "port": "5432",
}

DB_FETCH_AGENT_ADDRESS = (
    "agent1qwg0h3gx2kvqmwadlg0j4r258r7amcfskx2mudz92ztjmtfdclygxrh5esu"
)
