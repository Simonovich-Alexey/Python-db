import psycopg2
import os
from dotenv import load_dotenv


def create_db():
    load_dotenv()
    conn = psycopg2.connect(database='customers', user='postgres', password=os.getenv('PSW_DB'))
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE IF EXISTS telephone;
            DROP TABLE IF EXISTS client;
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            id_client SERIAL PRIMARY KEY,
            name_client VARCHAR(80) NOT NULL,
            surname_client VARCHAR(80) NOT NULL,
            email_client TEXT UNIQUE NOT NULL CHECK 
            (email_client ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'));
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS telephone(
            id_tel SERIAL PRIMARY KEY,
            telephone_client VARCHAR(20),
            id_client INTEGER NOT NULL REFERENCES client(id_client));
        """)
        conn.commit()

    conn.close()


def add_client(name, surname, email):
    load_dotenv()
    conn = psycopg2.connect(database='customers', user='postgres', password=os.getenv('PSW_DB'))
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client(name_client, surname_client, email_client)
            VALUES (%s, %s, %s)
            RETURNING id_client, name_client, surname_client;""", (name, surname, email))
        db_info = cur.fetchone()
        print(f'Клиент: {db_info[1]} {db_info[2]}, добавлен под id={db_info[0]}')
        conn.commit()

    conn.close()


def add_telephone(tel, id_client):
    load_dotenv()
    conn = psycopg2.connect(database='customers', user='postgres', password=os.getenv('PSW_DB'))
    with conn.cursor() as cur:
        cur.execute("""
                INSERT INTO telephone(telephone_client, id_client)
                VALUES (%s, %s) RETURNING telephone_client, id_client;""", (tel, id_client))
        db_info = cur.fetchone()
        print(f'Телефон {db_info[0]} добавлен клиенту c id={db_info[1]}')
        conn.commit()
    conn.close()


if __name__ == '__main__':
    # add_client('Александр', 'Пушкин', 'apushkin@gmail.com')
    add_telephone('+7 (495) 234-56-78', 5)
