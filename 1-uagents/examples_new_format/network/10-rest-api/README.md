## Example of how to add custom REST endpoints to your agent

![domain:uAgents101](https://img.shields.io/badge/uAgents--101-3D8BD3?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMCAwLjVDMCAwLjIzNDM3NSAwLjIxODc1IDAgMC41IDBIMS41QzEuNzY1NjIgMCAyIDAuMjM0Mzc1IDIgMC41VjEuNUgwVjAuNVpNMCAySDJWNkgwVjJaTTAgNi41SDJWNy41QzIgNy43ODEyNSAxLjc2NTYyIDggMS41IDhIMC41QzAuMjE4NzUgOCAwIDcuNzgxMjUgMCA3LjVWNi41Wk0yLjUgMC41QzIuNSAwLjIzNDM3NSAyLjcxODc1IDAgMyAwSDRDNC4yNjU2MiAwIDQuNSAwLjIzNDM3NSA0LjUgMC41VjEuNUgyLjVWMC41Wk0yLjUgMkg0LjVWNkgyLjVWMlpNMi41IDYuNUg0LjVWNy41QzQuNSA3Ljc4MTI1IDQuMjY1NjIgOCA0IDhIM0MyLjcxODc1IDggMi41IDcuNzgxMjUgMi41IDcuNVY2LjVaTTUuNjcxODggNi4yMDMxMkw1IDMuNjQwNjJWMi4yMzQzOEw2LjU2MjUgMS44MTI1TDcuNTkzNzUgNS42ODc1TDUuNjcxODggNi4yMDMxMlpNNi40Mzc1IDEuMzI4MTJMNSAxLjcxODc1VjAuMTcxODc1TDUuNTYyNSAwLjAzMTI1QzUuODI4MTIgLTAuMDQ2ODc1IDYuMTA5MzggMC4xMDkzNzUgNi4xNzE4OCAwLjM3NUw2LjQzNzUgMS4zMjgxMlpNNS43OTY4OCA2LjY3MTg4TDcuNzE4NzUgNi4xNzE4OEw3Ljk2ODc1IDcuMTI1QzguMDQ2ODggNy4zOTA2MiA3Ljg5MDYyIDcuNjU2MjUgNy42MjUgNy43MzQzOEw2LjY3MTg4IDcuOTg0MzhDNi40MDYyNSA4LjA2MjUgNi4xMjUgNy45MDYyNSA2LjA2MjUgNy42NDA2Mkw1Ljc5Njg4IDYuNjcxODhaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)

By using one of the two new decorators: `on_rest_get()` and `on_rest_post()` you are able to define custom endpoints that your agent can act upon.
Please note that this feature is only available at the "agent-level" meaning that you cannot add rest endpoints to uagents `Protocols`.

The usage is similar to a message handler in that you define:

- a custom endpoint in string format, e.g. `"/my_rest_endpoint"`,
- a Request Model (inheriting from uagents.models) for `POST` endpoints, and
- a Response Model for `GET` endpoints

The difference to a message handler is that you actually have to invoke `return` for the value to be returned to the REST client. The format can either be `Dict[str, Any]` or the `Model` itself but either way the output will be validated against the predefined response model.

**GET request example**

```python
@agent.on_rest_get("/custom_get_route", Response)
async def handle_get(ctx: Context) -> Dict[str, Any]:
    return {
        "field": <value>,
    }
```

**POST request example**

```python
@agent.on_rest_post("/custom_post_route", Request, Response)
async def handle_post(ctx: Context, req: Request) -> Response:
    ctx.logger.info(req)  # access to the request
    return Response(...)
```

For querying the agent you have to make sure that:

1. You use the correct REST method ("GET" or "POST"), and
2. You address the agent endpoint together with its route (`http://localhost:8000/custom_route`)

### Run the example

1. Run the agent:

```bash
python agent.py
```

2. Query the agent directly through your predefined interfaces:

```bash
curl -d '{"text": "test"}' -H "Content-Type: application/json" -X POST http://localhost:8000/rest/post
```
