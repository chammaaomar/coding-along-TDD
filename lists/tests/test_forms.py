from django.test import TestCase
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import List, Item

class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = ItemForm()
        # self.fail(form.as_p())
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertIn(
            EMPTY_ITEM_ERROR,
            form.errors['text']
        )
    
    def test_form_can_save_item(self):
        form = ItemForm(data={
            'text': 'example'
        })
        list_ = List.objects.create()
        posted_item = form.save(for_list = list_)
        item_in_db = Item.objects.first()
        self.assertEqual(posted_item, item_in_db)
        self.assertEqual(item_in_db.list, list_)