# -*- coding: utf-8 -*-
import os
import unittest
import requests
from selenium import webdriver
from python_docker_test import PythonDockerTestMixin, ContainerNotReady
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class TestIntegration(PythonDockerTestMixin, StaticLiveServerTestCase):

    CONTAINER_IMAGE = 'lbjay/canvas-docker'
    CONTAINER_NAME = 'canvas-docker'
    CONTAINER_READY_TRIES = 10
    CONTAINER_READY_SLEEP = 20
    APP_SERVER_PORT = 8000

    @classmethod
    def container_ready_callback(cls, container_data):
        try:
            container_ip = container_data['NetworkSettings']['IPAddress']
            resp = requests.head('http://{}:3000'.format(container_ip))
            # request to base url should redirect to login when ready
            assert resp.status_code == 302

            # yes this is side-effect hackish, but the live server addr
            # needs to get set at some point between the setUpClass() methods
            # of PythonDockerTestMixin and LiveServerTestCase, and this is
            # much easier/better than mucking with inheritance call order
            gateway_ip = container_data['NetworkSettings']['Gateway']
            os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = gateway_ip + ':8000'

            return True
        except (requests.ConnectionError, AssertionError):
            raise ContainerNotReady()

    @classmethod
    def setUpClass(cls):
        super(TestIntegration, cls).setUpClass()

    def setUp(self):
        super(TestIntegration, self).setUp()
        self.session = requests.Session()
        self.session.headers.update({'Authorization': 'Bearer canvas-docker'})
        self.canvas_api_base = 'http://{}:3000/api/v1'.format(self.container_ip)
        self.browser = webdriver.Firefox()

    def tearDown(self):
        super(TestIntegration, self).tearDown()
        self.session.close()
        self.browser.quit()

    def api_url(self, path):
        return self.canvas_api_base + path

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



if __name__ == '__main__':
    unittest.main()
