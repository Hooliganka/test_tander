import json
import re
import sqlite3
from config import database_name


def my_connect():
    connect = sqlite3.connect(database_name)
    cursor = connect.cursor()
    return cursor


def query(sql: str) -> list:
    def dict_factory(c, row):
        return {col[0]: row[idx] for idx, col in enumerate(c.description)}

    with sqlite3.connect(database_name) as connect:
        connect.row_factory = dict_factory
        cursor = connect.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

    return rows


def comment(request, *args, **kwargs):
    result = {
        '{{SUCCESS}}': '',
        '{{ERROR}}': '',
    }
    connect = sqlite3.connect(database_name)
    cursor = connect.cursor()

    # Проверки на валидность

    if request['GET']:
        result['{{ERROR}}'] = []
        if not request['GET'].get('name', ''):
            result['{{ERROR}}'].append('<li>Некорректно введено имя!</li>')

        if not request['GET'].get('last_name', ''):
            result['{{ERROR}}'].append('<li>Некорректно введена фамилия!</li>')

        if not request['GET'].get('comment', ''):
            result['{{ERROR}}'].append('<li>Некорректно введен комментарий!</li>')

        pattern_email = r'^[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}$'
        match = re.search(pattern_email, request['GET'].get('email', ''))
        if not match:
            result['{{ERROR}}'].append('<li>Некорректно введен email!</li>')

        pattern_telephone = r'^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$'
        match = re.search(pattern_telephone, request['GET'].get('telephone', ''))
        if not match:
            result['{{ERROR}}'].append('<li>Некорректно введен телефон!</li>')

        if result['{{ERROR}}']:
            temp = '<ul>'
            for error in result['{{ERROR}}']:
                temp = temp + error
            temp = temp + '</ul>'
            result['{{ERROR}}'] = temp
        else:
            result['{{ERROR}}'] = ''

            # Запись в базу

            query(
                "INSERT INTO 'comment' (`name`, `last_name`,`middle_name`,`region`, `city`, `email`, `telephone`,`comment`) "
                "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    request['GET'].get('name', ''),
                    request['GET']['last_name'],
                    request['GET']['middle_name'],
                    int(request['GET']['region']),
                    int(request['GET']['city']),
                    request['GET']['email'],
                    request['GET']['telephone'],
                    request['GET']['comment']
                )
            )
            result['{{SUCCESS}}'] = '<p>Данные успешно записаны!</p>'

    # Вывод региона

    rows = query("SELECT * FROM `regions`")
    pat = '<option value="{{region.id}}">{{region}}</option>'

    items = ''
    t = 0
    for row in rows:
        items = items + pat.replace('{{region}}', row['name']).replace('{{region.id}}', str(row['id']))
        t = t+1
    result['{{regions}}'] = items
    return result


def get_cities(request, *args, **kwargs):  # Получение городов по региону
    result = ''
    if request['POST']:
        rows = query("SELECT * FROM `city` WHERE `region`=%s" % request['POST'].get('city'))
        result = json.dumps(rows)
    print('result', result)
    return result