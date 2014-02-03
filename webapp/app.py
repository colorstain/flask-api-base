# -*- coding: utf-8 -*-
"""
    webapp
    ~~~~~~~~~~~~~~~
    
    
"""
import os
from werkzeug.utils import import_string
from webapp import AppFactory

os.environ.setdefault('ENV', 'Development')

settings = import_string('webapp.settings.%sConfig' % os.environ['ENV'])
app = AppFactory(settings).get_app(__name__)

if __name__ == '__main__':
    app.run()