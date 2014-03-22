# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~~~~~
    
    
"""

from importlib import import_module
from flask import Flask as _Flask
from webapp.lib.api import api_success, error_handler
from webapp.lib.utils import CustomJSONEncoder


class Flask(_Flask):
    """
    Custom Flask class that accepts other types of views responses
    """

    def make_response(self, rv):
        """
        Extended version of make_response, in addition to accepting the normal make response
         types it also accepts None, which gets converted to api_success and a dict that
         gets json encoded automatically

        :param rv: return value from the view function
        """
        if rv is None:
            rv = api_success()
        if isinstance(rv, dict):
            description = rv.pop('description', None)
            rv = api_success(rv, description)
        return super(Flask, self).make_response(rv)


class AppFactory(object):

    def __init__(self, config):
        """
        AppFactory is a :class:`flask.Flask` app factory that loads an app instance dynamically with the
        passed configuration.

        :param config: Configuration object
        """
        self._app = None
        self.app_config = config

    def get_app(self, module_name, **kwargs):
        """
        Instanciates a Flask _app registering extensions and blueprints from
        settings.

        :param str module_name: name of the webapp module, usually `__name__`
        :param kwargs: kwargs that get passed to Flask
        :return: an instance of :class:`flask.Flask` class
        :rtype: :class:`flask.Flask`
        """
        self._app = Flask(module_name, **kwargs)
        self._app.config.from_object(self.app_config)

        self._bind_extensions()
        self._register_blueprints()
        self._customize_encoder()
        self._add_hooks()
        self._register_error_handlers()

        return self._app

    def _get_imports_by_path(self, path):
        module_name , object_name = path.rsplit('.', 1)
        module = import_module(module_name)
        if not hasattr(module, object_name):
            raise ImportError('Module %s does not have %s' % (module, object_name))
        return getattr(module, object_name)

    def _register_blueprints(self):
        for blueprint_path, url_prefix in self._app.config.get('BLUEPRINTS', []):
            blueprint = self._get_imports_by_path(blueprint_path)
            self._app.register_blueprint(blueprint, url_prefix=url_prefix)

    def _bind_extensions(self):
        for ext_path in self._app.config.get('EXTENSIONS', []):
            ext = self._get_imports_by_path(ext_path)
            if getattr(ext, 'init_app', False):
                ext.init_app(self._app)
            else:
                ext(self._app)

    def _customize_encoder(self):
        self._app.json_encoder = CustomJSONEncoder

    def _register_error_handlers(self):
        self._app.errorhandler(Exception)(error_handler)

        for error in range(400, 420) + range(500, 506):
            self._app.error_handler_spec[None][error] = error_handler

    def _add_hooks(self):
        for path in self._app.config.get('BEFORE_REQUEST_HOOKS', []):
            hook = self._get_imports_by_path(path)
            self._app.before_request(hook)

        for path in self._app.config.get('AFTER_REQUEST_HOOKS', []):
            hook = self._get_imports_by_path(path)
            self._app.after_request(hook)