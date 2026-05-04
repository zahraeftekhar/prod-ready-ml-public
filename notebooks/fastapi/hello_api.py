from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello():
    return "Hello, world!"


@app.get("/zahra/{name}")
def greet(name: str):
    return f"Hello, {name}!"


@app.get("/greet_int")
@app.get("/greet_int/{num}")
def greet_int(num: int | None = None):
    if num is None:
        return "No number provided"
    return f"Hello, number {num}!"
