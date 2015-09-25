#!/usr/bin/python3

import unittest

from bc_api import BC_API

class TestMethods(unittest.TestCase):

    def test_get_all_robots(self):
        api = BC_API()
        api.login()
        api.get_all_robots()


    def test_get_all_members(self):
        api = BC_API()
        api.login()
        api.get_all_members()


    def test_get_ws_url(self):
        api = BC_API()
        api.login()
        ws_url = api.get_ws_url()

if __name__ == "__main__":
    unittest.main()
