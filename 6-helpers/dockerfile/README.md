# Agent with Docker

This project demonstrates how to run an agent using `uagents` within a Docker container managed by Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your machine
- [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine
- [Poetry](https://python-poetry.org/docs/#installation) installed on your machine

## Dependencies
- Python >= 3.10
- uagents == 0.13.0 (compatible with Python >= 3.10, < 3.13)

## Project Structure

```
.agent_with_docker_vm
├── docker-compose.yml
├── Dockerfile
├── poetry.lock
├── pyproject.toml
├── README.md
└── src
    └── agent.py
```

## How run the project
- git clone  `https://github.com/fetchai/docs_examples.git`
- Navigate to the cloned repo.
- Run `docker-compose build`
- Run `docker-compose up`


