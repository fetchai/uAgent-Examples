# Async Loops Agent Example

This example demonstrates how to integrate agents with an external event loop, allowing agents to run within a pre-existing loop. You'll learn how to attach agents or bureaus to an external loop and manage agent lifecycle events.

## Key Concepts

### Attaching to an External Loop

Agents can attach to an external event loop without taking control of it. Use `agent.run_async()` to attach an agent to a loop. In `external_loop_attach.py`, this is done using:

```python
loop.create_task(agent.run_async())  
```

### Starting an Agent with an External Loop

For more advanced control, start an agent within an external loop using `agent.run()` or `bureau.run()`. In `external_loop_run.py`, this is done with:

```python
agent.run()  
```

### Lifecycle Events

Use `@agent.on_event("startup")` and `@agent.on_event("shutdown")` to manage tasks at agent startup and shutdown, ensuring the agent performs necessary setup or cleanup.

### Running Additional Coroutines

You can run coroutines alongside agents. Both examples include a simple `coro()` function that runs concurrently with the agent.

## Running the Example

### Attach Agent/Bureau to External Loop

In `external_loop_attach.py`, attach the agent or bureau to the loop:

```python
python external_loop_attach.py  
```

### Start Agent/Bureau with External Loop

In `external_loop_run.py`, start the agent or bureau with the loop:

```python
python external_loop_run.py  
```

These examples show how agents can operate seamlessly within an existing asyncio loop.
