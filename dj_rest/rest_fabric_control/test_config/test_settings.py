# from django.test import TestCase
# from shared.settings import config


# class TestSettings(TestCase):
#     def test_base_settings(self):
#         """Test if base settings are loaded correctly."""
#         self.assertTrue(config.DJANGO_SECRET_KEY)
#         self.assertIn('localhost', config.ALLOWED_HOSTS)

#     def test_dev_settings(self):
#         """Test if development settings are configured correctly."""
#         from core.settings.dev import DEBUG, DATABASES
#         self.assertTrue(DEBUG)
#         self.assertEqual(DATABASES['default']['NAME'], config.PSQL_DB_DEV)

#     def test_prod_settings(self):
#         """Test if production settings are configured correctly."""
#         from core.settings.prod import DEBUG, DATABASES
#         self.assertFalse(DEBUG)
#         self.assertEqual(DATABASES['default']['NAME'], config.PSQL_DB_PROD)
