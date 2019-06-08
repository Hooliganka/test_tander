
def render(path, context) -> str:
    with open('templates/%s' % path, 'r', encoding='utf-8') as file:
        response = file.read()
        for key in context:
            response = response.replace(key, context[key])
    return response
