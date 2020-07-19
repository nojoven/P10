"""
This is the file used to test the functions
that are specific to a user account
"""
import pytest
import logging
from django.test import TestCase
from PurBeurre.constants import PRODUCT_EXAMPLE
from foodfacts.models import Products


@pytest.mark.django_db
class TestRoles(TestCase):
    """Pytest will be used to verify the behaviour of
     the following functions"""
    URI_r_BASE = "http://localhost:8000/roles/"
    logout_request = f"{URI_r_BASE}logout/"
    favourites_request = f"{URI_r_BASE}favourites/"
    account_request = f"{URI_r_BASE}account/"
    register_request = f"{URI_r_BASE}register/"
    signin_request = f"{URI_r_BASE}signin/"
    like_gazpacho_path = f"{URI_r_BASE}like/44/191/"
    unlike_gazpacho_path = f"{URI_r_BASE}unlike/44/"

    LOGGER = logging.getLogger(__name__)

    def test_views_register(self):
        """Reach the register page"""
        response = self.client.get(self.register_request)
        assert response.status_code == 200

    def test_create_login_update_user_data(
            self,
            username="username1",
            email="user@gmail.com",
            password1="test1234$",
            password2="test1234$",
            first_name="Pierre",
            last_name="Dupuis",
    ):

        """Reach the sign up page"""
        response = self.client.get(self.register_request)
        assert response.status_code == 200

        response = \
            self.client.post("/roles/create",
                             {
                                 "username": username,
                                 "email": email,
                                 "password1": password1,
                                 "password2": password2,
                                 "first_name": first_name,
                                 "last_name": last_name
                             })

        assert response.status_code == 302

        """Reach the favourites page"""
        response = self.client.get(self.favourites_request)
        assert response.status_code == 200

        """Reach the account page"""
        response = self.client.get(self.account_request)
        assert response.status_code == 200

        new_email = "charlie@choco.org"
        new_first_name = "Marcel"
        new_last_name = "Dupuis"
        response = self.client.post(
            "/roles/profileupdate",
            {
                'first_name': new_first_name,
                "last_name": new_last_name,
                "email": new_email
            }
        )
        assert response is not None
        assert response.status_code == 200

        logout_response = self.client.get(self.logout_request)
        assert logout_response.status_code == 302

        login_response = self.client.post(
            "/roles/signin",
            {"email": "rose@gmail.com",
             "password": "Niam1989"}
            )
        assert login_response.status_code == 200

        exit_page_response = self.client.get(self.signin_request)
        assert exit_page_response.status_code == 200

        logout_response = self.client.get(self.logout_request)
        assert logout_response.status_code == 302

    def test_like_then_unlike(self):
        """
        This tests the adding and the deletion
        of a favourite
        """
        query = Products(**PRODUCT_EXAMPLE)
        query.save()
        login_page_response = self.client.get(self.signin_request)
        assert login_page_response.status_code == 200

        login_response = self.client.post(
            "/roles/signin",
            {"email": "rose@gmail.com",
             "password": "Niam1989"}
        )
        assert login_response.status_code == 200

        like_response = self.client.post(
            self.like_gazpacho_path
        )
        assert like_response.status_code == 302
