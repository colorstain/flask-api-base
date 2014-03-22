# -*- coding: utf-8 -*-
"""
    test_libs
    ~~~~~~~~~~~~~~~

    Libs module tests

"""
from nose.tools import *

from flask import Flask, json
from webapp.exceptions import AppBaseException

from webapp.lib import utils
from webapp.lib import api

app = Flask(__name__)


def test_camel_case_to_underscore():
    eq_(utils.camel_case_to_underscore('TestOne'), 'test_one')
    eq_(utils.camel_case_to_underscore('AnotherOne'), 'another_one')
    eq_(utils.camel_case_to_underscore('MoreComplicatedExpression'), 'more_complicated_expression')


def test_api_success_data_description():
    with app.test_request_context():
        description = 'test description'
        r = api.api_success({'data': 'test'}, description)
        eq_(r.status_code, 200)
        eq_(r.mimetype, 'application/json')
        ok_(r.data)

        # checking response
        response = json.loads(r.data)
        assert_in('data', response)
        eq_(response['data'], 'test')
        eq_(response['description'], description)


def test_api_success_no_data_no_description():
    with app.test_request_context():
        r = api.api_success()
        eq_(r.status_code, 200)
        eq_(r.mimetype, 'application/json')
        ok_(r.data)

        # checking response
        response = json.loads(r.data)
        assert_not_in('description', response)
        ok_(response['success'])


def test_api_success_data_no_description():
    with app.test_request_context():
        that = [1, 2, 3]
        r = api.api_success({'this': that})
        eq_(r.status_code, 200)
        eq_(r.mimetype, 'application/json')
        ok_(r.data)

        # checking response
        response = json.loads(r.data)
        assert_not_in('description', response)
        ok_(response['success'])
        eq_(response['this'], that)


def test_api_error():
    with app.test_request_context():
        error = 'super_error'
        description = 'this is my description'
        r, status_code = api.api_error(error, description)
        eq_(status_code, 500)
        eq_(r.mimetype, 'application/json')
        ok_(r.data)

        # checking response
        response = json.loads(r.data)
        assert_false(response['success'])
        eq_(response['description'], description)
        eq_(response['error'], error)


def test_api_error_extra_info():
    with app.test_request_context():
        error = 'other_error'
        description = 'cool'
        extra_info = {'blame': 'not me'}
        error_code = 400
        r, status_code = api.api_error(error, description, extra_info, error_code)
        eq_(status_code, error_code)
        eq_(r.mimetype, 'application/json')
        ok_(r.data)

        # checking response
        response = json.loads(r.data)
        assert_false(response['success'])
        eq_(response['description'], description)
        eq_(response['error'], error)
        eq_(response['blame'], extra_info['blame'])


def test_error_handler_app_exception():

    class InvalidParametersException(AppBaseException):
        pass

    with app.test_request_context():
        msg = 'missing stuff'
        error = InvalidParametersException(msg)
        r, status_code = api.error_handler(error)
        eq_(status_code, 400)
        eq_(r.mimetype, 'application/json')
        ok_(r.data)

        # checking response
        response = json.loads(r.data)
        assert_false(response['success'])
        eq_(response['description'], msg)
        eq_(response['error'], 'invalid_parameters')


def test_error_unexpected_exception():
    with app.test_request_context():
        msg = 'missing stuff'
        error = Exception(msg)
        r, status_code = api.error_handler(error)
        eq_(status_code, 500)
        eq_(r.mimetype, 'application/json')
        ok_(r.data)

        # checking response
        response = json.loads(r.data)
        assert_false(response['success'])
        eq_(response['error'], 'unexpected_exception')


def test_error_unexpected_exception_testing():
    test_app = Flask(__name__)
    test_app.testing = True
    with test_app.test_request_context():
        msg = 'missing stuff'
        error = Exception(msg)
        with assert_raises(Exception):
            api.error_handler(error)


def test_error_unexpected_exception_debug():
    test_app = Flask(__name__)
    test_app.debug = True
    with test_app.test_request_context():
        msg = 'missing stuff'
        error = Exception(msg)
        r, status_code = api.error_handler(error)
        eq_(status_code, 500)
        eq_(r.mimetype, 'application/json')
        ok_(r.data)

        # checking response
        response = json.loads(r.data)
        assert_false(response['success'])
        eq_(response['error'], 'unexpected_exception')
        assert_in('tb', response)