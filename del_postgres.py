import psycopg2

def delete_table(name_db):
    conn = psycopg2.connect(
        host='localhost', 
        dbname='postgres', 
        user='postgres', 
        password='qwerty', 
        port=5432
    )
    cur = conn.cursor()

    cur.execute(f"DROP TABLE IF EXISTS {name_db};")
    conn.commit()

    cur.close()
    conn.close()
    print("[INFO]: Table deleted successfully.")