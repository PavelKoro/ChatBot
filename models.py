from pydantic import BaseModel

# Определяем модель данных для проверки входящих данных
class UserRegister(BaseModel):
    email: str
    password: str

class QueryRequest(BaseModel):
    user_id: int
    query: str

class QueryResponse(BaseModel):
    response: str
