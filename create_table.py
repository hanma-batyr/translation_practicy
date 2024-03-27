import sqlite3

'''Создание подключения к базе данных'''
conn = sqlite3.connect("Translator_program_base.db")
cursor = conn.cursor()

'''Создание таблицы users'''
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    login TEXT,
    password TEXT
)''')

'''Создание таблицы search_history'''
cursor.execute('''CREATE TABLE IF NOT EXISTS search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL,
    input_history TEXT NOT NULL,
    withdrawal_history TEXT NOT NULL
)''')

'''Создание таблицы dictionary'''
cursor.execute('''CREATE TABLE IF NOT EXISTS dictionary (
    work TEXT NOT NULL,
    translation TEXT NOT NULL
)''')
