from django.test import TestCase
from .models import Item

# Create your tests here.
class TestViews(TestCase):

    def test_get_home_page(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200) #200 refers to a successful page
        self.assertTemplateUsed(page, "todo_list.html")
    
    def test_get_add_item_page(self):
        page = self.client.get("/add")
        self.assertEqual(page.status_code, 200) #200 refers to a successful page
        self.assertTemplateUsed(page, "item_form.html")

    def test_get_edit_item_page(self):
        """ You have to create an item """
        item = Item(name='Create a Test')
        item.save()
        """ Otherwist the line below wont work """
        page = self.client.get("/edit/{0}".format(item.id))
        self.assertEqual(page.status_code, 200) #200 refers to a successful page
        self.assertTemplateUsed(page, "item_form.html")

    def test_get_edit_page_for_item_that_does_not_exist(self):
        page = self.client.get("/edit/1")
        self.assertEqual(page.status_code, 404) #404 refers to a page not found
