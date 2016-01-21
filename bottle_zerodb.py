# -*- coding: utf-8 -*-
"""ZeroDB support for Bottle.

This module provides a Bottle extension for supporting MongoDB for:

    - injecting a ZeroDB connection into handler functions
    - converting ZeroDB style returns from handlers into JSON

This module contains the following public classes:

    - ZeroDbPlugin -- The plugin for supporting handler functions.

"""
__all__ = ['ZeroDbPlugin']

from bottle import PluginError
import inspect
import zerodb


class ZeroDbPlugin(object):
    """ZeroDB Plugin for Bottle.

    Connect to a zerodb instance, and add a DB in a Bottle callback
    Sample :

        import bottle
        from bottle.ext import zerodb
        from zerodb.models import Model, Field

        app = bottle.Bottle()
        plugin = zerodb.ZeroDbPlugin()
        app.install(plugin)

        class Example(Model):
            name = Field()

        @app.route('/add/:item')
        def add(item, zerodb):
            zerodb.add(Example(item))
            return 'Number of elements in DB: %s' % len(zerodb[Example])

    uri : ZeroDB hostname or uri
    keyword : Override parameter name in Bottle function.
    post_create : Callback function to customize database obj after creation.

    """

    api = 2

    def get_db(self):
        """Return the mongo connection from the environment."""
        if self.zerodb_db:
            return self.zerodb_db
        db = zerodb.DB(self.sock, self.username, self.password, **self.kwargs)
        if self.post_create:
            db = self.post_create(db)
        self.zerodb_db = db
        return self.zerodb_db

    def __init__(self, sock, keyword='zerodb',
                 username=None, password=None,
                 post_create=None, **kwargs):
        self.sock = sock
        self.keyword = keyword
        self.username = username
        self.password = password
        self.zerodb_db = None
        self.post_create = post_create
        self.kwargs = {}
        self.kwargs.update(kwargs)

    def __str__(self):
        return "bottle_zerodb.ZeroDbPlugin(keyword=%r)" % (self.keyword)

    __repr__ = __str__

    def setup(self, app):
        """Called as soon as the plugin is installed to an application."""
        for other in app.plugins:
            if not isinstance(other, ZeroDbPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another ZeroDB plugin with "
                                  "conflicting settings (non-unique keyword).")

    def apply(self, callback, context):
        """Return a decorated route callback."""
        args = inspect.getargspec(context.callback)[0]
        # Skip this callback if we don't need to do anything
        if self.keyword not in args:
            return callback

        def wrapper(*a, **ka):
            ka[self.keyword] = self.get_db()
            rv = callback(*a, **ka)
            return rv

        return wrapper
