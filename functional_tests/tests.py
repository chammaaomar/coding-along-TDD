from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from django.test import LiveServerTestCase
import time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Safari()

    def tearDown(self):
        self.browser.quit()

    def input_item(self, item_text):
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(item_text)
        input_box.send_keys(Keys.ENTER)
        time.sleep(3)

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text.strip() for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
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

        self.fail('Finish the test!')

    # the site has generated a unique URL for the user, they can visit it for persistance
