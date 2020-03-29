from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest
from django.test import LiveServerTestCase
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Safari()

    def tearDown(self):
        self.browser.quit()

    def input_item(self, item_text):
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(item_text)
        input_box.send_keys(Keys.ENTER)

    def check_for_row_in_list_table(self, row_text):
        start_time = time.time()
        try:
            table = self.browser.find_element_by_id('id_list_table')
            rows = table.find_elements_by_tag_name('tr')
            self.assertIn(row_text, [row.text.strip() for row in rows])
            return
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # name has to start with test to run by test runner
        # User opens to-do list website
        self.browser.get(self.live_server_url)

        # page title and header mentions to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # user is immediately prompted to enter a to-do item
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # user types "buy gopher plush"
        # when the user hits enter, the page updates
        # make sure browser has finished loading before asserting about new page
        self.input_item('Buy Gopher plush')

        # and the page lists "1: buy gopher plush" as in item in a to-do list
        self.check_for_row_in_list_table('1: Buy Gopher plush')
        # There is still a textbox inviting the user to enter text
        # they enter

        self.input_item('Implement Redis using Go coroutines')

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy Gopher plush')
        self.check_for_row_in_list_table(
            '2: Implement Redis using Go coroutines')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Omar logs on to create a new list and really wants to buy
        # a Gopher plush
        self.browser.get(self.live_server_url)
        self.input_item('Buy Gopher plush')
        self.check_for_row_in_list_table('1: Buy Gopher plush')
        omar_url = self.browser.current_url
        self.assertRegex(omar_url, '/lists/.+')
        # Another user logs in, Sara, and she really wants to buy
        # a Smoko potato lamp, but doesn't share any relation to Omar
        # she gets her own unique URL

        self.browser.quit()
        # re-initialize
        self.browser = webdriver.Safari()

        self.browser.get(self.live_server_url)
        self.input_item('Buy Smoko potato lamp')
        self.check_for_row_in_list_table('1: Buy Smoko potato lamp')
        sara_url = self.browser.current_url
        self.assertRegex(sara_url, '/lists/.+')
        self.assertNotEqual(omar_url, sara_url)

        # and she doesn't see his items
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Gopher plush', page_text)
        self.assertIn('Buy Smoko potato lamp', page_text)
