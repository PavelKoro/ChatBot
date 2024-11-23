import sqlite3
import os

# Функция для подключения к базе данных и создания таблицы
def create_database():
    conn = sqlite3.connect('files.db')  # Подключаемся к базе данных (если файл не существует, он будет создан)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Функция для загрузки файла в базу данных
def upload_file(filepath):
    if not os.path.isfile(filepath):
        print("Файл не существует.")
        return
   
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
   
    filename = os.path.basename(filepath)

    conn = sqlite3.connect('files.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO files (filename, content) VALUES (?, ?)', (filename, content))
    conn.commit()
    conn.close()

    print(f"Файл '{filename}' загружен в базу данных.")

# Функция для удаления файла из базы данных по имени
def delete_file(filename):
    conn = sqlite3.connect('files.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM files WHERE filename = ?', (filename,))
    conn.commit()
    conn.close()
   
    print(f"Файл '{filename}' удален из базы данных.")

# Функция для отображения содержимого базы данных
def display_files():
    conn = sqlite3.connect('files.db')
    cursor = conn.cursor()
    cursor.execute('SELECT filename FROM files')
    files = cursor.fetchall()
    conn.close()

    if files:
        print("Список загруженных файлов:")
        for file in files:
            print(file[0])
    else:
        print("База данных пуста.")

# Основная программа
if __name__ == "__main__":
    create_database()
   
    while True:
        print("\nВыберите действие:")
        print("1. Загрузить файл")
        print("2. Удалить файл")
        print("3. Показать файлы")
        print("4. Выход")
       
        choice = input("\nВаш выбор: ")
       
        if choice == '1':
            filepath = input("Введите путь к загружаемому файлу: ")
            upload_file(filepath)
        elif choice == '2':
            filename = input("Введите имя файла для удаления: ")
            delete_file(filename)
        elif choice == '3':
            display_files()
        elif choice == '4':
            break
        else:
            print("Неверный выбор, попробуйте снова.")
