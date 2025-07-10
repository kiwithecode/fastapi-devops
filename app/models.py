from pydantic import BaseModel, Field


class Payload(BaseModel):
    message: str
    to: str
    from_: str = Field(alias="from")
    timeToLifeSec: int


class Response(BaseModel):
    message: str
