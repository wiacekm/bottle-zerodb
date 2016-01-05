#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import os
import sys

import bottle
from bottle.ext.zerodb import ZeroDbPlugin

from zerodb import DB
from zerodb.models import Model, Field
import transaction
import zerodb

class Example(Model):
    name = Field()

    def __str__(self):
        return '{name: %s}' % self.name

    __repr__ = __str__

class ZeroDbTest(unittest.TestCase):

    def setUp(self):
        self.app = bottle.Bottle(catchall=False)
        plugin = ZeroDbPlugin(("localhost", 8001),
                              username='root',
                              password='test'
                              )
        self.plugin = self.app.install(plugin)
        self.example = Example(name="test")

    def test_with_keyword(self):
        @self.app.get('/')
        def test(zerodb):
            self.assertEqual(type(zerodb), DB)
            self.assertTrue(zerodb)
        self.app({'PATH_INFO': '/', 'REQUEST_METHOD': 'GET'}, lambda x, y: None)

    def test_save(self):
        @self.app.get('/')
        def test(zerodb):
            count = len(zerodb[Example])
            with transaction.manager:
                zerodb.add(self.example)
            self.assertTrue(zerodb)
            self.assertEqual(len(zerodb[Example]), count+1)
        self.app({'PATH_INFO':'/', 'REQUEST_METHOD':'GET'}, lambda x,y: None)

    def test_install_plugin_twice(self):
        with self.assertRaises(bottle.PluginError):
            self.app.install(self.plugin)

    def test_get_plugin_description(self):
        keyword = "testdb"
        self.assertRegexpMatches(str(ZeroDbPlugin(("localhost", 8001), keyword)), keyword)

if __name__ == '__main__':
    unittest.main()
