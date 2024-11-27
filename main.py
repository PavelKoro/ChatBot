from fastapi import FastAPI, HTTPException, status, Body
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from models import Person, QueryRequest, QueryResponse
from database import create_users_table, insert_user, authenticate_user
from SearchBD import process_query

app = FastAPI()

create_users_table()

@app.get("/", response_class=HTMLResponse)
def root():
    return "<h2>Главная</h2>"

@app.get("/regi")
def auth():
    return FileResponse("registra.html")

@app.post("/reg")
def register(person: Person):
    if person.email.endswith("@gmail.com"):
        try:
            insert_user(person)
            return RedirectResponse(url="/autharith", status_code=status.HTTP_303_SEE_OTHER)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Ошибка базы данных")
    else:
        raise HTTPException(status_code=400, detail="Неправильный формат email")

@app.get("/autharith")
def autharith():
    return FileResponse("auth.html")

@app.post("/authhh")
def authenticate(nickname: str = Body(embed=True), password: str = Body(embed=True)):
    user = authenticate_user(nickname, password)
    if user:
        return RedirectResponse(url="/search", status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=401, detail="Неверный никнейм или пароль")

@app.get("/search")
def search_page():
    return FileResponse("/home/pavel/proga/Ilya/poisk_test.html")

@app.post("/chatbot", response_model=QueryResponse)
async def chatbot_endpoint(request: QueryRequest):
    try:
        result = process_query(request.query)
        return QueryResponse(response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon available"}
