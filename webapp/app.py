# -*- coding: utf-8 -*-
"""
    app
    ~~~~~~~~~~~~~~~

    Main flask app
"""
import os
from werkzeug.utils import import_string
from webapp import AppFactory

os.environ.setdefault('ENV', 'development')

settings = import_string('settings.%s' % os.environ['ENV'])
app = AppFactory(settings).get_app(__name__)

if __name__ == '__main__':
    app.run()