from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Safari()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # name has to start with test to run by test runner
        # User opens to-do list website
        self.browser.get("http://localhost:8000")

        # page title mentions to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the Test!')

    # user is immediately prompted to enter a to-do item

    # user types "buy gopher plush"

    # when the user hits enter, the page updates, and the page
    # lists "1: buy gopher plush" as in item in a to-do list

    # There is still a textbox inviting the user to enter text
    # they enter "buy python shirt"

    # the site has generated a unique URL for the user, they can visit it for persistance


if __name__ == '__main__':
    unittest.main(warnings='ignore')
