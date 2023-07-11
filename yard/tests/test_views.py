from django.conf import settings
from django.test import TestCase


class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_language_using_de_cookie(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "de"})
        response = self.client.get("/")
        self.assertContains(response, b"Betriebszeiten")

    def test_language_using_et_cookie(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "de"})
        response = self.client.get("/")
        self.assertContains(response, b"Liidu liige")

    def test_language_using_en_cookie(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "en"})
        response = self.client.get("/")
        self.assertContains(response, b"established")

    def test_language_using_ru_cookie(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "ru"})
        response = self.client.get("")
        decoded_content = response.content.decode("utf-8")
        self.assertIn("переработчиков", decoded_content)

    def test_language_using_header(self):
        response = self.client.get("", headers={"accept-language": "et"})
        self.assertContains(response, b"ainulaadne")
