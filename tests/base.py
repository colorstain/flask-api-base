# -*- coding: utf-8 -*-
"""
    test_base
    ~~~~~~~~~~~~~~~

    Base class for api based web apps
    
"""
from nose.tools import *
from flask import json
from werkzeug.utils import cached_property


class AppBase(object):

    response_decode = True
    response_check = True
    base_url = ''
    selected_app = None

    @classmethod
    def setup_class(cls):
        if cls.selected_app:
            cls._app = cls.selected_app
        else:
            from webapp.app import app as configured_app
            cls._app = configured_app

    @cached_property
    def app(self):
        return self._app


    @cached_property
    def client(self):
        return self.app.test_client()

    def get(self, path, expect_error=None, **params):
        """
        Performs HTTP `GET` in selected path

        :param path:  path
        :param params: kwargs that gets added to the querystring of the request
        :return: json decoded data from the response if json_decoded is set to true, otherwise the raw data
        """
        return self._do_request('get', path, query_string=params, expect_error=expect_error)

    def post(self, path, expect_error=None, **params):
        """
        Performs HTTP `POST` in selected path

        raw data should be sent using data_raw=data
        json encoded data should be sent data_json=data

        :param path:  path
        :param params: kwargs that gets added to the querystring of the request
        :return: json decoded data from the response if json_decoded is set to true, otherwise the raw data
        """
        return self._do_submit('post', path, expect_error=expect_error, **params)

    def put(self, path, expect_error=None,  **params):
        """
        Performs HTTP `PUT` in selected path

        raw data should be sent using data_raw=data
        json encoded data should be sent data_json=data

        :param path:  path
        :param params: kwargs that gets added to the querystring of the request
        :return: json decoded data from the response if json_decoded is set to true, otherwise the raw data
        """
        return self._do_submit('put', path, expect_error=expect_error, **params)

    def delete(self, path, expect_error=None, **params):
        """
        Performs HTTP `DELETE` in selected path

        :param path:  path
        :param params: kwargs that gets added to the querystring of the request
        :return: json decoded data from the response if json_decoded is set to true, otherwise the raw data
        """
        return self._do_request('delete', path, expect_error=expect_error, query_string=params)

    def _do_submit(self, method, path, expect_error=None, **params):
        """ Helper method that prepares data to be submitted """
        payload = None
        for key in params.keys():
            if key.startswith('data_'):
                payload = getattr(self, '_build_{type}_payload'.format(type=key[5:]))(params.pop(key))
        kwargs = {
            'query_string': params,
        }
        if payload is not None:
            kwargs.update(payload)
        return self._do_request(method, path, expect_error=expect_error, **kwargs)

    def _do_request(self, method, path, expect_error=None, **kwargs):
        method_fn = getattr(self.client, method)
        full_path = '{}{}'.format(self.base_url, path)
        response = method_fn(full_path, **kwargs)
        if self.response_decode:
            return self._decode_validate_json_response(response, expect_error)
        return response

    def _decode_validate_json_response(self, response, expect_error):
        response_json = decode_json(response.data)
        if self.response_check:
            if expect_error is not None:
                assert_in(response.status_code, (500, 400), 'Error: {!r}'.format(response.data))
                self._check_errors(response_json, expect_error)
            else:
                eq_(response.status_code, 200, 'Error: {!r}'.format(response.data))
                assert_success(response_json)
        return response_json

    def _check_errors(self, response, expect_error):
        if isinstance(expect_error, basestring):
            assert_error(response, expect_error)
        else:
            assert_error(response)

    def _build_json_payload(self, data):
        return {'data': json.dumps(data),
                'content_type': 'application/json'}

    def _build_raw_payload(self, data):
        return {'data': data}


def decode_json(data):
    """
    Tries to decode json, otherwise it raises a descriptive exception

    :param data: data to be json decoded
    """
    try:
        return json.loads(data)
    except ValueError:
        raise Exception('Cannot decode json: {!r}'.format(data))


def assert_success(response):
    assert_in('success', response, 'Missing success key: {!r}'.format(response))
    ok_(response['success'], 'Error: {!r}'.format(response))


def assert_error(response, error=None):
    for field in ('success', 'error', 'description'):
        assert_in(field, response)
    assert_false(response['success'])
    if error:
        eq_(error, response['error'])



