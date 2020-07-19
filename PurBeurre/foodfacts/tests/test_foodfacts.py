"""This file contains the unitary tests of foodfacts"""
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from PurBeurre.constants import PRODUCT_EXAMPLE
from foodfacts.models import Products
from foodfacts import views as fviews


class SimpleTest(TestCase):
    """
    Here we define attributes and functions to test
    the views responses and functions.
    """
    URI_f_BASE = "https://beurrepur.herokuapp.com/foodfacts/"
    home_request = URI_f_BASE
    aliment_request = f"{URI_f_BASE}aliment/1/"
    notice_request = f"{URI_f_BASE}notice/"
    resultats_gazpacho = f"{URI_f_BASE}resultats/?nav_search=Gazpacho"
    resultats_empty = f"{URI_f_BASE}resultats/?nav_search=empty/"
    account_request = f"{URI_f_BASE}account/"

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.test_user = User.objects.create_user(
            username='jacobin89',
            email='jacob@gmail.com',
            password='Niam1989')

    def test_views_home(self):
        """Tests the HTTP response"""
        response = self.client.get(self.home_request)
        self.assertEqual(response.status_code, 200)

    def test_views_resultats_gazpacho(self):
        """Tests the HTTP response"""
        response = self.client.get(self.resultats_gazpacho)
        self.assertEqual(response.status_code, 200)

    def test_views_aliment(self):
        """Tests the HTTP response"""
        product = PRODUCT_EXAMPLE
        query = Products(**product)
        query.save()

        request = self.factory.get(self.resultats_gazpacho)
        request.user = self.test_user
        response = fviews.search_term(request)
        assert response.status_code == 200

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
        selection = fviews.select_better_products("soup", -4)
        assert selection is not None

    def test_search_product(self):
        """Tests the retrieving of the wanted product"""
        product = PRODUCT_EXAMPLE
        query = Products(**product)
        query.save()
        searched = fviews.select_product("Gazpacho")
        assert searched is not None

    def test_show_details(self):
        """Tests the requesting of a specific product"""
        product = PRODUCT_EXAMPLE
        query = Products(**product)
        query.save()
        article = fviews.select_product("Gazpacho")
        selected = fviews.show_details(article.idproduct)
        assert selected is not None

    def test_product_wanted(self):
        product = PRODUCT_EXAMPLE
        query = Products(**product)
        query.save()

        request = self.factory.get(self.resultats_gazpacho)
        request.user = self.test_user

        response = fviews.product_wanted(request, product["idproduct"])
        assert response is not None
        assert response.status_code == 200
