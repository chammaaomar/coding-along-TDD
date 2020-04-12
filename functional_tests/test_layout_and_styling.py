from functional_tests.base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # she visits the website
        self.browser.get(self.live_server_url)

        # using 2013 macbook air in full screen
        self.browser.set_window_size(1920, 1080)

        # she sees the input box in the middle
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2, 960, delta=10)

        # she adds an element
        self.input_item('Learn Nim and implement toy Docker')
        self.check_for_row_in_list_table(
            '1: Learn Nim and implement toy Docker')
        inputbox = self.browser.find_element_by_id('id_new_item')
        # and notices the input box is still nicely centered
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 960, delta=10)
