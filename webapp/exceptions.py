# -*- coding: utf-8 -*-
"""
    exceptions
    ~~~~~~~~~~~~~~~
    
    
"""


class AppBaseException(Exception):
    """
    App Base Exception, all api exceptions should inherit from this exception
    """
    pass


class InvalidParametersException(AppBaseException):
    pass


class InvalidBodyException(AppBaseException):
    pass