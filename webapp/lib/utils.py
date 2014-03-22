# -*- coding: utf-8 -*-
"""
    utils
    ~~~~~~~~~~~~~~~

    Collection of utilities
    
"""
import re
from flask.json import JSONEncoder

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def camel_case_to_underscore(name):
    """
    Converts a string from camel case to underscore delimited string
    :param name: string to be converted to underscore
    :return: the converted string
    """
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


class CustomJSONEncoder(JSONEncoder):

    def __init__(self, *args, **kwargs):
        """
        Initializes the custom json encoder to not accept NaN, and return a compact json representation
        :param args: args for the json encoder
        :param kwargs: kwargs for the json encoder
        """
        kwargs['allow_nan'] = False
        kwargs['separators'] = (',', ':')
        kwargs['indent'] = None
        super(CustomJSONEncoder, self).__init__(*args, **kwargs)

    def default(self, o):
        try:
            if hasattr(o, 'isoformat'):
                return o.isoformat()
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, o)