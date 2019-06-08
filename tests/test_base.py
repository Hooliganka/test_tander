import os
import unittest
import requests
import threading

import config
from app import app


def runserver(name_test_database, ip, port):
    from wsgiref.simple_server import make_server
    config.database_name = name_test_database
    httpd = make_server(ip, port, app)
    httpd.serve_forever()


class TestMyApp(unittest.TestCase):
    name_test_database = None
    port = 8080
    ip = '127.0.0.1'
    host = f'http://{ip}:{port}'

    @classmethod
    def setUpClass(cls) -> None:
        try:
            os.remove(cls.name_test_database)
        except:
            pass

        cls.name_test_database = 'test.db'
        cls.tread = threading.Thread(target=runserver, daemon=True, args=(cls.name_test_database, cls.ip, cls.port))
        cls.tread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(cls.name_test_database)

    def testIsRunServer(self):
        r = requests.get(self.host)
        self.assertEqual(r.status_code, 200)

    def testAllUrls(self):
        urls = {
            '/comment/',
            '/view/',
            '/stat/',
        }

        for url in urls:
            r = requests.get(f'{self.host}{url}')
            self.assertEqual(r.status_code, 200)

    def testGetCites(self):
        r = requests.post(f'{self.host}/api/get_cities/')
        self.assertEqual(r.status_code, 200)

        r = requests.post(f'{self.host}/api/get_cities/', data=dict(
            region=1,
        ))
        self.assertEqual(r.status_code, 200)

    def testDeleteComment(self):
        r = requests.post(f'{self.host}/api/delete_comment/')
        self.assertEqual(r.status_code, 200)

        r = requests.post(f'{self.host}/api/delete_comment/', data=dict(
            comment_id=1,
        ))
        self.assertEqual(r.status_code, 200)

    @property
    def region_id(self):
        return 1

    @property
    def city_id(self):
        return 1

    def testStatistic(self):
        r = requests.get(f'{self.host}/stat/{self.region_id}/')
        self.assertEqual(r.status_code, 200)

    def testAddComment(self):
        r = requests.post(f'{self.host}/comment/', data=dict(
            name='name',
            last_name='last_name',
            middle_name='middle_name',
            region=self.region_id,
            city=self.city_id,
            comment='comment',
            email='email@email.ru',
            telephone='+7(111)321-12-12',
        ))
        self.assertEqual(r.status_code, 200)

    def testErrorAddComment(self):
        r = requests.post(f'{self.host}/comment/', data=dict(
            name='name',
        ))
        self.assertEqual(r.status_code, 200)
        self.assertTrue('Некорректно' in r.content.decode('utf-8'))
