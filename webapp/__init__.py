# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~~~~~
    
    
"""

from importlib import import_module
from flask import Flask


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

