from django.urls import resolve
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item, List
# Create your tests here.


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        # check what template was used to render the response
        self.assertTemplateUsed(response, 'home.html')


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        # for every unit test case, Django sets up a database instance
        response = self.client.post(
            '/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'A new list item')

    def test_redirect_after_POST(self):
        # redirect after a POST request to allow safe refresh
        response = self.client.post(
            '/lists/new', data={'item_text': 'A new list item'})
        list_ = List.objects.first()
        self.assertRedirects(response, f'/lists/{list_.id}/')

    def test_validation_errors_are_sent_back_to_home_page(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = 'You cannot enter an empty item'
        self.assertContains(response, expected_error)

    def test_invalid_list_items_are_not_saved(self):
        item = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(List.objects.count(), 0)


class ListViewTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(f'/lists/{list_.id}/', list_.get_absolute_url())

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_items_for_that_list_only(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Item 1', list=correct_list)
        Item.objects.create(text='Item 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='Another item 1', list=other_list)
        Item.objects.create(text='Another item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'Item 1')
        self.assertNotContains(response, 'Another item 1')
        self.assertContains(response, 'Item 2')
        self.assertNotContains(response, 'Another item 2')

    def test_passes_correct_list_to_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertEqual(response.context.get('list', None), list_)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.id}/', {
            'item_text': 'A new item for an existing list'
        })
        item = Item.objects.first()
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(item.text, 'A new item for an existing list')
        self.assertEqual(list_, item.list)

    def test_POST_redirects_to_list_view(self):
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.id}/', {
            'item_text': 'A new item for an existing list'
        })
        self.assertRedirects(response, f'/lists/{list_.id}/')

    def test_cannot_POST_empty_item_to_existing_list(self):
        list_ = List.objects.create()
        response = self.client.post(
            f'/lists/{list_.id}/', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You cannot enter an empty item')
        self.assertTemplateUsed(response, 'list.html')
