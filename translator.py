import asyncio
import main


async def main_async():
    print("Выберите действие: ")
    print("1. Зарегистрироваться")
    print("2. Аутентификация")
    one = int(input())
    main.entrance_handler(one)

    print("Выберите следующее действие")
    print("1. Переводчик")
    print("2. История переводов")
    print("3. Словарь")
    two = int(input())

    if two == 1:
        await main.translate()
    elif two == 2:
        main.display_history()
    elif two == 3:
        await main.dictionary()

# Запуск асинхронного кода
asyncio.run(main_async())
