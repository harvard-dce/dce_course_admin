# -*- coding: utf-8 -*-

import unittest
from seleniumrequests import Firefox


class FunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_tool_config(self):
        response = self.browser.request('GET', 'http://localhost:8000/course_admin/tool_config')
        self.assertEqual(response.headers['Content-Type'], 'text/xml')
        self.assertIn('<blti:title>DCE Course Admin</blti:title>', response.text)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
