from urllib.parse import parse_qsl

database_name = 'my.db'


def qs_parser(qs):
    result = {}
    for row in parse_qsl(qs):
        result[row[0]] = row[1]

    return result
