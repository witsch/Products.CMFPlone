import unittest2 as unittest
from plone.app.testing.selenium_layers import SELENIUM_PLONE_FUNCTIONAL_TESTING
from plone.app.testing.selenium_layers import open, login, click
from plone.app.testing.selenium_layers import type, typeMce, clear, select
from plone.app.testing.helpers import applyProfile
import time

class TestPortlets(unittest.TestCase):    
    layer = SELENIUM_PLONE_FUNCTIONAL_TESTING
    
    def setUp(self):
        self.driver = self.layer['selenium']
        self.portal = self.layer['portal']
        self.driver.implicitly_wait(5)

        self.portal.acl_users._doAddUser('member1', 'secret',
                                         ['Member'], [])
        applyProfile(self.layer['portal'], 'Products.CMFPlone:plone-selenium')
    
    def test_add_static_portlet(self):
        self.portal.acl_users._doAddUser('manager', 'secret', ['Manager'], [])
        login(self.driver, self.portal, 'manager', 'secret')
        open(self.driver, self.portal.absolute_url()+'/')
        # create a test folder
        click(self.driver, "//dl[@id='plone-contentmenu-factories']/dt/a")
        click(self.driver, "#folder")
        type(self.driver,  "title", "test")
        click(self.driver, "form.button.save")
        click(self.driver, "link=Manage portlets")
        
        # add a static header portlet
        select(self.driver, "//option[attribute::value='/++contextportlets++plone.rightcolumn/+/plone.portlet.static.Static']")
        typeMce(self.driver, "nom nom nom")
        type(self.driver,  "form.header", "Better Header")
        type(self.driver,  "form.footer", "I'll eat pancakes on your grave")
        click(self.driver, "form.actions.save")
        click(self.driver, "link=test")
        
        # confirm that the portlet is there
        assert(self.driver.find_element_by_class_name('portlet-static-better-header'))
        click(self.driver, "link=Manage portlets")
        # block nav portets
        select(self.driver, "//div[@id='portletmanager-plone-rightcolumn']/div[3]/form/div[1]/select", "label=Block")
        click(self.driver, "//div[@id='portletmanager-plone-rightcolumn']/div[3]/form/div[4]/input") # save
        
        # add navigation portlet at root
        click(self.driver, "//span[@id='breadcrumbs-home']/a")
        click(self.driver, "link=Manage portlets")
        select(self.driver, "//option[attribute::value='/++contextportlets++plone.rightcolumn/+/portlets.Navigation']")
        
        # not sure why but it seems that I need to put a pause in here for
        # this to work
        time.sleep(2)
        
        type(self.driver,  "form.name", "Navigation Station")
        clear(self.driver, 'form.topLevel')
        type(self.driver,  "form.topLevel", "0")
        click(self.driver, "form.actions.save")
        click(self.driver, "link=Home")
        assert(self.driver.find_element_by_class_name('portletNavigationTree'))
        click(self.driver, "link=test")
        assert(not self.driver.find_elements_by_class_name('portletNavigationTree'))
        
        # edit an existing portlet
        click(self.driver, "link=Manage portlets")
        click(self.driver, "link=Better Header")
        click(self.driver, "form.omit_border")
        click(self.driver, "form.actions.save")
        click(self.driver, "link=test")
        # this path doesn't exist with a border turned on
        assert(self.driver.find_elements_by_xpath("//div[@class='portletStaticText portlet-static-better-header']/p"))
        
