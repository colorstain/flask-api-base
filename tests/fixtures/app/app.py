# -*- coding: utf-8 -*-
"""
    app
    ~~~~~~~~~~~~~~~
    
    
"""
from werkzeug.utils import import_string
from webapp import AppFactory

settings = import_string('tests.fixtures.app.settings')
app = AppFactory(settings).get_app(__name__)