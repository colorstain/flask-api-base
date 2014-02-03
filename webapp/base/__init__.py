# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~~~~~
    
    
"""

from flask import Blueprint

base = Blueprint('base', __name__)

from views import *

