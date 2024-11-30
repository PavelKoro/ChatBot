import streamlit as st
import requests
import re

# Установка конфигурации страницы
st.set_page_config(
    page_title="Чат и загрузка файлов",
    page_icon="💬",
)

# URL для взаимодействия с чатботом
CHATBOT_URL = "http://localhost:9070/chatbot"
FILES_URL = "http://localhost:9070/files"
DELETE_URL = "http://localhost:9070/delete/"

# Инициализация состояния сессии
if 'users_db' not in st.session_state:
    st.session_state['users_db'] = {}
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def register_user(email, password):
    try:
        response = requests.post("http://localhost:9070/reg", json={"email": email, "password": password})
        response_data = response.json()
        
        if response.status_code == 200 and response_data.get("isRegister") == "true":
            st.success("Регистрация успешна!")
            st.session_state['page'] = 'chatbot'
        else:
            st.error("Ошибка при регистрации. Попробуйте еще раз.")
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка соединения с сервером: {e}")

def login_user(email, password):
    try:
        response = requests.post("http://localhost:9070/auth", json={"email": email, "password": password})
        response_data = response.json()
        
        if response.status_code == 200 and response_data.get("id") != "0":
            st.success("Добро пожаловать!")
            st.session_state['current_user'] = response_data.get("id")
            st.session_state['authenticated'] = True
            st.session_state['page'] = 'chatbot'
        else:
            st.error("Ошибка при авторизации. Попробуйте еще раз.")
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка соединения с сервером: {e}")

def send_file_to_api(user_id, file):
    try:
        # Подготовка данных для отправки
        files = {'file': (file.name, file.getbuffer(), file.type)}
        data = {'user_id': str(user_id)}  # Передача user_id как строки
        
        # Отправка файла на API
        response = requests.post("http://localhost:9070/upload", files=files, data=data)
        
        if response.status_code == 200:
            st.success("Файл успешно отправлен на сервер!")
        else:
            st.error(f"Ошибка при отправке файла: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка соединения с сервером: {e}")

def send_question_to_chatbot(user_id, query):
    """Отправляет вопрос на сервер чатбота и получает ответ."""
    try:
        response = requests.post(CHATBOT_URL, json={"user_id": user_id, "query": query})
        if response.status_code == 200:
            return response.json().get("response", "Чатбот не ответил.")
        else:
            return f"Ошибка: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Ошибка соединения с сервером: {e}"

def get_user_files(user_id):
    try:
        response = requests.get("http://localhost:9070/files", params={"user_id": user_id})
        if response.status_code == 200:
            files = response.json().get("files", [])
            return files
        else:
            st.error(f"Ошибка: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка соединения с сервером: {e}")
        return []

def delete_user_file(user_id, filename):
    try:
        response = requests.delete(f"{DELETE_URL}{filename}", params={"user_id": user_id})
        if response.status_code == 200:
            st.success(f"Файл '{filename}' удален.")
        else:
            st.error(f"Ошибка при удалении файла: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка соединения с сервером: {e}")

# Боковое меню для навигации
st.sidebar.title("Навигация")
page = st.sidebar.radio("Перейти на", ["Главная", "Авторизация", "Регистрация", "Chatbot", "Загрузить файл"])

# Основное содержимое
if page == "Главная":
    st.title("Главная страница")
    st.write("Добро пожаловать! Пожалуйста, выберите действие:")

elif page == "Авторизация":
    st.title("Авторизация")
    email = st.text_input("Email")
    password = st.text_input("Пароль", type="password")

    if st.button("Войти"):
        if not email or not password:
            st.error("Пожалуйста, заполните все поля.")
        elif not is_valid_email(email):
            st.error("Пожалуйста, введите действительный адрес электронной почты.")
        else:
            login_user(email, password)

elif page == "Регистрация":
    st.title("Регистрация")
    email = st.text_input("Email")
    password = st.text_input("Пароль", type="password")
    
    if st.button("Зарегистрироваться"):
        if not email or not password:
            st.error("Пожалуйста, заполните все поля.")
        elif not is_valid_email(email):
            st.error("Пожалуйста, введите действительный адрес электронной почты.")
        else:
            register_user(email, password)

elif page == "Chatbot" and st.session_state['authenticated']:
    st.title("Чатбот")
    # st.write(f"Добро пожаловать, {st.session_state['current_user']}!")

    # Отображение сообщений чата из истории
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Получение пользовательского ввода
    if prompt := st.chat_input("Введите ваш вопрос:"):
        # Добавление сообщения пользователя в историю чата
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Отображение сообщения пользователя
        with st.chat_message("user"):
            st.markdown(prompt)

        # Отправка вопроса чатботу и получение ответа
        assistant_response = send_question_to_chatbot(st.session_state['current_user'], prompt)

        # Отображение ответа ассистента
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        # Добавление ответа ассистента в историю чата
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

elif page == "Загрузить файл" and st.session_state['authenticated']:
    st.title("Загрузите файл")
    user_id = int(st.session_state['current_user'])
    uploaded_file = st.file_uploader("Загрузите текстовый файл", type="txt")
    
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        st.text_area("Содержимое файла:", file_content, height=200)
        
        if st.button("Отправить файл на сервер"):
            send_file_to_api(user_id, uploaded_file)

    st.subheader("Список ваших файлов:")
    files = get_user_files(user_id)
    
    if files:
        for file in files:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(file)
            with col2:
                if st.button("Удалить", key=file):
                    delete_user_file(user_id, file)
    else:
        st.write("У вас нет загруженных файлов.")

else:
    st.warning("Вы еще не вошли в систему. Пожалуйста, авторизуйтесь.")
