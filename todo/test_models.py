from django.test import TestCase
from django.shortcuts import get_object_or_404
from .models import Item

# Create your tests here.
class TestModels(TestCase):

    def test_done_defaults_to_false(self):
        item = Item(name="Create a Test")
        item.save()
        self.assertEqual(item.name, "Create a Test")
        self.assertFalse(item.done)

    def test_can_create_an_item_with_a_name_and_status(self):
        item = Item(name="Create a Test", done="True")
        item.save()
        self.assertEqual(item.name, "Create a Test")
        self.assertTrue(item.done)

    def test_item_as_a_string(self):
        item = Item(name="Create a Test")
        self.assertEqual("Create a Test", str(item))

    def test_post_create_an_item(self):
        response = self.client.post("/add", {"name": "Create a Test"})
        item = get_object_or_404(Item, pk=1)
        self.assertEqual(item.done, False)

    def test_post_edit_an_item(self):
        item = Item(name="Create a Test")
        item.save()
        id = item.id

        response = self.client.post("/edit/{0}".format(id), {"name": "A different name"})
        item = get_object_or_404(Item, pk=1)
        self.assertEqual("A different name", item.name)

    def test_toggle_status(self):
        item = Item(name="Create a Test")
        item.save()
        id = item.id

        response = self.client.post("/toggle/{0}".format(id), {"name": "A different name"})
        item = get_object_or_404(Item, pk=1)
        self.assertEqual(item.done, True)