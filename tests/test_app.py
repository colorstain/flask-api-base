# -*- coding: utf-8 -*-
"""
    test_app
    ~~~~~~~~~~~~~~~
    
    Test that factory configured application correctly
"""
from datetime import date
from nose.tools import *

from tests.base import AppBase
from tests.fixtures.app.app import app


class TestApp(AppBase):

    selected_app = app

    def test_normal_view(self):
        r = self.get('/')
        assert_not_in('description', r)

    def test_unexpected_exception(self):
        self.get('/dangerous', expect_error='unexpected_exception')

    def test_app_error(self):
        self.get('/app_error', expect_error='invalid_something')

    def test_dict_view_response(self):
        r = self.get('/json_response')
        assert_in('this', r)
        eq_(r['this'], 'that')

    def test_json_date(self):
        r = self.get('/date')
        today = date.today().isoformat()
        eq_(r['date'], today)

        r = self.get('/datetime')
        ok_(r['datetime'].startswith(today))