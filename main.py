from app import app

if __name__ == '__main__':
    try:
        from wsgiref.simple_server import make_server
        httpd = make_server('127.0.0.1', 8080, app)
        print('Serving on port 8080...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Goodbye.')
