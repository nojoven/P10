"""
This file is used to test the functionalities in the browser.
It will use Selenium.
"""
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from webdriver_manager.chrome import ChromeDriverManager

class MySeleniumTests(StaticLiveServerTestCase):
    """
    This class provides a configuration and a set of actions to
    simulate the behaviour of a human user.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox") 
    options.add_argument("--disable-setuid-sandbox") 

    options.add_argument("--remote-debugging-port=9222")

    options.add_argument("--disable-dev-shm-using") 
    options.add_argument("--disable-extensions") 
    options.add_argument("--disable-gpu") 
    options.add_argument("disable-infobars") 
    options.add_argument("--headless")


    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(24000)

    def test_browser(self):
        """
        This contains the list of actions to perform in the browser,
         the order in which Selenium executes them and the assertions to test.
        """
        # First we go full screen
        self.driver.maximize_window()
        # Then we go on the website
        self.driver.get("https://beurrepur.herokuapp.com/")
        self.assertIn(
            "GRAS", self.driver.find_element_by_id(
                "main_title").text)

        # Then we go on the sigin page
        self.driver.get("https://beurrepur.herokuapp.com/roles/signin/")
        self.assertIn(
            "CONNEXION", self.driver.find_element_by_tag_name(
                "h1").text)
        # We sign in
        signin_email = self.driver.find_element_by_name("signin_email")
        signin_email.send_keys("pujadas@gmail.com")
        signin_password = self.driver.find_element_by_name("signin_password")
        signin_password.send_keys("pujadas")
        self.driver.find_element_by_xpath('//input[@type="submit"]').click()

        self.assertIn(
            "Editez", self.driver.find_element_by_id("sub_title").text
        )
        # We look for a product
        search_navbar_input = self.driver.find_element_by_name("nav_search")
        search_navbar_input.send_keys("Coleslaw")
        search_navbar_input.send_keys("\ue007")

        self.assertIn(
            "Coleslaw", self.driver.find_element_by_id("product_found").text
        )
        # We go to the product's page
        self.driver.find_element_by_id(f"details{1}").click()

        self.assertIn(
            "Nutriscore", self.driver.find_element_by_id("nutriscore_h3").text
        )
        # We go to its Open Food Facts page
        self.driver.find_element_by_name("offacts_link").click()

        # We go back to the results
        self.driver.execute_script("window.history.go(-2)")
        # We add the products to our favourites
        self.driver.find_elements_by_class_name("add_to_fav")[0].submit()
        # We go to the favourites page
        self.driver.get("https://beurrepur.herokuapp.com/roles/favourites")
        self.assertIn(
            "VOS FAVORIS", self.driver.find_element_by_tag_name("h1").text
        )
        # We unlike the product and go back to th results
        self.driver.find_elements_by_class_name("unlike_form")[0].submit()
        self.driver.execute_script("window.history.go(-2)")
        # This is because of the browser's cache
        self.driver.refresh()
        # We log out
        self.driver.get("https://beurrepur.herokuapp.com/roles/signin/")
        # submit
        self.assertIn(
            "CONNEXION", self.driver.find_element_by_tag_name("h1").text
        )
        self.driver.find_elements_by_class_name("logout_form")[0].submit()
        # We close the browser.
        self.driver.close()
