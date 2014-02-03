# -*- coding: utf-8 -*-
"""
    settings
    ~~~~~~~~~~~~~~~
    
    
"""
import os


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = ''

    ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

    BLUEPRINTS = (  # tuples of module and url
        ('webapp.base.base', ''),
    )

    EXTENSIONS = (

    )


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    TESTING = True