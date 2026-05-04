# FastAPI endpoint definition
import fastapi
from pydantic import BaseModel

app = fastapi.FastAPI()


def to_camel_case(snake_str: str) -> str:
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class User(BaseModel, populate_by_name=True, alias_generator=to_camel_case):
    first_name: str
    last_name: str


@app.post("/users/")
def create_user(user: User):
    # do important things
    return {"user_name": user.name, "user_id": user.id}
