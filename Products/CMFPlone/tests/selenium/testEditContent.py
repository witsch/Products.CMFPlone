import unittest2 as unittest
from plone.app.testing.selenium_layers import SELENIUM_PLONE_FUNCTIONAL_TESTING
from plone.app.testing.selenium_layers import login, click, type, clear
from plone.app.testing.helpers import applyProfile

class TestEditContent(unittest.TestCase):
    layer = SELENIUM_PLONE_FUNCTIONAL_TESTING

    def setUp(self):
        self.driver = self.layer['selenium']
        self.portal = self.layer['portal']
        self.driver.implicitly_wait(5)

        self.portal.acl_users._doAddUser('member1', 'secret',
                                         ['Member'], [])
        applyProfile(self.layer['portal'], 'Products.CMFPlone:plone-selenium')

    def test_edit_content(self):
        login(self.driver, self.portal, 'member1','secret')
        click(self.driver, "link=Folder 1")
        click(self.driver, "link=Edit")
        clear(self.driver, "title")
        type(self.driver,  "title", "Some say potato")
        click(self.driver, "form.button.save")
