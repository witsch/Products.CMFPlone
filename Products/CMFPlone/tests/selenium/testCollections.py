import time
import transaction
import unittest2 as unittest

from plone.app.testing.layers import PLONE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing.selenium_layers import SELENIUM_PLONE_FUNCTIONAL_TESTING
from plone.app.testing.selenium_layers import open, login as slogin, click
from plone.app.testing.selenium_layers import type, select
from Products.CMFPlone.tests.selenium.base import SeleniumTestCase

class TestCollections(unittest.TestCase):
    layer = SELENIUM_PLONE_FUNCTIONAL_TESTING

    def setUp(self):
        self.driver = self.layer['selenium']
        self.portal = self.layer['portal']
        self.driver.implicitly_wait(5)
        
        # Set a default workflow for the site
        self.portal.portal_workflow.setDefaultChain('simple_publication_workflow')
        
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        for m in range(1,3):
            self.portal.invokeFactory('Folder', 'folder%s' % m, title='Folder %s' % m)
            for n in range(0,10):
                self.portal['folder%s' % m].invokeFactory('Event', 'event%s' % n, title='Event %s' % n)
        setRoles(self.portal, TEST_USER_ID, ['Member'])

    def test_add_collection(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        slogin(self.driver, self.portal, TEST_USER_NAME, TEST_USER_PASSWORD)
        open(self.driver, self.portal.absolute_url()+'/')

        # Add a new collection
        click(self.driver, 'link=Add new')
        click(self.driver, 'link=Collection')
        
        # Define title, description
        type(self.driver, 'title', 'I am a collection with javascript')
        type(self.driver, 'description', 'skkep skip skop')
        
        # Display as Table
        click(self.driver, '#customView')
        
        # Select all available table columns for viewing
        options = {'CreationDate': 'Creation Date',
                   'Creator': 'Creator',
                   'Description': 'Description',
                   'EffectiveDate': 'Effective Date',
                   'end': 'End Date',
                   'ExpirationDate': 'Expiration Date',
                   'getId': 'Short Name',
                   'getObjSize': 'Size',
                   'location': 'Location',
                   'ModificationDate': 'Modification Date',
                   'review_state': 'State',
                   'start': 'Start Date',
                   'Subject': 'Tags',
                   'Type': 'Item Type'}
        
        for opt in options.keys():
            select(self.driver, "id('customViewFields_options')/option[attribute::value='%s']" % opt)

        click(self.driver, "//input[attribute::value='>>']")
        
        # Save the collection
        click(self.driver, 'form.button.save')

        # Publish it
        click(self.driver, 'link=Private')
        click(self.driver, 'link=Publish')
        time.sleep(1)
        self.assertIn('Published', self.driver.get_page_source())
        
        # Add a title criteria
        click(self.driver, 'link=Criteria')
        select(self.driver, "id('field')/option[attribute::value='Title']")
        click(self.driver, "form.button.AddCriterion")
        type(self.driver, "crit__Title_ATSimpleStringCriterion_value", "Event")
        click(self.driver, "form.button.Save")
        time.sleep(1)
        self.assertTrue("Changes saved." in self.driver.get_page_source())
        
        # View the collection
        click(self.driver, "link=View")
        
        # Check that all table columns requested are displayed
        time.sleep(3)
        for opt in options.values():
            self.assertIn(opt, self.driver.get_page_source())

        # Return the list of results
        def getCollectionResults(self):
            return self.driver.find_elements_by_xpath("//table[attribute::class='listing']/tbody/tr")
        
        # Make sure we find all 20 events
        self.assertEquals(len(getCollectionResults(self)), 20)
        
        