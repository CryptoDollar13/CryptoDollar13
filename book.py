import sys
import sqlite3

DB_FILE = 'polyprofi.db'  # Файл базы данных

def create_connection():
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except sqlite3.Error as e:
        print("Ошибка при подключении к базе данных:", e)
        sys.exit()

def create_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            description TEXT,
            genre_id INTEGER,
            FOREIGN KEY (genre_id) REFERENCES genres(id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        ''')

        conn.commit()
        cursor.close()
    except sqlite3.Error as e:
        print("Ошибка при создании таблиц базы данных:", e)
        conn.close()
        sys.exit()

def add_book(conn, title, author, description, genre):
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO genres (name) VALUES (?)', (genre,))
        genre_id = cursor.lastrowid
        cursor.execute('INSERT INTO books (title, author, description, genre_id) VALUES (?, ?, ?, ?)', (title, author, description, genre_id))
        conn.commit()
        cursor.close()
        print("Книга добавлена успешно!")
    except sqlite3.Error as e:
        print("Ошибка при добавлении книги:", e)

def view_books(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT b.title, b.author FROM books AS b')
        books = cursor.fetchall()
        for book in books:
            print("Название:", book[0])
            print("Автор:", book[1])
            print("----------")
        if len(books) < 1:
            print("На данный момент книг в базе нет.")
        cursor.close()
    except sqlite3.Error as e:
        print("Ошибка при просмотре книг:", e)

def view_books_by_genre(conn, genre):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT b.title, b.author FROM books AS b, genres AS g WHERE b.genre_id = g.id AND g.name = ?', (genre,))
        books = cursor.fetchall()
        for book in books:
            print("Название:", book[0])
            print("Автор:", book[1])
            print("----------")
        if len(books) < 1:
            print("На данный момент книг в данном жанре нет.")
        cursor.close()
    except sqlite3.Error as e:
        print("Ошибка при просмотре книг по жанру:", e)

def search_books(conn, keyword):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT title, author FROM books WHERE title LIKE ? OR author LIKE ?', ('%'+keyword+'%', '%'+keyword+'%'))
        books = cursor.fetchall()
        for book in books:
            print("Название:", book[0])
            print("Автор:", book[1])
            print("----------")
        if len(books) < 1:
            print("По вашему запросу не найдено книг.")
        cursor.close()
    except sqlite3.Error as e:
        print("Ошибка при поиске книги:", e)

def delete_book(conn, title):
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE title = ?', (title,))
        conn.commit()
        cursor.close()
        print("Книга удалена успешно!")
    except sqlite3.Error as e:
        print("Ошибка при удалении книги:", e)

def main():
    conn = create_connection()
    create_tables(conn)

    while True:
        print("""
        Выберите действие:
        1. Добавить книгу
        2. Просмотреть все книги
        3. Просмотреть книги по жанру
        
        4. Поиск книги
        5. Удалить книгу
        6. Выйти из программы
        """)

        choice = input("Введите номер действия: ")

        if choice == "1":
            try:
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                description = input("Введите описание книги: ")
                genre = input("Введите жанр книги: ")
                add_book(conn, title, author, description, genre)
            except KeyboardInterrupt:
                print("\nОтменено.")
        elif choice == "2":
            view_books(conn)
        elif choice == "3":
            try:
                genre = input("Введите жанр книги: ")
                view_books_by_genre(conn, genre)
            except KeyboardInterrupt:
                print("\nОтменено.")
        elif choice == "4":
            try:
                keyword = input("Введите ключевое слово для поиска: ")
                search_books(conn, keyword)
            except KeyboardInterrupt:
                print("\nОтменено.")
        elif choice == "5":
            try:
                title = input("Введите название книги для удаления: ")
                delete_book(conn, title)
            except KeyboardInterrupt:
                print("\nОтменено.")
        elif choice == "6":
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор. Попробуйте еще раз.")

    conn.close()

if __name__ == '__main__':
    main()
