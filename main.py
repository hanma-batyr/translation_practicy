import sqlite3
from aiogoogletrans import Translator
import hashlib


def registration():
    '''Получение логина и пароля для дальнейшего добавления в базу данных'''
    login = input("Введите логин: ")
    password = input("Введите пароль: ")

    '''Подключение к базе данных'''
    conn = sqlite3.connect("Translator_program_base.db")
    cursor = conn.cursor()

    '''Проверка на отсуствие такого же(одинакового) логина'''
    cursor.execute("SELECT * FROM users WHERE login=?", (login,))
    existing_user = cursor.fetchone()

    '''Цикл добавления пользователя при уникальности логина'''
    '''Так же при добавление пользователя пароль будет хэширован'''
    if existing_user:
        print("Пользователь с таким логином уже существует.")
    else:
        # Хэшируем пароль пользователя с помощью hashlib
        # sha512 - Это количество символов который создасть библеотека hashlib
        # encode('utf-8') - преобразование в байтовую строку
        # hexdigest() - возвращает строку в шестнадцатеричном формате.
        hashlib_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
        # Добавляем нового пользователя
        cursor.execute("INSERT INTO users (login, password) VALUES (?, ?)",
                       (login, hashlib_password))
        print("Пользователь успешно зарегистрирован.")
        # сохраняем результат и закрываем базу данных
        conn.commit()
        conn.close()


def authenticate():
    '''Функция проверки и аутификацией пользователя учетом возможных ошибок'''
    try:
        '''Получаем данные для прооверки'''
        login = input("Введите логин: ")
        password = input("Введите пароль: ")

        '''Подключение к базе данных'''
        conn = sqlite3.connect("Translator_program_base.db")
        cursor = conn.cursor()

        '''Проверка на наличего логина в базе данных'''
        cursor.execute("SELECT * FROM users WHERE login=?", (login,))
        user = cursor.fetchone()

        '''Цикл аутификацией'''
        if user:
            # Получаем хэш пароля из базы данных
            hashed_password_db = user[2]
            # Хэшируем введенный пароль для сравнения
            h_password = hashlib.sha512(password.encode('utf-8')).hexdigest()

            # Сравниваем хэшированные символы для аутификацией
            if h_password == hashed_password_db:
                print("Вход выполнен успешно!")
                return True  # Возвращаем True, если аутентификация успешна
            else:
                print("Неправильный пароль.")
                return False  # Возвращаем False, если пароль неправильный
        else:
            print("Пользователя с таким логином не существует.")
            return False  # Возвращаем False, если пользователь не найден
        conn.close()
    except sqlite3.Error as e:
        print("Ошибка при работе с базой данных:", e)
        return False  # Возвращаем False в случае ошибки работы с базой данных
    except Exception as e:
        print("Произошла ошибка:", e)
        return False  # Возвращаем False в случае другой ошибки


def entrance_handler(entrance_choice: int):
    '''Простоя функция выбора между регистрацией и аутентификацией'''
    if entrance_choice == 1:
        registration()
    elif entrance_choice == 2:
        authenticated = False
        while not authenticated:
            authenticated = authenticate()
            if authenticated:
                print("Вход выполнен успешно!")
            else:
                print("Неправильно. Пожалуйста, попробуйте еще раз.")
    else:
        print("Неправильный выбор. Пожалуйста, выберите 1 или 2.")


