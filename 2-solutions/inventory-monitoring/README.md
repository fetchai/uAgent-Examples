# Minimal multi-agent inventory monitoring

This project demonstrates a simple example of supply level monitoring, and how two agents can work together to keep a supply level consistent. These agents are working as siloed monitors, one agent tracks a fuel level, and another add more fuel to the store. A third agent randomly takes some fuel.

## Prerequisites
- [Poetry](https://python-poetry.org/docs/#installation) installed on your machine

## Dependencies
- Python >= 3.10
- tiny_db >= 2.9.9
- uagents == 0.13.0 (compatible with Python >= 3.10, < 3.13)

## Project Structure
```
.inventory-monitoring 
├── README.md
└── src
    ├── db.json
    └── main.py
```



## How run the project
- git clone  `https://github.com/fetchai/docs_examples.git`
- Navigate to the cloned repo
- in the root folder of the repo run `poetry install`
- then `cd src && poetry run python main.py`