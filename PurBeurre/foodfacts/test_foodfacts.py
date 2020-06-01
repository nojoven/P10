"""This file contains the unitary tests of foodfacts"""
from django.test import TestCase, Client
from PurBeurre.constants import PRODUCT_EXAMPLE
from foodfacts.models import Products
from foodfacts.modules.database_service import DatabaseService


class SimpleTest(TestCase):
    """
    Here we define attributes and functions to test
    the views responses and functions.
    """
    URI_f_BASE = "https://beurrepur.herokuapp.com/foodfacts/"
    home_request = URI_f_BASE
    aliment_request = f"{URI_f_BASE}aliment/1/"
    notice_request = f"{URI_f_BASE}notice/"
    resultats_gazpacho = f"{URI_f_BASE}resultats/Gazpacho/"
    resultats_empty = f"{URI_f_BASE}resultats/empty/"
    account_request = f"{URI_f_BASE}account/"
    c = Client()

    def test_views_home(self):
        """Tests the HTTP response"""
        response = self.client.get(self.home_request)
        self.assertEqual(response.status_code, 200)

    def test_views_resultats_gazpacho(self):
        """Tests the HTTP response"""
        response = self.client.get(self.resultats_gazpacho)
        self.assertEqual(response.status_code, 200)

        response = self.c.post("/foodfacts/research",
                               {'nav_search': 'Gazpacho'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/foodfacts/resultats/Gazpacho/")

    def test_views_aliment(self):
        """Tests the HTTP response"""
        product = PRODUCT_EXAMPLE
        query = Products(**product)
        query.save()

        product = DatabaseService.select_product("Gazpacho")
        product_id = product.idproduct

        response = self.client.get(f"{self.URI_f_BASE}aliment/{product_id}")
        self.assertEqual(response.status_code, 301)

    def test_views_resultats_empty(self):
        """Tests the HTTP response"""
        response = self.client.get(self.resultats_empty)
        self.assertEqual(response.status_code, 200)

    def test_views_notice(self):
        """Tests the HTTP response"""
        response = self.client.get(self.notice_request)
        self.assertEqual(response.status_code, 200)

    def test_select_better_products(self):
        """Tests the the database request for better products"""
        selection = DatabaseService.select_better_products("soup", -4)
        assert selection is not None

    def test_search_product(self):
        """Tests the retrieving of the wanted product"""
        product = PRODUCT_EXAMPLE
        query = Products(**product)
        query.save()
        searched = DatabaseService.select_product("Gazpacho")
        assert searched is not None

    def test_show_details(self):
        """Tests the requesting of a specific product"""
        product = PRODUCT_EXAMPLE
        query = Products(**product)
        query.save()
        article = DatabaseService.select_product("Gazpacho")
        selected = DatabaseService.show_details(article.idproduct)
        assert selected is not None

    print(aliment_request)
