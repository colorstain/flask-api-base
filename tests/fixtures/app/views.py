# -*- coding: utf-8 -*-
"""
    views
    ~~~~~~~~~~~~~~~
    
    
"""
from datetime import datetime
from flask import Blueprint

from webapp.exceptions import AppBaseException


class InvalidSomething(AppBaseException):
    pass

test = Blueprint('test', __name__)

@test.route('/')
def success():
    return

@test.route('/dangerous')
def dangerous():
    raise ValueError('problem')

@test.route('/app_error')
def app_error():
    raise InvalidSomething('invalid')

@test.route('/json_response')
def json_response():
    return {'this': 'that'}

@test.route('/date')
def json_date():
    return {'date': datetime.now().date()}

@test.route('/datetime')
def json_datetime():
    return {'datetime': datetime.now()}