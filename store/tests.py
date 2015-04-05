from django.test import TestCase
from selenium import webdriver
import unittest


class MainPage(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_title(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        self.assertEqual(u"MultyDOM - лучшие товары для дома!!!", driver.find_element_by_id("topText").text)

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()