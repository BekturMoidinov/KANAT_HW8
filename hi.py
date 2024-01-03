import sqlite3


def create_connection(db_name):
    connection = None
    try:
        connection = sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print(e)
    return connection


def create_table(connection, sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except sqlite3.Error as e:
        print(e)


sql_create_countries_table = '''
CREATE TABLE countries (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL
)'''


def insert_country(connection, country):
    sql = '''INSERT INTO countries (title) VALUES (?)'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, country)
        connection.commit()
    except sqlite3.Error as e:
        print(e)


sql_create_cities_table = '''
CREATE TABLE cities (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
area FLOAT DEFAULT 0,
country_id INTEGER REFERENCES countries(id) ON DELETE NO ACTION 
)'''


def insert_city(connection, city):
    sql = '''INSERT INTO cities (title, area, country_id) VALUES (?, ?, ?)'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, city)
        connection.commit()
    except sqlite3.Error as e:
        print(e)


sql_create_students_table = '''
CREATE TABLE students (
id INTEGER PRIMARY KEY AUTOINCREMENT,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
city_id INTEGER REFERENCES cities(id) ON DELETE NO ACTION
)'''


def insert_students(connection, name):
    sql = '''INSERT INTO students (first_name, last_name, city_id)
    VALUES (?, ?, ?)'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, name)
        connection.commit()
    except sqlite3.Error as e:
        print(e)


countries_list = ["Kyrgyzstan", "Turkey", "USA"]
cities_list = [('Bishkek', 3.2, 1), ('Osh', 2.7, 1), ('Moscow', 8.7, 2), ('Berlin', 2.5, 2),
                   ('Florida', 5.9, 2), ('London', 4.9, 3), ('Tokyo', 3.8, 3)]
students_list = [("Kanat", "Attokurov", 1), ("Atay", "Beshekeev", 2), ("Alina", "Mbekova", 3), ("Mirbek", "Mercedes", 4),
                     ("Alisher", "Nayzabekov", 5), ("Adil", "Alimbekov", 6), ("Erbol", "Nasirdinov", 7),
                     ("Aman", "Gaynazarov", 1), ("Bektur", "Mzayev", 2), ("Ivan", "Mashkin", 3), ("Egor", "Bajenov", 4),
                     ("Artur", "Arturov", 5), ("Vlad", "Morozov", 6), ("Vadim", "Morozov", 7), ("Danil", "Alekseyev", 1)]


my_connection = create_connection('new10_countries.db')
if my_connection is not None:
    print("Connection established")
    # create_table(my_connection, sql_create_countries_table)
    # for i in countries_list:
    #     # insert_country(my_connection, (i, ))
    # create_table(my_connection, sql_create_cities_table)
    # for i in cities_list:
    #     i = tuple(i)
    #     # insert_city(my_connection, (i))
    # create_table(my_connection, sql_create_students_table)
    # for i in students_list:
    #     i = tuple(i)
    #     # insert_students(my_connection, i)


def show_students(connection, city_id):
    sql = '''SELECT st.first_name, st.last_name,
        (SELECT co.title FROM countries AS co WHERE co.id = (SELECT country_id FROM cities WHERE id = st.city_id)),
        (SELECT ci.title FROM cities AS ci WHERE ci.id = st.city_id),
        (SELECT ci.area FROM cities AS ci WHERE ci.id = st.city_id)
    FROM students AS st
    WHERE st.city_id IN (SELECT id FROM cities WHERE id = ?)'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (city_id, ))
        rows_list = cursor.fetchall()
        sql = '''SELECT title FROM cities WHERE id = ?'''
        cursor.execute(sql, (city_id,))
        city = cursor.fetchall()
        print("Полный список студентов в городе " + city[0])
        for row in rows_list:
            print(f" {row[0]}, Фамилия: {row[1]}, Страна: {row[2]}, Город: {row[3]}, Площадь: {row[4]}")
    except Exception as e:
        print(e)


def show_cities(connection):
    sql = '''SELECT * FROM cities'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        rows_list = cursor.fetchall()
        return rows_list
    except Exception as e:
        print(e)


try:
    cities = show_cities(my_connection)
    city_id = input('Выбери id города по списке ниже, для вывода студентов(0 выдаст выход):'
                    f'\n{", ".join([f"{i[0]}. {i[1]}" for i in cities])}'
                    f'\nID города:')
    if city_id == '0':
        print('Вы вышли из запроса')
    else:
        show_students(my_connection, city_id)
except:
    print('Неверный ответ!')