import sqlite3
import re
import sys
from typing import Callable

def connect_to_database() -> sqlite3.Connection:
    """
    Подключение к базе данных SQLite.
    """
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Создание таблицы в базе данных, если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS books
                     (title TEXT, author TEXT, year TEXT, genre TEXT)''')
    conn.commit()

    return conn

def add_book(conn: sqlite3.Connection, title: str, author: str, year: str, genre: str):
    """
    Добавление новой книги в библиотеку.
    """
    # Проверка на безопасность переданных данных
    if not all(re.match(r'^[a-zA-Z0-9\s]+$', data) for data in (title, author, year, genre)):
        print("Некорректные данные. Попробуйте снова.")
        return
    
    # Добавление новой книги в базу данных
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books VALUES (?, ?, ?, ?)", (title, author, year, genre))
    conn.commit()
    print("Книга успешно добавлена в библиотеку.")

def search_books(conn: sqlite3.Connection, title: str):
    """
    Поиск книги по названию.
    """
    # Проверка на безопасность переданного названия книги
    if not re.match(r'^[a-zA-Z0-9\s]+$', title):
        print("Некорректное название книги. Попробуйте снова.")
        return

    # Поиск книги в базе данных
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title=?", (title,))
    books = cursor.fetchall()

    if len(books) == 0:
        print(f"Книга с названием '{title}' не найдена.")
    else:
        print(f"Найдены книги с названием '{title}':")
        for book in books:
            print(f"Название: {book[0]}, Автор: {book[1]}, Год: {book[2]}, Жанр: {book[3]}")

def delete_book(conn: sqlite3.Connection, title: str):
    """
    Удаление книги из библиотеки по названию.
    """
    # Проверка на безопасность переданного названия книги
    if not re.match(r'^[a-zA-Z0-9\s]+$', title):
        print("Некорректное название книги. Попробуйте снова.")
        return

    # Удаление книги из базы данных
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE title=?", (title,))
    conn.commit()
    print(f"Книга с названием '{title}' успешно удалена из библиотеки.")

def display_books(conn: sqlite3.Connection):
    """
    Выводит список всех книг в библиотеке.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    if not books:
        print("Библиотека пуста.")
    else:
        print("Список книг в библиотеке:")
        for book in books:
            print(f"Название: {book[0]}, Автор: {book[1]}, Год: {book[2]}, Жанр: {book[3]}")

def exit_program(conn: sqlite3.Connection):
    """
    Выход из программы и закрытие подключения к базе данных.
    """
    print("Выход из программы.")
    # Закрытие подключения к базе данных SQLite
    conn.close()
    sys.exit()

def main():
    """
    Осуществление взаимодействия с пользователем и управление программой.
    """
    conn = connect_to_database()

    def add():
        add_book(conn, input("Введите название книги: "),
                 input("Введите автора книги: "),
                 input("Введите год публикации книги: "),
                 input("Введите жанр книги: "))

    def search():
        search_books(conn, input("Введите название книги для поиска: "))

    def delete():
        delete_book(conn, input("Введите название книги для удаления: "))

    def display():
        display_books(conn)

    def exit_program():
        exit_program(conn)

    options = {
        '1': add,
        '2': search,
        '3': delete,
        '4': display,
        '5': exit_program
    }

    while True:
        print("1. Добавить книгу")
        print("2. Поиск книги")
        print("3. Удалить книгу")
        print("4. Просмотреть список книг")
        print("5. Выход")
        choice = input("Введите ваш выбор: ")

        func = options.get(choice)
        if func:
            func()
            input("Нажмите Enter для продолжения...")
            print("\n" * 100)  # Очистка консоли
        else:
            print("Неправильный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
