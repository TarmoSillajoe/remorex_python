from django.conf import settings
from django.test import TestCase
from django.urls import reverse


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
        self.assertContains(response, b"Fachverband")

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

    def test_set_language_page_changes_language(self):
        response = self.client.post(
            reverse("set_language"), data={"next": "", "language": "et"}
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get("")
        decoded_content = response.content.decode("utf-8")
        self.assertIn("lammutusele", decoded_content)
