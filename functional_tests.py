from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Safari()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # name has to start with test to run by test runner
        # User opens to-do list website
        self.browser.get("http://localhost:8000")

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
        input_box.send_keys('Buy Gopher plush')
        # when the user hits enter, the page updates
        input_box.send_keys(Keys.ENTER)
        # make sure browser has finished loading before asserting about new page
        time.sleep(2)

        # and the page lists "1: buy gopher plush" as in item in a to-do list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy Gopher plush' for row in rows)
        )
        # There is still a textbox inviting the user to enter text
        # they enter "buy python shirt"
        self.fail('Finish the test!')
    # the site has generated a unique URL for the user, they can visit it for persistance


if __name__ == '__main__':
    unittest.main(warnings='ignore')
