# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from canvas_docker_test import CanvasDockerTestMixin
from django.test import LiveServerTestCase

class TestIntegration(CanvasDockerTestMixin, LiveServerTestCase):

    DOCKER_IMAGE = 'lbjay/canvas-docker'
    APP_SERVER_PORT = '8000'

    def setUp(self):
        super(TestIntegration, self).setUp()
        self.browser = webdriver.Firefox()

    def tearDown(self):
        super(TestIntegration, self).tearDown()
        self.browser.quit()

    def test_tool_registration(self):
        reg_params = {
            'name': 'Canvas-Docker LTI Test',
            'consumer_key': 'consumer_key',
            'shared_secret': 'secret_key',
            'config_type': 'by_url',
            'config_url': 'http://{}:{}/course_admin/tool_config'.format(
                self.docker_gateway_ip,
                self.APP_SERVER_PORT)
        }

        self.session.post(
            self.api_url("/accounts/1/external_tools"),
            data=reg_params)

        tool_resp = self.session.get(self.api_url("/accounts/1/external_tools"))
        tool_list = tool_resp.json()
        self.assertTrue(len(tool_list) > 0)
        self.assertEqual(tool_list[0]['name'], 'Canvas-Docker LTI Test')

    # def test_tool_navigation(self):
    #     self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
