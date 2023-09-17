import pprint
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
                PRIMARY KEY (id_phone),
                id_phone            SERIAL          NOT NULL,
                phone_client        VARCHAR(20)     NOT NULL,
                id_client           INTEGER         NOT NULL,
                CONSTRAINT fk_id_client FOREIGN KEY(id_client)
                REFERENCES client(id_client)
                ON DELETE CASCADE);
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

        print(f"Клиент добавлен, ID = {id_client}")


def add_phone(cursor, id_client, phone_client):
    with cursor.cursor() as cur:
        cur.execute("""
            INSERT INTO phones(phone_client, id_client)
            VALUES (%s, %s)
            RETURNING phone_client, id_client;""", (phone_client, id_client))
        info = cur.fetchone()
        print(f'Телефон {info[0]} добавлен клиенту c id={info[1]}')


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
                SELECT id_phone, phone_client
                FROM phones
                WHERE id_client = %s;""", (id_client,))
            info = cur.fetchall()
            if len(info) > 1:
                for i in info:
                    print(f"Телефон {i[1]} - ID = {i[0]}")
                id_phone = int(input(f"Введите ID телефона который хотите изменить: "))
                cur.execute("""
                    UPDATE phones
                    SET phone_client = %s
                    WHERE id_client = %s
                    AND id_phone = %s;""", (phone_client, id_client, id_phone))
            if len(info) == 1:
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

        cursor.commit()
        print(f'Телефон {phone_client} удален у клиента c id={id_client}')


def delete_client(cursor, id_client):
    with cursor.cursor() as cur:
        cur.execute("""
            DELETE FROM client
            WHERE       id_client = %s
            RETURNING   id_client;""", (id_client,))
        print(f'Клиент с ID = {cur.fetchone()[0]} удален!')


def find_client(cursor, first_name=None, last_name=None, email_client=None, phone_client=None):
    params = {'first_name': first_name, 'last_name': last_name, 'email_client': email_client,
              'phone_client': phone_client}
    for key, value in params.items():
        if value is None:
            params.update({key: '%'})
    with cursor.cursor() as cur:
        cur.execute("""
                SELECT c.id_client, c.first_name, c.last_name, c.email_client, p.phone_client FROM client AS c
                LEFT JOIN phones AS p ON c.id_client = p.id_client
                WHERE c.first_name LIKE %s
                AND c.last_name LIKE %s
                AND c.email_client LIKE %s
                AND p.phone_client LIKE %s;""", (params.get('first_name'), params.get('last_name'),
                                                 params.get('email_client'), params.get('phone_client')))
        pprint.pprint(cur.fetchall())


if __name__ == '__main__':
    load_dotenv()
    with psycopg2.connect(database="clients_db", user="postgres", password=os.getenv('PSW_DB')) as conn:
        # create_db(conn)
        # add_client(conn, 'Михаил', 'Лермонтов', 'mlermontov@mail.ru')
        # add_client(conn, 'Александр', 'Пушкин', 'apushkin@gmail.com', '+7 (495) 234-56-78')
        # add_client(conn, 'Лев', 'Толстой', 'ltolstoy@yahoo.com', '+7 (495) 345-67-89')
        # add_client(conn, 'Антон', 'Чехов', 'achehov@hotmail.com', '+7 (495) 456-78-90')
        # add_client(conn, 'Сергей', 'Есенин', 'sesenin@yandex.ru', '+7 (495) 567-89-01')
        # add_client(conn, 'Анна', 'Ахматова', 'aahmatova@mail.ru')
        # add_client(conn, 'Николай', 'Гоголь', 'ngogol@mail.ru', '+7 (495) 234-56-78')
        # add_client(conn, 'Иван', 'Тургенев', 'iturgenev@hotmail.com', '+7 (495) 901-23-45')
        # add_client(conn, 'Александр', 'Тургенев', 'iturgeev@hotmail.com', '+7 (495) 901-23-45')
        # add_client(conn, 'Иван', 'Гоголь', 'iturgenv@hotmail.com', '+7 (495) 901-23-45')
        # add_phone(conn, 3, '+7 (495) 123-45-67')
        # add_phone(conn, 2, '+7 (495) 567-89-08')
        # add_phone(conn, 4, '+7 (495) 567-29-66')
        # add_phone(conn, 6, '+7 (495) 567-69-12')
        # add_phone(conn, 7, '+7 (495) 567-81-97')
        # add_phone(conn, 1, '+7 (495) 587-17-00')
        # change_client(conn, 3, first_name=None, last_name=None, email_client=None, phone_client='+7 (495) 123-45-85')
        # change_client(conn, 4, first_name='Андрей', last_name=None, email_client='achehov@gmail.com',
        #               phone_client='+7 (495) 123-45-77')
        # delete_phone(conn, 2, '+7 (495) 234-56-78')
        # delete_client(conn, 3)
        find_client(conn, first_name=None, last_name=None, email_client=None,
                    phone_client='+7 (495) 567-69-12')
    conn.close()