async def translate():
    '''Основная функция приложения для перевода текста на любой язык'''
    translator = Translator()
    s_lang = input("Введите язык (например, 'ru' для русского): ")
    d_lang = input("Язык перевода (например, 'en' для английского): ")

    while True:
        # Запрос ввода текста у пользователя
        text = input("Введите текст для перевода: ")

        # Перевод текста
        result = await translator.translate(text, src=s_lang, dest=d_lang)

        # Вывод перевода
        print(f"Перевод текста: {result.text}")

        # Запрос на действие пользователя
        print("1. Вывод текущих языков")
        print("2. Заново перевести текст")
        print("3. Сменить языки местами и перевести текст")
        print("4. Сохранить историю")
        print("5. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            print(f"Текущая пара языков: {s_lang} -> {d_lang}")
        elif choice == '2':
            continue
        elif choice == '3':
            # Смена языков местами и перевод текста
            s_lang, d_lang = d_lang, s_lang
            result = await translator.translate(text, src=s_lang, dest=d_lang)
            print(f"Языки местами: {s_lang} -> {d_lang}")
            print(f"Перевод текста: {result.text}")
        elif choice == '4':
            conn = sqlite3.connect("Translator_program_base.db")
            cursor = conn.cursor()

            # Вставляем запись в таблицу search_history
            cursor.execute('''INSERT INTO search_history (login,
                            input_history, withdrawal_history)
                            VALUES (?, ?, ?)''', ("", text, result.text))
            # Подтверждаем изменения
            conn.commit()
            print("История поиска сохранена.")
        elif choice == '5':
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите действие из списка.")
            continue


def display_history():
    '''Функция для получение историй пользователя'''
    # Подключение к базам данных
    conn = sqlite3.connect("Translator_program_base.db")
    cursor = conn.cursor()

    # Получение элементов
    cursor.execute("SELECT * FROM search_history")
    history_win = cursor.fetchall()

    # Вывод результата
    for el in history_win:
        print(el)

    # Закрытие базы данных
    conn.close()


async def dictionary():
    # Бесконечный цикл для повторения операций
    while True:
        # Подключения к нашим базам данным и библеотекам
        translator = Translator()
        conn = sqlite3.connect("Translator_program_base.db")
        cursor = conn.cursor()

        '''Меню взаймодействия с пользователем'''
        print("Что вы хотите?")
        print("1. Добавить слова")
        print("2. Посмотреть слова")
        print("3. Проверить знания")
        print("4. Вернуться в главное меню")
        chouse = int(input(""))

        if chouse == 1:
            '''Переводчик с опцией сохранения слов на базе aiogoogletrans'''
            work = input("Введите слово для перевода: ")
            # Выбор начального языка
            s_lang = input("Введите язык (например, 'ru' для русского): ")
            # Выбор языка на который нужен перевод
            d_lang = input("Язык перевода (например, 'en' для английского): ")
            # Функция для перевода
            result = await translator.translate(work, src=s_lang, dest=d_lang)
            # Вывод результата перевода
            print(f"Перевод текста: {result.text}")
            # Сохрание изначального слово и перевода этого слово
            cursor.execute('''INSERT INTO dictionary (work, translation)
                              VALUES (?, ?)''', (work, result.text))
            # Сохранение изменений в базе данных
            conn.commit()

        elif chouse == 2:
            '''Функция просмотра слов в базе данных в виде картежа'''
            cursor.execute("SELECT * FROM dictionary")
            works = cursor.fetchall()
            for el in works:
                print(el)

        elif chouse == 3:
            '''Функция ТЕСТ которое дает возможность проверить знания слов'''
            # подключаемся к таблице dictionary
            cursor.execute("SELECT work, translation FROM dictionary")
            # получаем данные из таблицы
            row = cursor.fetchone()
            if not row:
                print("В базе данных нет слов для проверки.")
            else:
                while row:
                    # Получение значения из первого столбца
                    work = row[0]
                    # Получение значения из столбца (translation-перевод)
                    translation = row[1]
                    # Вывод значения на экран
                    print(work)
                    # Получение ответа пользователя
                    # используем upper чтобы избежать ошибок с регистором
                    test = input("Введите перевод: ").strip().upper()

                    # цикл если был введен пустое значение
                    while not test:
                        print("Введите перевод пожалуйста.")
                        test = input("Введите перевод: ").strip().upper()
                    # casefold для сравнения без учета регистра.
                    if test.casefold() == translation.casefold():
                        print("Верно!")
                    else:
                        print("Неверно.")
                        print("Правильный перевод:", translation)
                    row = cursor.fetchone()

        elif chouse == 4:  # Опция для возврата в главное меню
            break  # Выход в главное меню. Недоделан

        conn.close()
