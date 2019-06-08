import json
import re
import sqlite3
from config import database_name


def query(sql: str) -> list:
    def dict_factory(c, row):
        return {col[0]: row[idx] for idx, col in enumerate(c.description)}

    with sqlite3.connect(database_name) as connect:
        connect.row_factory = dict_factory
        cursor = connect.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

    return rows


def comment(request, *args, **kwargs):  # Добавление комментария
    result = {
        '{{SUCCESS}}': '',
        '{{ERROR}}': '',
    }

    # Проверки на валидность

    if request.get('POST'):
        result['{{ERROR}}'] = []
        if not request['POST'].get('name', ''):
            result['{{ERROR}}'].append('<li>Некорректно введено имя!</li>')

        if not request['POST'].get('last_name', ''):
            result['{{ERROR}}'].append('<li>Некорректно введена фамилия!</li>')

        if not request['POST'].get('comment', ''):
            result['{{ERROR}}'].append('<li>Некорректно введен комментарий!</li>')

        pattern_email = r'^[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}$'
        match = re.search(pattern_email, request['POST'].get('email', ''))
        if not match:
            result['{{ERROR}}'].append('<li>Некорректно введен email!</li>')

        pattern_telephone = r'^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$'
        match = re.search(pattern_telephone, request['POST'].get('telephone', ''))
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
                    request['POST'].get('name', ''),
                    request['POST']['last_name'],
                    request['POST']['middle_name'],
                    int(request['POST']['region']),
                    int(request['POST']['city']),
                    request['POST']['email'],
                    request['POST']['telephone'],
                    request['POST']['comment']
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
        t = t + 1
    result['{{regions}}'] = items

    return result


def get_cities(request, *args, **kwargs):  # Получение городов по региону
    rows = []
    if request['POST']:
        rows = query("SELECT * FROM `city` WHERE `region`=%s" % request['POST'].get('city', 0))
    return json.dumps(rows)


def view(request, *args, **kwargs):  # вывод всех комментов
    rows = query("""SELECT `comment`.id AS id,
                          `comment`.name,
                          `last_name`,
                          `middle_name`,
                          regions.name AS region,
                          city.name AS city,
                          `email`,
                          `telephone`,
                          `comment`
                        FROM
                          comment
                        INNER JOIN regions ON comment.region=regions.id
                        INNER JOIN city ON comment.city=city.id""")

    patt = '<tr><td>{{id}}</td><td>{{name}}</td><td>{{last_name}}</td><td>{{middle_name}}</td><td>{{region}}</td><td>{{' \
           'city}}</td><td>{{email}}</td><td>{{telephone}}</td><td>{{comment}}</td><td class="del" dat="{{id}}" ' \
           'style="cursor: pointer">Х</td></tr>'

    items = ''

    for row in rows:
        items = items + patt.replace('{{id}}', str(row['id'])).replace('{{name}}', row['name']).replace('{{last_name}}',
                                                                                                        row[
                                                                                                            'last_name']) \
            .replace('{{middle_name}}', row['middle_name']).replace('{{region}}', str(row['region'])).replace(
            '{{city}}', str(row['city'])) \
            .replace('{{email}}', row['email']).replace('{{telephone}}', row['telephone']).replace('{{comment}}', row[
            'comment']).replace(
            '{{id}}', str(row['id']))

    return {
        '{{comments}}': items,
    }


def del_comment(request, *args, **kwargs):
    result = {
        'STATE': 'ERROR',
    }
    if request['POST']:
        query("DELETE FROM `comment` WHERE `id`=%s" % request['POST'].get('comment_id'))
        result['STATE'] = 'OK'
    return json.dumps(result)


def stat(request, *args, **kwargs):
    rows = query("""SELECT regions.id, name, comments_count
                        FROM regions,
                            (SELECT region, COUNT(region) AS comments_count
                           FROM comment
                           GROUP BY region
                          )regs
                        WHERE id=region AND comments_count>5""")
    patt = '<tr><td>{{id}}</td><td><a href="/stat/{{id}}/">{{name}}</a></td><td>{{comments_count}}</td></tr>'
    items = ''
    for row in rows:
        items = items + patt.replace('{{id}}', str(row['id'])).replace('{{name}}', row['name']).replace(
            '{{comments_count}}',
            str(row['comments_count']))
    return {
        '{{regions}}': items,
    }


def stat_city(request, *args, **kwargs):
    kwargs['region'] = query("SELECT name FROM regions WHERE id=%s" % kwargs['id'])

    rows = query('''SELECT city.id, city.name , COUNT(*) AS comments_count
                    FROM comment, (SELECT id, name FROM city WHERE region=%s)city
                    WHERE region=%s AND city=city.id GROUP BY city.id''' % (kwargs['id'], kwargs['id']))
    patt = '<tr><td>{{id}}</td><td>{{name}}</td><td>{{comments_count}}</td></tr>'

    items = ''
    for row in rows:
        items = items + patt.replace('{{id}}', str(row['id'])).replace('{{name}}', row['name']).replace(
            '{{comments_count}}',
            str(row['comments_count']))
    return {
        '{{sities}}': items,
    }
