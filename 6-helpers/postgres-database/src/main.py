from db.db_connection import create_connection
from uagents import Agent, Context, Bureau
from db.models.models import Employees, GetEmployees
from constants import employees_data
from constants import db_params, DB_FETCH_AGENT_ADDRESS


def get_db_version():
    """
    Retrieves the PostgreSQL database version.

    :return: Database version string or None if retrieval fails
    """
    conn = create_connection(**db_params)
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            cursor.close()
            return db_version
        except Exception as error:
            print(f"Error executing query: {error}")
            return None


db_insert_agent = Agent(name="db_inserter", seed="db_inserter_seed_phrase")
db_fetch_agent = Agent(name="db_fetcher", seed="db_fetcher_seed_phrase")

DB_FETCH_AGENT_ADDRESS = DB_FETCH_AGENT_ADDRESS


@db_fetch_agent.on_event("startup")
async def on_startup(ctx: Context):
    """
    Event handler triggered on agent startup to fetch database version and send employee data.

    :param ctx: Context object for handling agent events
    """
    db_version = get_db_version()
    if db_version:
        ctx.logger.info(
            f"Hello, I'm agent {db_insert_agent.name} and my address is {db_insert_agent.address}. PostgreSQL database version: {db_version[0]}"
        )
        await ctx.send(DB_FETCH_AGENT_ADDRESS, Employees(employees_data=employees_data))
    else:
        ctx.logger.info(
            f"Hello, I'm agent {db_insert_agent.name} and my address is {db_insert_agent.address}. Could not retrieve the database version."
        )


@db_insert_agent.on_message(model=Employees, replies=GetEmployees)
async def handle_employee_data(ctx: Context, sender: str, msg: Employees):
    """
    Handler for inserting employee data into the database.

    :param ctx: Context object for handling agent events
    :param sender: Sender of the message
    :param msg: Message containing employee data
    """
    ctx.logger.info(f"Received request from {sender} {msg.dict()}")
    employee_data = msg.employees_data
    conn = create_connection(**db_params)
    if conn:
        try:
            cursor = conn.cursor()
            insert_query = """
            INSERT INTO Employees (EmployeeID, FirstName, LastName, BirthDate, Salary)
            VALUES (%s, %s, %s, TO_DATE(%s, 'DD-MM-YYYY'), %s)
            """
            cursor.execute(
                insert_query,
                (
                    employee_data["EmployeeID"],
                    employee_data["FirstName"],
                    employee_data["LastName"],
                    employee_data["BirthDate"],
                    employee_data["Salary"],
                ),
            )
            REPLY_BACK = True
            conn.commit()
            cursor.close()
            ctx.logger.info(f"Inserted employee data: {employee_data}")
            await ctx.send(sender, GetEmployees(reply_back=REPLY_BACK))
        except Exception as error:
            ctx.logger.error(f"Error inserting employee data: {error}")
    else:
        ctx.logger.error("Could not connect to the database.")


@db_fetch_agent.on_message(model=GetEmployees)
async def fetch_all_employee_details(ctx: Context, sender: str, msg: GetEmployees):
    """
    Handler for fetching all employee details from the database.

    :param ctx: Context object for handling agent events
    :param sender: Sender of the message
    :param msg: Message triggering the fetch operation
    """
    if msg.reply_back:
        conn = create_connection(**db_params)
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT * FROM Employees"
                cursor.execute(query)
                all_employees = cursor.fetchall()
                cursor.close()

                employees_list = []
                for employee in all_employees:
                    employee_info = {
                        "EmployeeID": employee[0],
                        "FirstName": employee[1],
                        "LastName": employee[2],
                        "BirthDate": employee[3].strftime("%d-%m-%Y"),
                        "Salary": employee[4],
                    }
                    employees_list.append(employee_info)
                ctx.logger.info(f"Retrieved all employee data: {employees_list}")
            except Exception as error:
                ctx.logger.error(f"Error retrieving employee data: {error}")
        else:
            ctx.logger.error("Could not connect to the database.")


bureau = Bureau()
bureau.add(db_insert_agent)
bureau.add(db_fetch_agent)

if __name__ == "__main__":
    bureau.run()
