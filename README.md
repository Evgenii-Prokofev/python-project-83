### Hexlet tests and linter status:
[![Actions Status](https://github.com/Evgenii-Prokofev/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Evgenii-Prokofev/python-project-83/actions)
### Result of the Render deploy:
https://python-project-83-nul4.onrender.com/

**"Page Analyzer"** - это сайт, который анализирует указанные страницы на SEO-пригодность.

### Установка:
Для установки и запуска проекта вам потребуется Python версии 3.10 и выше, 
инструмент для управления зависимостями Poetry и база данных PostgreSQL.

**Для установки выполните следующие шаги:**

1. Склонируйте репозиторий с проектом на ваше локальное устройство: 
git clone git@github.com:Evgenii-Prokofev/python-project-83.git
2. Перейдите в директорию проекта: cd python-project-50
3. Установите необходимые зависимости с помощью Poetry: poetry install
4. Создайте файл .env, который будет содержать ваши конфиденциальные настройки
5. Задайте в нём значение ключей SECRET_KEY и DATABASE_URL
6. Запустите команды из database.sql в SQL-консоли вашей базы данных, 
чтобы создать необходимые таблицы.

**Запуск:**

1. Выполните команду *make build*
2. Выполните команду *make start* или *make dev*
3. Пользуйтесь на здоровье!!! 
