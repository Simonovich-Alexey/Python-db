import psycopg2
import os
from dotenv import load_dotenv


def create_db(cursor):
    with cursor.cursor() as cur:
        cur.execute("""
            DROP TABLE IF EXISTS telephone;
            DROP TABLE IF EXISTS client;
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                PRIMARY KEY (id_client),
                id_client       SERIAL          NOT NULL,
                first_name      VARCHAR(80)     NOT NULL,
                last_name       VARCHAR(80)     NOT NULL,
                email_client    TEXT UNIQUE     NOT NULL 
                                CHECK (email_client ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'));
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones(
                PRIMARY KEY (id_telephone),
                id_telephone        SERIAL          NOT NULL,
                phone_client        VARCHAR(20)     NULL,
                id_client           INTEGER         NOT NULL
                                    REFERENCES client(id_client));
        """)
        cursor.commit()


def add_client(cursor, first_name, last_name, email_client, phone_client=None):
    with cursor.cursor() as cur:
        cur.execute("""
            INSERT INTO client(first_name, last_name, email_client)
            VALUES (%s, %s, %s)
            RETURNING id_client;""", (first_name, last_name, email_client))
        id_client = cur.fetchone()[0]

        if phone_client:
            cur.execute("""
                INSERT INTO phones(phone_client, id_client)
                VALUES (%s, %s);""", (phone_client, id_client))

        cursor.commit()
        print(f"Клиент добавлен, ID = {id_client}")


def add_phone(cursor, id_client, phone_client):
    with cursor.cursor() as cur:
        cur.execute("""
            INSERT INTO phones(phone_client, id_client)
            VALUES (%s, %s)
            RETURNING phone_client, id_client;""", (phone_client, id_client))
        db_info = cur.fetchone()
        print(f'Телефон {db_info[0]} добавлен клиенту c id={db_info[1]}')
        cursor.commit()


def change_client(cursor, id_client, first_name=None, last_name=None, email_client=None, phone_client=None):
    if first_name:
        with cursor.cursor() as cur:
            cur.execute("""
                UPDATE client
                SET first_name = %s
                WHERE id_client = %s;""", (first_name, id_client))
    if last_name:
        with cursor.cursor() as cur:
            cur.execute("""
                UPDATE client
                SET last_name = %s
                WHERE id_client = %s;""", (last_name, id_client))
    if email_client:
        with cursor.cursor() as cur:
            cur.execute("""
                UPDATE client
                SET email_client = %s
                WHERE id_client = %s;""", (email_client, id_client))
    if phone_client:
        with cursor.cursor() as cur:
            cur.execute("""
                SELECT id_telephone, phone_client
                FROM phones
                WHERE id_client = %s;""", (id_client,))
            db_info = cur.fetchall()
            if len(db_info) > 1:
                for i in db_info:
                    print(f"Телефон {i[1]} - ID = {i[0]}")
                id_phone = int(input(f"Введите ID телефона который хотите изменить: "))
                cur.execute("""
                    UPDATE phones
                    SET phone_client = %s
                    WHERE id_client = %s
                    AND id_telephone = %s;""", (phone_client, id_client, id_phone))
            if len(db_info) == 1:
                cur.execute("""
                    UPDATE phones
                    SET phone_client = %s
                    WHERE id_client = %s;""", (phone_client, id_client))


def delete_phone(cursor, id_client, phone_client):
    with cursor.cursor() as cur:
        cur.execute("""
                DELETE FROM phones
                WHERE   id_client = %s 
                AND     phone_client = %s;""", (id_client, phone_client))

        print(f'Телефон {phone_client} удален у клиента c id={id_client}')
        cursor.commit()


if __name__ == '__main__':
    load_dotenv()
    with psycopg2.connect(database="clients_db", user="postgres", password=os.getenv('PSW_DB')) as conn:
        # create_db(conn)
        # add_client(conn, 'Михаил', 'Лермонтов', 'mlermontov@mail.ru')
        # add_client(conn, 'Александр', 'Пушкин', 'apushkin@gmail.com', '+7 (495) 234-56-78')
        # add_client(conn, 'Лев', 'Толстой', 'ltolstoy@yahoo.com', '+7 (495) 345-67-89')
        # add_client(conn, 'Антон', 'Чехов', 'achehov@hotmail.com', '+7 (495) 456-78-90')
        # add_client(conn, 'Сергей', 'Есенин', 'sesenin@yandex.ru', '+7 (495) 567-89-01')
        # add_client(conn, 'Анна', 'Ахматова', 'aahmatova@gmail.com')
        # add_client(conn, 'Николай', 'Гоголь', 'ngogol@mail.ru', '+7 (495) 234-56-78')
        # add_phone(conn, 3, '+7 (495) 123-45-67')
        # add_phone(conn, 2, '+7 (495) 567-89-01')
        # add_phone(conn, 4, '+7 (495) 567-29-66')
        # add_phone(conn, 6, '+7 (495) 567-69-12')
        add_phone(conn, 7, '+7 (495) 567-81-97')
        # change_client(conn, 3, first_name=None, last_name=None, email_client=None, phone_client='+7 (495) 123-45-85')
        # delete_phone(conn, 2, '+7 (495) 567-89-01')

    conn.close()
