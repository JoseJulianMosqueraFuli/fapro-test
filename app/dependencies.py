from pydantic import BaseModel


class UFRequest(BaseModel):
    date: str
