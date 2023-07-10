from django.conf import settings
from django.test import TestCase


class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_language_using_cookie(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "de"})
        response = self.client.get("/")
        self.assertContains(response, b"Samstag")

    def test_language_using_header(self):
        response = self.client.get("", headers={"accept-language": "et"})
        self.assertContains(response, b"ainulaadne")
