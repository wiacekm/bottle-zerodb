Bottle ZeroDB
=============

This bottle-zerodb plugin integrates ZeroDB with your Bottle
application. It injects a ZeroDB session in your route and handle the
session cycle.

Usage Example:

.. code-block:: python

    from bottle import Bottle ,redirect
    from bottle.ext.zerodb import ZeroDbPlugin
    from zerodb.models import Model, Field


    class Element(Model):
        name = Field()


    app = Bottle()
    plugin = ZeroDbPlugin()
    app.install(plugin)

    @app.route('/', method='GET')
    def index(zerodb):
        return 'Number of Elements in: %s' % len(zerodb[Element])

    @app.route('/add/', method='POST')
    def add(zerodb):
        zerodb.add(Element(name="example"))
        redirect("/")
