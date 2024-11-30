from fastapi import FastAPI, HTTPException, status, Body, UploadFile, File, Depends, Request, Form, Query
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from models import UserRegister, QueryRequest, QueryResponse
from database import create_users_table, insert_user, authenticate_user, get_user_id_name
from list_file_user_db import create_file_list_db, insert_file_list, delete_file_list_db, get_file_list
from SearchBD import process_query
from pydantic import BaseModel
global USER_ID

app = FastAPI()

create_users_table()
create_file_list_db()

@app.get("/", response_class=HTMLResponse)
def root():
    return "<h2>Главная</h2>"



@app.post("/reg")
def register(new_user: UserRegister):
    user_id = insert_user(new_user.email, new_user.password)
    if user_id > 0:
        return {"isRegister": "true"}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")

@app.post("/auth")
def register(new_user: UserRegister):
    user_id = authenticate_user(new_user.email, new_user.password)
    if user_id > 0:
        return {"id": f"{user_id}"}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")


@app.get("/search")
def search_page(request: Request):
    user_id = request.query_params.get("user_id", None)
    redirect_url = f"http://localhost:8502?user_id={user_id}"
    return RedirectResponse(redirect_url)

@app.post("/chatbot", response_model=QueryResponse)
async def chatbot_endpoint(request: QueryRequest):
    try:
        print(request.user_id, request.query)
        result = process_query(request.user_id, request.query)
        return QueryResponse(response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon available"}

## API добавления, удаления и просмотра файлов в БД
@app.post("/upload")
async def upload_file(user_id: int = Form(...), file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename
    success, message = insert_file_list(user_id, filename, content.decode('utf-8'))
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"status": 200, "message": message}

@app.delete("/delete/{filename}")
async def delete_file(user_id: int, filename: str):
    success, message = delete_file_list_db(user_id, filename)
    if not success:
        raise HTTPException(status_code=404, detail=message)
    return {"message": message}

@app.get("/files")
async def display_files(user_id: int = Query(...)):
    try:
        result = get_file_list(user_id)
        files, error = result if isinstance(result, tuple) else (result, None)
        if files is None:
            raise HTTPException(status_code=500, detail="Ошибка при отображении файлов из базы данных.")
        
        if not files:
            return {"status": 200, "message": "База данных пуста.", "files": []}
        
        return {"status": 200, "files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
