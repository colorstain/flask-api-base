# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~~~~~
    
    Settings module, common settings go here
"""
import os

DEBUG = False
SECRET_KEY = 'my_secret_key'

ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

BLUEPRINTS = (  # tuples of module and url
    ('webapp.base.base', ''),
)

EXTENSIONS = (

)

BEFORE_REQUEST_HOOKS = (
)

AFTER_REQUEST_HOOKS = (

)