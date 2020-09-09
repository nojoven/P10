"""
This file is used to test the functionalities in the browser.
It will use Selenium.
"""
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
import logging

from foodfacts.models import Products, Favorites


class MySeleniumTests(StaticLiveServerTestCase):
    """
    This class provides a configuration and a set of actions to
    simulate the behaviour of a human user.
    """

    URI_r_BASE = "http://localhost:8000/roles/"
    register_request = f"{URI_r_BASE}register/"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.implicitly_wait(4)


    def test_browser(self):
        """
        This contains the list of actions to perform in the browser,
         the order in which Selenium executes them and the assertions to test.
        """

        print(Favorites.objects.all())

        print(self.live_server_url)

        logging.info("Starting selenium")
        print("Starting selenium")

        # First we go full screen
        self.driver.maximize_window()
        logging.info("Window maximized")
        print("Window maximized")
        # Then we go on the website
        self.driver.start_client()

        self.driver.execute_script(open("../management/commands/fill_db.py").read())

        self.driver.get(f"{self.live_server_url}/foodfacts/")
        logging.info("Got localhost")
        print("Got localhost")
        self.assertIn(
            "GRAS", self.driver.find_element_by_id(
                "main_title").text)

        logging.info("Home title contains 'GRAS'")
        print("Home title contains 'GRAS'")


        username="BigFriend90s",
        email="monami@gmail.com",
        password1="Niam1989",
        password2="Niam1989",
        first_name="Robert",
        last_name="Engels",
        """Reach the sign up page"""
        response = self.client.get(self.register_request)
        assert response.status_code == 200
        self.client.post(
            "/roles/create",
             {
                 "username": username,
                 "email": email,
                 "password1": password1,
                 "password2": password2,
                 "first_name": first_name,
                 "last_name": last_name
             })

        # Then we go on the sigin page
        self.driver.get(f"{self.live_server_url}/roles/signin/")
        logging.info("Asking signin page")
        print("Asking signin page")
        self.assertIn(
            "CONNEXION", self.driver.find_element_by_tag_name(
                "h1").text)
        logging.info("On signin page.")
        print("On signin page.")
        # We sign in
        signin_email = self.driver.find_element_by_name("email")
        signin_email.send_keys("monami@gmail.com")
        signin_password = self.driver.find_element_by_name("password")
        signin_password.send_keys("Niam1989")
        self.driver.find_element_by_xpath('//input[@type="submit"]').click()
        logging.info("Signin form submitted")
        print("Signin form submitted")
        self.assertIn(
            "Editez", self.driver.find_element_by_id("sub_title").text
        )
        logging.info("On account page")
        print("On account page")
        # We look for a product
        search_navbar_input = self.driver.find_element_by_id("nav_input")
        logging.info("We want cheese")
        print("We want cheese")
        self.driver.execute_script("document.getElementById('nav_input').value = 'cheese'")
        search_navbar_input.submit()

        self.assertIn(
            "cheese", self.driver.find_element_by_id("product_found").text
        )
        logging.info("cheese found")
        print("cheese found")
        # We go to the product's page
        self.driver.find_element_by_id(f"details{1}").click()

        self.assertIn(
            "Nutriscore", self.driver.find_element_by_id("nutriscore_h3").text
        )
        logging.info("On coleslaw details page")
        print("On coleslaw details page")
        # We go to its Open Food Facts page
        self.driver.execute_script("document.getElementById('offacts_link').click()")
        logging.info("Offact linked worked for cheese")
        print("Offact linked worked for cheese")
        # We go back to the results
        self.driver.execute_script("window.history.go(-2)")
        logging.info("Back to results page (cheese)")
        print("Back to results page (cheese)")
        # We add the products to our favourites
        self.driver.find_elements_by_class_name("add_to_fav")[0].click()
        logging.info("One product is now a favourite")
        print("One product is now a favourite")
        # We go to the favourites page
        self.driver.get(f"{self.live_server_url}/roles/favourites")
        self.assertIn(
            "VOS FAVORIS", self.driver.find_element_by_tag_name("h1").text
        )
        logging.info("On favs page")
        print("On favs page")
        # We unlike the product and go back to th results
        self.driver.find_elements_by_class_name("unlike_form")[0].submit()
        logging.info("Favourite deleted")
        print("Favourite deleted")
        self.driver.execute_script("window.history.go(-2)")
        # This is because of the browser's cache
        self.driver.refresh()
        # We log out
        self.driver.get(f"{self.live_server_url}/roles/signin/")
        # submit
        self.assertIn(
            "CONNEXION", self.driver.find_element_by_tag_name("h1").text
        )
        logging.info("On deconnection page")
        print("On deconnection page")
        self.driver.execute_script("document.getElementById('logout_btn').click()")
        logging.info("Logged out")
        print("Logged out")
        # We close the browser.
        self.driver.close()
