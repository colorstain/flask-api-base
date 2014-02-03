# -*- coding: utf-8 -*-
"""
    views
    ~~~~~~~~~~~~~~~
    
    
"""

from webapp.base import base
from webapp.lib.api import api_success

@base.route('/')
def hello_world():
    return api_success({'msg': 'hello world'})