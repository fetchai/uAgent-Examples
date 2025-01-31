from book import book_proto
from query import TableStatus, query_proto

# build the restaurant agent from stock protocols
agent.include(query_proto)
agent.include(book_proto)

TABLES = {
    1: TableStatus(seats=2, time_start=16, time_end=22),
    2: TableStatus(seats=4, time_start=19, time_end=21),
    3: TableStatus(seats=4, time_start=17, time_end=19),
}

# set the table availability information in the restaurant protocols
for number, status in TABLES.items():
    agent.storage.set(number, status.dict())
