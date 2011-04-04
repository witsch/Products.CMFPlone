import os
import unittest2 as unittest
from App.Common import package_home

from plone.app.testing.selenium_layers import SELENIUM_PLONE_FUNCTIONAL_TESTING
from plone.app.testing.selenium_layers import open, login, click, type
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import applyProfile
from plone.app.testing import setRoles


class TinyMCE(unittest.TestCase):
    layer = SELENIUM_PLONE_FUNCTIONAL_TESTING

    def setUp(self):
        self.driver = self.layer['selenium']
        self.portal = self.layer['portal']
        self.driver.implicitly_wait(5)

        self.portal.acl_users._doAddUser('member1', 'secret',
                                         ['Member'], [])
        applyProfile(self.layer['portal'], 'Products.CMFPlone:plone-selenium')

    def testAddImage(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.driver, self.portal, TEST_USER_NAME, TEST_USER_PASSWORD)
        open(self.driver, self.portal.absolute_url()+'/')

        # Add a new collection
        click(self.driver, 'link=Add new')
        click(self.driver, 'link=Page')
        type(self.driver, 'title', 'Image Test')

        click(self.driver, '#text_image')
        self.driver.switch_to_frame('mce_44_ifr')
        click(self.driver, 'upload')

        path = os.path.join(package_home(globals()), 'input', 'test.gif')

        self.driver.find_element_by_id('uploadfile').send_keys(path)
        
        click(self.driver, '#uploadbutton')
        click(self.driver, '#insert')
        click(self.driver, 'form.button.save')

        self.assertIn('test.gif', self.driver.get_page_source())
