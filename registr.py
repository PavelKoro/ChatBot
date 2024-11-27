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

@app.get("/regi") #перекидывает на страницу с регистрацией
def auth():
    return FileResponse("registra.html")



@app.post("/reg") #получает данные для регистрации проверяет корректность введенного email. Дописать связь с БД и создание профиля там
def authhh(nickname = Body(embed=True), password = Body(embed=True), email = Body(embed=True)):
    a = "@gmail.com"
    t = 0
    i = 0
    c = 0
    for b in email:
        if(b == "@"):
            c = c + 1
            t = i
        i = i + 1
    size = len(email)
    flag = 1
    i = 0
    if(t > 0):
        while(t < size):
            if(email[t] != a[i]):
                flag = 0
            t = t + 1
            i = i + 1

    if(c == 1 and flag > 0):
        return {"message": f"OK"}
    else:
        return {"message": f"Bad"}



#Еще для красоты - создать кнопки котоыре будут находиться в главной странице и перекидывать на регистрацию и атворизацмю