# -*- coding: utf-8 -*-
"""
    test_require_json
    ~~~~~~~~~~~~~~~

    Test for the require_json_decorator
    
"""
from flask import Flask
from tests.base import AppBase

from webapp.lib import api

app = Flask(__name__)

@app.route('/test0', methods=['POST'])
@api.json_required({'number': int, 'string': str})
def fn0():
    return api.api_success()

@app.route('/test1', methods=['POST'])
@api.json_required(optional_fields={'number': int, 'string': str})
def fn1():
    return api.api_success()


@app.route('/test2', methods=['POST'])
@api.json_required(required_fields={'weight': float}, optional_fields={'number': int, 'string': str})
def fn2():
    return api.api_success()

app.errorhandler(Exception)(api.error_handler)


class TestRequireJson(AppBase):

    selected_app = app

    def test_decorator(self):

        self.post('/test0', expect_error='invalid_body')

        self.post('/test0', data_json={'bla': '123'}, expect_error='invalid_parameters')

        # valid requests url 0
        self.post('/test0', data_json={'number': 1, 'string': 'yay'})
        self.post('/test0', data_json={'number': 1, 'string': 'yay', 'extra': 'woo'})

        # invalid parameter type
        self.post('/test0', data_json={'number': 'not a number', 'string': 'yay'}, expect_error='invalid_parameters')
        self.post('/test0', data_json={'number': 123, 'string': 444}, expect_error='invalid_parameters')

        #valid request url 1
        self.post('/test1', data_json={'extra': ''})
        self.post('/test1', data_json={'number': 1, 'string': 'yay'})

         # invalid parameter type
        self.post('/test1', data_json={'number': 'not a number', 'string': 'yay'}, expect_error='invalid_parameters')
        self.post('/test1', data_json={'number': 123, 'string': 444}, expect_error='invalid_parameters')

        # valid request url2
        self.post('/test2', data_json={'weight': 1})
        self.post('/test2', data_json={'weight': 1.2})
        self.post('/test2', data_json={'weight': 1.2, 'number': 1})
        self.post('/test2', data_json={'weight': 1.2, 'number': 1, 'string': ''})
        self.post('/test2', data_json={'weight': 0, 'number': 0, 'string': ''})

        # invalid optional field
        self.post('/test0', data_json={'weight': 1.2, 'number': 123, 'string': 444}, expect_error='invalid_parameters')
