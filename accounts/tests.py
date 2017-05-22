from django.test import TestCase

from .models import make_api_key


class ApiKeyTests(TestCase):

    def test_make_api_key(self):
        key = make_api_key()
        self.assertEqual(len(key), 32)
