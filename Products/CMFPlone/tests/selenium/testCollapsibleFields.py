import time
import unittest2 as unittest

from plone.app.testing.selenium_layers import SELENIUM_PLONE_FUNCTIONAL_TESTING
from plone.app.testing.selenium_layers import open, click, select

class TestCollapsibleFileds(unittest.TestCase):
    layer = SELENIUM_PLONE_FUNCTIONAL_TESTING

    def setUp(self):
        self.driver = self.layer['selenium']
        self.portal = self.layer['portal']
        self.driver.implicitly_wait(5)
        
    def test_collapsible_fields(self):

        open(self.driver, self.portal.absolute_url()+'/search_form')    

        # verify fields are collapsed when 'Advanced Search Form' opened
        # ... Item type
        self.assertFalse(self.driver.find_element_by_id('pt_toggle').is_displayed())
        listedItemTypes = self.driver.find_elements_by_name('portal_type:list')
        for listedType in listedItemTypes:
            self.assertFalse(listedType.is_displayed())

        # ... New items since
        self.assertFalse(self.driver.find_element_by_id('created').is_displayed())
        # ... Author
        self.assertFalse(self.driver.find_element_by_name('Creator').is_displayed())

        # expand fields
        cfields = self.driver.find_elements_by_class_name('collapser collapsed')
        for cfield in cfields:
            cfield.click()
    
        time.sleep(1)

        # verify fields are now expanded
        # ... Item type
        self.assertTrue(self.driver.find_element_by_id('pt_toggle').is_displayed())
        listedItemTypes = self.driver.find_elements_by_name('portal_type:list')
        for listedType in listedItemTypes:
            self.assertTrue(listedType.is_displayed())
        
        # ... New items since
        self.assertTrue(self.driver.find_element_by_id('created').is_displayed())
        # ... Author
        self.assertTrue(self.driver.find_element_by_name('Creator').is_displayed())

        # re-collapse fields
        cfields = self.driver.find_elements_by_class_name('collapser expanded')
        for cfield in cfields:
            cfield.click()

        time.sleep(1)
        
        # verify fields are collapsed again
        # ... Item type
        self.assertFalse(self.driver.find_element_by_id('pt_toggle').is_displayed())
        listedItemTypes = self.driver.find_elements_by_name('portal_type:list')
        for listedType in listedItemTypes:
            self.assertFalse(listedType.is_displayed())
        
        # ... New items since
        self.assertFalse(self.driver.find_element_by_id('created').is_displayed())
        # ... Author
        self.assertFalse(self.driver.find_element_by_name('Creator').is_displayed())
