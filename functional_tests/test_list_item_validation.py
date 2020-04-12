from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_item(self):
        self.browser.get(self.live_server_url)

        # she tries to input an empty element
        self.input_item('')
        # the browser does not let her
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # she enters a valid element; and shows up on her screen
        self.input_item('Practice for behavioral interview')
        self.wait_for(self.check_for_row_in_list_table,
                      '1: Practice for behavioral interview')

        # just to assure, she tries to enter another empty element
        self.input_item('')
        # and the browser again does not let her
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # she tries to input another valid element, and she sees all her elements
        self.input_item('Get better at Django')
        self.wait_for(self.check_for_row_in_list_table,
                      '1: Practice for behavioral interview')
        self.wait_for(self.check_for_row_in_list_table,
                      '2: Get better at Django')
