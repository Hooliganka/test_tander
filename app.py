import re
import copy
from basebd import my_bd
from url import patterns


def app(request, start_response, *args, **kwargs):

    # Костыль чтобы работали нормально тесты
    from config import database_name, qs_parser
    my_bd(database_name)
    request.update({'database_name': database_name})

    response = ''
    start_response('200 OK', [('Content-Type', 'text/html')])
    for url in patterns:
        match = re.search(url[0], request['PATH_INFO'])
        if match:
            kwargs = copy.deepcopy(match.groupdict())
            if request['REQUEST_METHOD'] == 'GET':
                request['GET'] = qs_parser(request['QUERY_STRING'])
                if url[1]:
                    response = url[1](request, *args, **kwargs)

            elif request['REQUEST_METHOD'] == 'POST':
                request['POST'] = qs_parser(request['wsgi.input'].read(
                    int(request.get('CONTENT_LENGTH', 0))).decode())

                response = url[1](request, *args, **kwargs)

    return [response.encode()]
