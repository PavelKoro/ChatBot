import sqlite3
import os
import difflib
def load_text_files(directory):
    files_content = {}
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                files_content[filename] = content
        else:
            print(f"Предупреждение: файл '{filename}' должен быть формата txt ")
    return files_content

def check_similarity(files_content):
    processed_files = []
    for filename, content in files_content.items():
        for other_filename, other_content in files_content.items():
            if filename == other_filename:
                continue
            similarity = difflib.SequenceMatcher(None, content, other_content).ratio()
            if similarity >= 0.95:  # 95% совпадение
                print(f"Предупреждение: файл '{filename}' похож на файл '{other_filename}' на {similarity * 100:.2f}%!")
                processed_files.append(filename)
                processed_files.append(other_filename)
    return processed_files

def main(directory):
    files_content = load_text_files(directory)
    check_similarity(files_content)

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

def upload_file(filepath):
    if not os.path.isfile(filepath):
        print("Файл не существует.")
        return
    
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    filename = os.path.basename(filepath)

    conn = sqlite3.connect('files.db')
    cursor = conn.cursor()

    # Проверка, существует ли такой файл в базе данных 
    cursor.execute('SELECT COUNT(*) FROM files WHERE filename = ?', (filename,))
    count = cursor.fetchone()[0]

    if count > 0:
        print(f"Файл с таким названием '{filename}' уже существует в базе данных.")
        return
    
    # Проверка на подобие содержимого
    cursor.execute('SELECT content FROM files')
    existing_contents = cursor.fetchall()

    for existing_content in existing_contents:
        similarity = difflib.SequenceMatcher(None, content, existing_content[0]).ratio()
        if similarity >= 0.95:  # 95% совпадение
            print(f"Файл с таким содержимым уже существует в базе данных.")
            conn.close()
            return

    # После проверки загружаем файл в базу данных
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
        
        choice = input("Ваш выбор: ")
        
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
