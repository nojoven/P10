"""
This is the file used to test the functions
that are specific to a user account
"""
import pytest
import logging
from django.contrib.auth import authenticate
from django.test import TestCase, Client
from PurBeurre.constants import IMG_URL, PRODUCT_EXAMPLE
from foodfacts.models import Favorites, Products
from foodfacts.modules.database_service import DatabaseService
from roles.forms import (
    CreateForm, UpdateProfileForm, LikeForm, SigninForm,
    UnlikeForm)


class SimpleTest(TestCase):
    """
    class used to
    test the HTTP GET responses of views
    """
    URI_r_BASE = "http://localhost:8000/roles/"
    provided_mail = "dubosc@gmail.com"
    provided_password = "Franck"
    signin_request = f"{URI_r_BASE}signin/"
    logout_request = f"{URI_r_BASE}logout/"
    favourites_request = f"{URI_r_BASE}favourites/"
    account_request = f"{URI_r_BASE}account/"
    register_request = f"{URI_r_BASE}register/"
    c = Client()
    LOGGER = logging.getLogger(__name__)

    def test_views_signin(self):
        """Get of signin page"""
        response = self.client.get(self.signin_request)
        assert response.status_code == 200
        self.client.post("/roles/signin", {
            'signin_email': 'ezzou@gmail.com',
            'signin_password': 'ezzou'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            'form',
            "signin_email",
            None)

    def test_views_favourites(self):
        """Get of favourites page"""
        response = self.client.get(self.favourites_request)
        assert response.status_code == 200

    def test_views_account(self):
        """Get of account page"""
        response = self.client.get(self.account_request)
        assert response.status_code == 200

    def test_views_register(self):
        """Get of register page"""
        response = self.client.get(self.register_request)
        assert response.status_code == 200

    def test_views_logout(self):
        """Get of register page"""
        response = self.client.get(self.logout_request)
        assert response.status_code == 200

    def test_service_details(self):
        """Tests show_details()"""
        product = PRODUCT_EXAMPLE
        query = Products(**product)
        query.save()

        product = DatabaseService.select_product("Gazpacho")
        product_id = product.idproduct

        data = DatabaseService.show_details(product_id)
        assert data is not None


@pytest.mark.django_db
class TestRoles(TestCase):
    """Pytest will be used to verify the behaviour of
     the following functions"""
    c = Client()
    LOGGER = logging.getLogger(__name__)

    provided_mail = "dubosc@gmail.com"
    provided_password = "Franck"

    def test_create_product(self):
        """Tests the creation of a product"""
        product = PRODUCT_EXAMPLE
        query = Products(**product)
        query.save()
        article = DatabaseService.select_product("Gazpacho")
        assert article.productname == "Gazpacho"

    def test_create_update_user_data(
        self,
        provided_username="username1",
        provided_mail="user@gmail.com",
        provided_password="test1234",
        update_email="update@test.com",
        update_first_name="Pierre",
        update_last_name="Dupuis",
    ):
        """Tests the update of a profile"""
        DatabaseService.create_user(
            provided_username,
            provided_password,
            provided_mail,
            "User",
            "TESTNAME"
        )

        user = authenticate(username=provided_mail,
                            password=provided_password)
        assert user is not None

        email_before = user.email
        assert email_before is not None

        first_name_before = user.first_name
        assert first_name_before is not None

        last_name_before = user.last_name
        assert last_name_before is not None

        try:
            if update_email != "" \
                    and update_email != email_before:
                user.email = update_email
                assert user.email != email_before
            if update_first_name != "" \
                    and update_first_name != first_name_before:
                user.first_name = update_first_name
                assert user.first_name != first_name_before
            if update_last_name != "" \
                    and update_last_name != last_name_before:
                user.last_name = update_last_name
                assert user.last_name != last_name_before
            user.save()

            user = authenticate(username=update_email,
                                password=provided_password)
            assert user is not None
            assert user.email != email_before
            assert user.first_name != first_name_before
            assert user.last_name != last_name_before

            user.email = email_before
            user.first_name = first_name_before
            user.last_name = last_name_before
            user.save()
            assert user.email == email_before
            assert user.first_name == first_name_before
            assert user.last_name == last_name_before

        except KeyError:
            return KeyError("USER DOES NOT EXISTS")

    def test_views_create_update_user_data(
        self,
        provided_mail="user@gmail.com",
        provided_password="test1234",
        update_email="update@test.com",
        update_first_name="Pierre",
        update_last_name="Dupuis",
    ):
        """Tests the update of a profile"""
        response = self.c.post(
            "/roles/create", {
                'prenom': 'Jean',
                'nom': 'Dubois',
                'mot_de_passe': provided_password,
                'repeter_mot_de_passe': provided_password,
                'mail': provided_mail,
                'telephone': int("0606060606")
            })
        self.LOGGER.info(f"RESPONSE CREATE IS {response}")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/roles/account")

        response = self.c.post(
            "/roles/profileupdate", {
                'update_first_name': update_first_name,
                'update_last_name': update_last_name,
                'update_email': update_email,
                'confirm_email': provided_mail,
                'confirm_password': provided_password
            })
        self.assertEqual(response.status_code, 200)

    def test_find_user_category_favourites(self):
        """Tests if a user has a product in a category"""
        favourites = DatabaseService.sort_favourites(4, "soup")
        assert favourites is not None

    def test_find_favorite_in_products(self):
        """
        Tests if a liked product is found in the
        products table.
        """
        product = PRODUCT_EXAMPLE
        query = Products(**product)
        query.save()
        product = DatabaseService.select_product("Gazpacho")
        product_id = product.idproduct

        like_data = dict()
        like_data["productid"] = product_id
        like_data["name"] = product.productname
        like_data["nutrigrade"] = product.nutrigrade
        like_data["stores"] = product.stores
        like_data["brands"] = product.brands
        like_data["category"] = product.category
        like_data["quantity"] = product.quantity
        like_data["replacedid"] = product_id
        like_data["replacedarticle"] = product.productname
        like_data["replacednutrigrade"] = product.nutrigrade
        like_data["userid"] = 4
        like_data[
            "front_img"
        ] = IMG_URL

        if not Favorites.objects.filter(
                productid=like_data["productid"]).exists():
            query = Favorites(**like_data)
            query.save()

        article = DatabaseService.select_liked_in_products(product_id)
        assert article is not None

    def test_get_all_user_favs(self):
        """Tests the SELECT on all user's favourites"""
        like_data = dict()
        like_data["productid"] = 22
        like_data["name"] = "Gazpacho Vert"
        like_data["nutrigrade"] = "a"
        like_data["stores"] = "'auchan', 'magasins-u'"
        like_data["brands"] = "Innocent"
        like_data["category"] = "soup"
        like_data["quantity"] = "84 g"
        like_data["replacedid"] = 1
        like_data["replacedarticle"] = "Gazpacho"
        like_data["replacednutrigrade"] = "a"
        like_data["userid"] = 4
        like_data[
            "front_img"
        ] = IMG_URL

        if not Favorites.objects.filter(
                productid=like_data["productid"]).exists():
            query = Favorites(**like_data)
            query.save()
        user_favs = DatabaseService.select_user_favs(4)
        assert user_favs is not None
        assert len(user_favs) > 0

    def test_create_remove_fav(self):
        """Tests creation then deletion af a favourite"""
        like_data = dict()
        like_data["productid"] = 44
        like_data["name"] = "Gazpacho Vert"
        like_data["nutrigrade"] = "a"
        like_data["stores"] = "'auchan', 'magasins-u'"
        like_data["brands"] = "Innocent"
        like_data["category"] = "soup"
        like_data["quantity"] = "84 g"
        like_data["replacedid"] = 1
        like_data["replacedarticle"] = "Gazpacho"
        like_data["replacednutrigrade"] = "a"
        like_data["userid"] = 4
        like_data[
            "front_img"
        ] = IMG_URL

        if not Favorites.objects.filter(productid=44).exists():
            query = Favorites(**like_data)
            query.save()
            user_favs = DatabaseService.select_user_favs(4)
            assert user_favs is not None

        item = Favorites.objects.filter(productid=44, userid=4)

        item.delete()
        assert len(Favorites.objects.filter(productid=44, userid=4)) == 0

    def test_update_form(self):
        """Tests the profile update form"""
        update_email = "charlie@choco.org"
        update_first_name = "Marcel"
        update_last_name = "Dupuis"
        confirm_email = "lucien@gmail.com"
        confirm_password = "Daddy"
        u_form = UpdateProfileForm(
            data={
                'update_first_name': update_first_name,
                "update_last_name": update_last_name,
                "confirm_password": confirm_password,
                "confirm_email": confirm_email,
                "update_email": update_email
            })
        assert u_form.is_valid()

    def test_create_form(self):
        """Tests the user create form"""
        prenom = "gaston"
        nom = "lagaffe"
        mot_de_passe = "lagaffe06"
        repeter_mot_de_passe = "lagaffe06"
        mail = "gaston@gmail.com"
        telephone = "0601020304"
        c_form = CreateForm(
            data={
                'prenom': prenom,
                "nom": nom,
                "mot_de_passe": mot_de_passe,
                "repeter_mot_de_passe": repeter_mot_de_passe,
                "mail": mail,
                "telephone": telephone
            })
        assert c_form.is_valid()

    def test_like_form(self):
        """tests the like form"""
        liked_id = 5
        replaced_id = 89
        replaced_name = "Cheese"
        replaced_nutrigrade = "D"
        userid = 57
        l_form = LikeForm(
            data={
                'liked_id': liked_id,
                "replaced_id": replaced_id,
                "replaced_name": replaced_name,
                "replaced_nutrigrade": replaced_nutrigrade,
                "userid": userid
            })
        assert l_form.is_valid()

    def test_views_like_form(self):
        """Tests the like """
        response = self.client.get(SimpleTest.signin_request)
        assert response.status_code == 200
        self.client.post("/roles/signin", {
            'signin_email': 'ezzou@gmail.com',
            'signin_password': 'ezzou'})

        product = PRODUCT_EXAMPLE
        query = Products(**product)
        query.save()

        """Creation of a favourite"""
        like_data = dict()
        like_data["productid"] = 44
        like_data["name"] = "Gazpacho Vert"
        like_data["nutrigrade"] = "a"
        like_data["stores"] = "'auchan', 'magasins-u'"
        like_data["brands"] = "Innocent"
        like_data["category"] = "soup"
        like_data["quantity"] = "84 g"
        like_data["replacedid"] = 1
        like_data["replacedarticle"] = "Gazpacho"
        like_data["replacednutrigrade"] = "a"
        like_data["userid"] = 2
        like_data[
            "front_img"
        ] = IMG_URL
        # if not Favorites.objects.filter(
        #         productid=like_data["productid"]).exists():
        query = Favorites(**like_data)
        query.save()
        self.LOGGER.info("SAVED")
        """tests the like """
        response = self.client.post("/roles/like/", {
            'liked_id': like_data["productid"],
            "replaced_id": like_data["replacedid"],
            "replaced_name": like_data["replacedarticle"],
            "replaced_nutrigrade": like_data["replacednutrigrade"],
            "userid": like_data["userid"]
        })
        self.assertEqual(response.status_code, 302)

    def test_unlike_form(self):
        """Tests the unlike form"""
        unliked_id = 999
        userid_unlike = 57
        unl_form = UnlikeForm(
            data={
                'unliked_id': unliked_id,
                "userid_unlike": userid_unlike
            })
        assert unl_form.is_valid()

    def test_views_unlike_form(self):
        """Test the unlike wiew"""
        response = self.client.get(SimpleTest.signin_request)
        assert response.status_code == 200
        self.client.post("/roles/signin", {
            'signin_email': 'ezzou@gmail.com',
            'signin_password': 'ezzou'})

        product = PRODUCT_EXAMPLE
        query = Products(**product)
        query.save()

        """Creation of a favourite"""
        like_data = dict()
        like_data["productid"] = 44
        like_data["name"] = "Gazpacho Vert"
        like_data["nutrigrade"] = "a"
        like_data["stores"] = "'auchan', 'magasins-u'"
        like_data["brands"] = "Innocent"
        like_data["category"] = "soup"
        like_data["quantity"] = "84 g"
        like_data["replacedid"] = 1
        like_data["replacedarticle"] = "Gazpacho"
        like_data["replacednutrigrade"] = "a"
        like_data["userid"] = 2
        like_data[
            "front_img"
        ] = IMG_URL
        # if not Favorites.objects.filter(
        #         productid=like_data["productid"]).exists():
        query = Favorites(**like_data)
        query.save()
        self.LOGGER.info("SAVED")
        """tests the like """
        response = self.client.post("/roles/unlike/", {
            'unliked_id': like_data["productid"],
            "userid_unlike": like_data["userid"]
        })
        self.assertEqual(response.status_code, 302)

    def test_signin_form(self):
        """Tests the signin form"""
        signin_email = "sonic@sega.com"
        signin_password = "herisson"
        s_form = SigninForm(
            data={
                'signin_email': signin_email,
                "signin_password": signin_password
            })
        assert s_form.is_valid()
