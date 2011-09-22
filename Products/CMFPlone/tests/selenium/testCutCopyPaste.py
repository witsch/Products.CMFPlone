import unittest2 as unittest
from plone.app.testing.selenium_layers import SELENIUM_PLONE_FUNCTIONAL_TESTING
from plone.app.testing.selenium_layers import login, click
from plone.app.testing.helpers import applyProfile

class TestCutPaste(unittest.TestCase):
    layer = SELENIUM_PLONE_FUNCTIONAL_TESTING

    def setUp(self):
        self.driver = self.layer['selenium']
        self.portal = self.layer['portal']
        self.driver.implicitly_wait(5)

        self.portal.acl_users._doAddUser('member1', 'secret',
                                         ['Member'], [])
        applyProfile(self.layer['portal'], 'Products.CMFPlone:plone-selenium')

    def test_cut_and_paste(self):
        login(self.driver,self.portal,'member1','secret')
        click(self.driver, "link=Folder 1")
        click(self.driver, "link=Contents")
        click(self.driver, "#cb_folder-3")
        click(self.driver, "folder_cut:method")
        click(self.driver, "link=Folder 2")
        click(self.driver, "link=Contents")
        click(self.driver, "folder_paste:method")

    def test_copy_and_paste(self):
        login(self.driver,self.portal,'member1','secret')
        click(self.driver, "link=Folder 1")
        click(self.driver, "link=Contents")
        click(self.driver, "#cb_folder-3")
        click(self.driver, "folder_copy:method")
        click(self.driver, "link=Folder 2")
        click(self.driver, "link=Contents")
        click(self.driver, "folder_paste:method")


import time
from plone.seleniumtesting.homepage import HomePage
from plone.seleniumtesting.folderpageobject import FolderPageObject

class TestCutPasteUsingPageObjects(unittest.TestCase):
    layer = SELENIUM_PLONE_FUNCTIONAL_TESTING

    def setUp(self):
        self.driver = self.layer['selenium']
        self.portal = self.layer['portal']
        self.driver.implicitly_wait(5)

        self.hp = HomePage(self.driver, self.portal)

        self.portal.acl_users._doAddUser('member1', 'secret',
                                         ['Member'], [])
        applyProfile(self.layer['portal'], 'Products.CMFPlone:plone-selenium')

    def test_cut_and_paste_using_pageobjects(self):
        login(self.driver,self.portal,'member1','secret')
        self.hp.open_default_url()
        self.driver.find_element_by_partial_link_text('Folder 1').click()

        fpo = FolderPageObject(self.driver)
        folder_contents = fpo.goto_contents_tab()
        folder_contents.selectFolderItemByPostition(0)
        folder_contents.cut()

        #ToDo verify cut
        
        self.driver.find_element_by_partial_link_text('Folder 2').click()
        folder_contents = fpo.goto_contents_tab()
        folder_contents.paste()

        #ToDo verify pasted
        
    def test_copy_and_paste_using_pageobjects(self):
        login(self.driver,self.portal,'member1','secret')
        self.hp.open_default_url()
        self.driver.find_element_by_partial_link_text('Folder 1').click()

        fpo = FolderPageObject(self.driver)
        folder_contents = fpo.goto_contents_tab()
        folder_contents.selectFolderItemByPostition(0)
        folder_contents.copy()

        #ToDo verify copy
        
        self.driver.find_element_by_partial_link_text('Folder 2').click()
        folder_contents = fpo.goto_contents_tab()
        folder_contents.paste()

        #ToDo verify pasted
