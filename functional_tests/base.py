import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Safari()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = f'http://{staging_server}'

    def tearDown(self):
        self.browser.quit()

    def get_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def input_item(self, item_text):
        input_box = self.get_input_box()
        input_box.send_keys(item_text)
        input_box.send_keys(Keys.ENTER)

    def wait_for(self, fn, *args):
        start_time = time.time()
        while True:
            try:
                return fn(*args)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(5)

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text.strip() for row in rows])
