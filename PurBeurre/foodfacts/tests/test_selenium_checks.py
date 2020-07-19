"""
This file is used to test the functionalities in the browser.
It will use Selenium.
"""
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class MySeleniumTests(StaticLiveServerTestCase):
    """
    This class provides a configuration and a set of actions to
    simulate the behaviour of a human user.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(30000)

    def test_browser(self):
        """
        This contains the list of actions to perform in the browser,
         the order in which Selenium executes them and the assertions to test.
        """
        # First we go full screen
        self.driver.maximize_window()
        # Then we go on the website
        self.driver.get("http://localhost:8000/foodfacts/")
        self.assertIn(
            "GRAS", self.driver.find_element_by_id(
                "main_title").text)

        # Then we go on the sigin page
        self.driver.get("http://localhost:8000/roles/signin/")
        self.assertIn(
            "CONNEXION", self.driver.find_element_by_tag_name(
                "h1").text)
        # We sign in
        signin_email = self.driver.find_element_by_name("email")
        signin_email.send_keys("monami@gmail.com")
        signin_password = self.driver.find_element_by_name("password")
        signin_password.send_keys("Niam1989")
        self.driver.find_element_by_xpath('//input[@type="submit"]').click()

        self.assertIn(
            "Editez", self.driver.find_element_by_id("sub_title").text
        )

        # We look for a product
        search_navbar_input = self.driver.find_element_by_id("nav_input")
        self.driver.execute_script("document.getElementById('nav_input').value = 'Coleslaw'")
        search_navbar_input.submit()

        self.assertIn(
            "Coleslaw", self.driver.find_element_by_id("product_found").text
        )

        # We go to the product's page
        self.driver.find_element_by_id(f"details{1}").click()

        self.assertIn(
            "Nutriscore", self.driver.find_element_by_id("nutriscore_h3").text
        )
        # We go to its Open Food Facts page
        self.driver.execute_script("document.getElementById('offacts_link').click()")

        # We go back to the results
        self.driver.execute_script("window.history.go(-2)")
        # We add the products to our favourites
        self.driver.find_elements_by_class_name("add_to_fav")[0].click()
        # We go to the favourites page
        self.driver.get("http://localhost:8000/roles/favourites")
        self.assertIn(
            "VOS FAVORIS", self.driver.find_element_by_tag_name("h1").text
        )
        # We unlike the product and go back to th results
        self.driver.find_elements_by_class_name("unlike_form")[0].submit()
        self.driver.execute_script("window.history.go(-2)")
        # This is because of the browser's cache
        self.driver.refresh()
        # We log out
        self.driver.get("http://localhost:8000/roles/signin/")
        # submit
        self.assertIn(
            "CONNEXION", self.driver.find_element_by_tag_name("h1").text
        )

        self.driver.execute_script("document.getElementById('logout_btn').click()")
        # We close the browser.
        self.driver.close()
