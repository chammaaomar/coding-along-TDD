from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_item(self):
        self.browser.get(self.live_server_url)

        self.input_item('')
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_class_name('has-error').text,
                'You cannot enter an empty item'
            )
        )

        self.input_item('Practice for behavioral interview')
        self.wait_for(self.check_for_row_in_list_table,
                      '1: Practice for behavioral interview')

        self.input_item('')
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_class_name('has-error').text,
            'You cannot enter an empty item'
        ))
        self.input_item('Get better at Django')
        self.wait_for(self.check_for_row_in_list_table,
                      '1: Practice for behavioral interview')
        self.wait_for(self.check_for_row_in_list_table,
                      '2: Get better at Django')
