import sqlite3
import os


def my_bd(database_name):
    if not os.path.exists(database_name):
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        # Создание таблицы
        c.execute('''CREATE TABLE IF NOT EXISTS `regions` (`id` INTEGER PRIMARY KEY AUTOINCREMENT,`name` VARCHAR)''')
        # Создание таблицы
        c.execute(
            '''CREATE TABLE IF NOT EXISTS `city` (`id` INTEGER PRIMARY KEY AUTOINCREMENT,`name` VARCHAR, `region` INTEGER NOT NULL )''')

        c.execute('''CREATE TABLE IF NOT EXISTS `comment` (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            `name` VARCHAR, 
                                                            `last_name` VARCHAR,
                                                            `middle_name` VARCHAR,
                                                            `region` INTEGER,
                                                            `city` INTEGER,
                                                            `email` VARCHAR,
                                                            `telephone` VARCHAR,
                                                            `comment` VARCHAR
                                                             )''')
        # Наполнение таблицы
        c.execute("INSERT INTO `regions` (`name`) "
                  "VALUES ('Краснодарский край'),"
                  "('Ростовская область'),"
                  "('Ставропольский край')")
        # Наполнение таблицы
        c.execute("INSERT INTO 'city' (`name`, `region`) "
                  "VALUES"
                  "('Краснодар', 1),"
                  "('Кропоткин', 1),"
                  "('Славянск', 1),"
                  "('Ростов', 2),"
                  "('Шахты', 2),"
                  "('Батайск', 2),"
                  "('Ставрополь', 3),"
                  "('Пятигорск', 3),"
                  "('Кисловодск', 3)")
        # Подтверждение отправки данных в базу
        conn.commit()
        # Завершение соединения
        c.close()
        conn.close()


