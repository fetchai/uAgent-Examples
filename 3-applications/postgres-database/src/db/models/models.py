from uagents import Model


class Employees(Model):
    employees_data: dict


class GetEmployees(Model):
    reply_back: bool
