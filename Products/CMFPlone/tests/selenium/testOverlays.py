import time
import unittest2 as unittest
from plone.app.testing.selenium_layers import SELENIUM_PLONE_FUNCTIONAL_TESTING
from plone.app.testing.selenium_layers import open, login, click, type
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing.helpers import applyProfile
from selenium.webdriver.common.exceptions import NoSuchElementException

class TestOverlays(unittest.TestCase):
    layer = SELENIUM_PLONE_FUNCTIONAL_TESTING
    
    def setUp(self):
        self.driver = self.layer['selenium']
        self.portal = self.layer['portal']
        self.driver.implicitly_wait(5)

        self.portal.acl_users._doAddUser('member1', 'secret',
                                         ['Member'], [])
        applyProfile(self.layer['portal'], 'Products.CMFPlone:plone-selenium')

    def test_login_form(self):
        # Make sure we're logged out before starting
        open(self.driver, "%s%s" % (self.portal.absolute_url(),'/logout'))
        open(self.driver, self.portal.absolute_url())
        time.sleep(3)
        
        click(self.driver, 'link=Log in')
        type(self.driver, '__ac_name', 'wrong')
        type(self.driver, '__ac_password', 'fail')
        click(self.driver, 'submit')
        self.assertIn('Login failed.', self.driver.get_page_source())
        
        type(self.driver, '__ac_name', TEST_USER_NAME)
        type(self.driver, '__ac_password', TEST_USER_PASSWORD)
        click(self.driver, 'submit')
        
        self.assertEquals(TEST_USER_ID, self.driver.find_element_by_id('user-name').text)
        
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, 'login_form')
        
        