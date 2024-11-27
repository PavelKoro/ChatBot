from pydantic import BaseModel

class Person(BaseModel):
    nickname: str
    password: str
    email: str

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str