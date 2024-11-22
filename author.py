from fastapi import FastAPI, Query, Body
from fastapi.responses import RedirectResponse, PlainTextResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,Field


class Person(BaseModel):
    nickname: str 
    password: str
    email: str

app = FastAPI()

@app.get("/", response_class= HTMLResponse)
def root():
    data = "<h2>Главная</h2>"
    return data

@app.get("/autharith") ##перекидывает на страницу с автроризацией
def auth():
    return FileResponse("auth.html")



@app.post("/authhh") #получает данные с авторизации.Дописать связь с БД и проверкой на наличие данных в БД
def authhh(nickname = Body(embed=True), password = Body(embed=True)): 
    return{"message": f" {nickname} ваш пароль - {password}"}
