# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Testappweb(unittest.TestCase):
    def setUp(self):
        #added so that chrome browser dosen't close when a test is over
        opts = ChromeOptions()
        opts.add_experimental_option("detach",True)
        self.driver = webdriver.Chrome(options=opts)
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:5000/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_login(self):
        driver = self.driver
        driver.get(self.base_url)

        #driver.find_element_by_id("username").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("cisco")

        #driver.find_element_by_id("password").click()
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("class")
        driver.find_element_by_id("password").send_keys(Keys.ENTER)

        # Warning: verifyTextPresent may require manual changes only works on webdriver.Chrome()
        #try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*cisco[\s\S]*$") #gave warnings switched to assertRegex
        try: self.assertRegex(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*cisco[\s\S]*$")
        except AssertionError as e: self.verificationErrors.append(str(e))
        time.sleep(1)
        driver.find_element_by_link_text("Log Off").click()
        try:
            self.assertRegex(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*You successfully signed out[\s\S]*$")
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        time.sleep(1)


    """def test_logout(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text("Log Off").click()"""

    def test_loginfailure(self):
        driver = self.driver
        driver.get(self.base_url)
        #driver.find_element_by_id("username").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("JohnDoe")
        #driver.find_element_by_id("password").click()
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("Howcouldthispasswordbeanylongerormorepompus")
        driver.find_element_by_id("password").send_keys(Keys.ENTER)
        try:
            self.assertRegex(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*Authentication failed. Please try again.[\s\S]*$")
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        time.sleep(1)

    def test_blocking(self):
        driver = self.driver
        driver.get(self.base_url)

        if driver.title == "index":
            driver.find_element_by_link_text("Log Off").click()

        driver.get(self.base_url) #try access Index page without logging in
        self.assertEqual("Login", driver.title)
        #driver.find_element_by_id("username").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("cisco")
        #driver.find_element_by_id("password").click()
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("class")
        driver.find_element_by_id("password").send_keys(Keys.ENTER)
        time.sleep(1)
        driver.get(self.base_url+"GCU")
        time.sleep(1)
        # Warning: verifyTextPresent may require manual changes
        try:
            self.assertRegex(driver.find_element_by_css_selector("BODY").text,
                                     r"^[\s\S]*You are not authorized to access this page![\s\S]*$")
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        time.sleep(1)

    def test_admincreateuser(self):
        driver = self.driver
        driver.get(self.base_url)
        time.sleep(1)
        #driver.find_element_by_id("username").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")

        #driver.find_element_by_id("password").click()
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("admin123")
        driver.find_element_by_id("password").send_keys(Keys.ENTER)

        # Warning: verifyTextPresent may require manual changes
        try:
            self.assertRegex(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*admin[\s\S]*$")
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        # Warning: verifyTextPresent may require manual changes
        try:
            self.assertRegex(driver.find_element_by_css_selector("BODY").text,
                                     r"^[\s\S]*Create Account[\s\S]*$")
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Create Account").click()
        #driver.find_element_by_id("username").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("test2")

        #driver.find_element_by_id("passw").click()
        driver.find_element_by_id("passw").clear()
        driver.find_element_by_id("passw").send_keys("test123")

        driver.find_element_by_name("submitcreateUser").click()
        # Warning: verifyTextPresent may require manual changes

        try:
            self.assertRegex(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*Successful[\s\S]*$")
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        time.sleep(1)
        driver.find_element_by_link_text("Main Page").click()
        driver.find_element_by_link_text("Log Off").click()
        # Warning: verifyTextPresent may require manual changes
        try:
            self.assertRegex(driver.find_element_by_css_selector("BODY").text,
                                     r"^[\s\S]*You successfully signed out[\s\S]*$")
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        time.sleep(1)


    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit() #the browser will close after test is finished
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
