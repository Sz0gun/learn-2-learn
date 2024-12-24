import os
from unittest import mock
from django.test import TestCase
from core.utils import setup_environment, get_django_settings_module

class TestUtils(TestCase):
    def test_get_django_settings_module_dev(self):
        with mock.patch.dict(os.environ, {'DJANGO_ENV': 'dev'}):
            self.assertEqual(get_django_settings_module(), 'core.settings.dev')

    def test_get_django_settings_module_prod(self):
        with mock.patch.dict(os.environ, {'DJANGO_ENV': 'prod'}):
            self.assertEqual(get_django_settings_module(), 'core.settings.prod')

    def test_setup_environment_dev(self):
        with mock.patch.dict(os.environ, {'DJANGO_ENV': 'dev'}):
            setup_environment()
            self.assertEqual(os.getenv('DJANGO_SETTINGS_MODULE'), 'core.settings.dev')

    def test_setup_environment_prod(self):
        with mock.patch.dict(os.environ, {'DJANGO_ENV': 'prod'}):
            setup_environment()
            self.assertEqual(os.getenv('DJANGO_SETTINGS_MODULE'), 'core.settings.prod')

    def test_environment_variables_set(self):
        # Test for 'dev'
        with mock.patch.dict(os.environ, {'DJANGO_ENV': 'dev'}):
            setup_environment()
            self.assertEqual(os.getenv('DJANGO_SETTINGS_MODULE'), 'core.settings.dev')

        # Test for 'prod'
        with mock.patch.dict(os.environ, {'DJANGO_ENV': 'prod'}):
            setup_environment()
            self.assertEqual(os.getenv('DJANGO_SETTINGS_MODULE'), 'core.settings.prod')
