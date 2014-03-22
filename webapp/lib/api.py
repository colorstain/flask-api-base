# -*- coding: utf-8 -*-
"""
    api
    ~~~~~~~~~~~~~~~

    Collection of functions for the api
    
"""
from functools import wraps

import traceback
from flask import jsonify, current_app, request
from werkzeug.exceptions import HTTPException
from webapp.exceptions import AppBaseException, InvalidBodyException, InvalidParametersException
from webapp.lib.utils import camel_case_to_underscore


def api_success(response=None, description=None):
    """
    Response indicating that the action was successful. Returns a json object with success: true as well
    as the response.

    :param response: api response to be converted to json
    :param description: description if any
    :return: a json response
    """
    if response is None:
        response = {}
    response['success'] = True
    if description is not None:
        response['description'] = description
    return jsonify(response)


def api_error(error, description, extra_info=None, error_code=500):
    """
    Response indicating error and that the actions as not successful. Returns a json
     response.

    :param str error: name of error
    :param str description: description of the error
    :param dict extra_info: any extra info that should be included in the response
    :param int error_code: HTTP error code
    :return: a json response with success: False, error name and other info with the specified error code
    """
    response = {'success': False,
                'error': error,
                'description': description}
    if extra_info and isinstance(extra_info, dict):
        response.update(extra_info)
    return jsonify(response), error_code


def error_handler(error):
    """
    API error handler, if the exception inherits from AppBaseException the error name is extracted and converted
    to an api error json response with code 400. If the error is an HTTPException, then the error code, message and name
    are taken from the error. Any other type of error is considered an unexpected exception it returns
    a json 500 error.

    :param error: Exception or Error
    :return: :raise error: json response with error information if the app is in testing mode it re raise the exception.
    """
    extra_info = None
    if isinstance(error, HTTPException):
        error_name = camel_case_to_underscore(error.__class__.__name__)
        error_code = error.code
        message = error.description
    elif isinstance(error, AppBaseException):
        error_name = camel_case_to_underscore(error.__class__.__name__).replace('_exception', '')
        error_code = 400  # Bad request
        message = error.message
    else:
        # log traceback
        tb = traceback.format_exc()
        current_app.logger.warning(tb)
        # re raise generic error when testing to ease debug when testing
        if current_app.config.get('TESTING', False):
            raise error
        # when debugging add the tb
        if current_app.config.get('DEBUG', False):
            extra_info = {'tb': tb}
        error_name = 'unexpected_exception'
        error_code = 500  # server error
        message = "something went bad, don't panic"
    return api_error(error_name, message, error_code=error_code, extra_info=extra_info)


def json_required(required_fields=None, optional_fields=None):
    """
    Usage:

        @json_required({'name': str}, {'age': int})
        def view_fn():
            # do something with json

    Decorator that checks if the request contains a valid json body, if required fields is
    :param dict required_fields: dictionary with required fields as keys and the type they should be as value
    :return: :raise InvalidParametersException: decorated function
    """
    if required_fields is None:
        required_fields = {}
    if optional_fields is None:
        optional_fields = {}

    def wrapper(fn):
        @wraps(fn)
        def wrapped_view(*args, **kwargs):
            json_body = request.get_json(silent=True, cache=True)
            if not json_body:
                error_msg = 'a valid JSON body is required'
                if required_fields:
                    error_msg = '%s, required fields: %s' % (error_msg, ', '.join(required_fields.iterkeys()))
                raise InvalidBodyException(error_msg)
            #checking required fields
            errors = _check_fields(json_body, required_fields)

            #checking optional fields
            errors += _check_fields(json_body, optional_fields, False)

            if errors:
                raise InvalidParametersException('errors: %s' % ', '.join(errors))
            return fn(*args, **kwargs)

        return wrapped_view
    return wrapper


def _check_fields(json_body, fields_dict, required=True):
    """
    Checks fields in the json body. It accumulates errors and returns them. If the required flag
    is `True`, the field has to be present in the json_body
    :param dict json_body: parsed json body
    :param dict fields_dict: dict that maps fields to the type they should be
    :param bool required: indicates if the fields in the dict are required
    :return: list of all the errors found in the json_body
    :rtype: list
    """
    errors = []
    for key, type_field in fields_dict.iteritems():
        type_name = type_field.__name__
        if type_field is str: # str -> basestring so that unicode strings are ok
            type_field = basestring
        if type_field is float:
            type_field = (float, int, long)  # float -> take all of the integer values too

        field = json_body.get(key, None)
        if field is None:
            if required:
                errors.append("'%s' field is missing" % key)
            else:
                continue
        elif not isinstance(field, type_field):
            errors.append('%s field must be type %s' % (key, type_name))
    return errors