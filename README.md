# Starting

Installed Django with

sudo pip3 install django==1.11.24

# Running Server on VSCode

python3 manage.py runserver

# Create App

django-admin startapp [app name]

# Add Webpages

add these liens to "views.py"

def get_todo_list(request):
    return render(request, "[webpage]")

# Modify urls.py

from [foldername].views import [whatever def is]

### Example

from todo.views import get_todo_list

## Modify urlpatterns

url(r'^$', [whatever def is] )

# Fixing the fail

## goto settings.py

Find INSTALLED_APPS = [

and add the [folder name] to the bottom of the list.

### Example

'todo'

# Using SQLite in VSCode

use the command palette

'sqlite: open database'
then the 'db.sqlite3' file

# Migrate the table to fix the red text when running the server

'python3 manage.py migrate'

# Create Superuser

'python3 manage.py createsuperuser'

# Modals

find the models.py

class Item(models.model):
    name = models.CharField(max_length=30, blank=False) <--Charfield is a text field, blank is the same as null
    done = models.BooleanField(blank=False, default=False)

## Makemigration

python3 manage.py makemigrations
python3 manage.py migrate


## Add to Admin.py

from .models import Item

# Register your models here.
admin.site.register(Item)

After python3 manage.py runserver

goto /admin

and the todo list will be there, add 3 items and then they will appear as item object

# Make it readable to a human.

add this to models.py to actually display what the task is

    def __str__(self):
        return self.name

# Rendering Data

goto views.py

add this line

from .models import Item

then change the def to

def get_todo_list(request):
    results = Item.objects.all()
    return render(request, "todo_list.html", {'items':results})

# Make a Table in todo_list.html

<table>
        {% for item in items %}
        <tr>
                        {% if item.done %}
            <td><strike>{{ item.name }}</strike></td>
            {% else %}
            <td>{{ item.name }}</td>
            {% endif %}
        </tr>
        {% endfor %}
    </table>

# If there are no items in the for loop

add this 

        {% empty %}
        <p>You have nothing to do.</p>

so it should look like this 

<table>
        {% for item in items %}
        <tr>
            {% if item.done %}
            <td><strike>{{ item.name }}</strike></td>
            {% else %}
            <td>{{ item.name }}</td>
            {% endif %}
        </tr>
        {% empty %}
        <p>You have nothing to do.</p>
        {% endfor %}
    </table>

# Create an Item

added the bottom of the table in todo_list.html

<a href="add">Add an Item</a>

## Create new Item Form Page

so in templates make a new file called "item_form.html"

## Add Route to views.py

def create_an_item(request):
    return render(request, "item_form.html")

## Update url.py

from todo.views import get_todo_list, create_an_item

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', get_todo_list ),
    url(r'^add$', create_an_item)
]

## Add form to item_form.html

<form method="POST">
        <label for="id_name">Name:</label>
        <input type="text" name="name" id="id_name"><br>
        <label for="id_done">Done:</label>
        <input type="checkbox" name="done" id="id_done"><br>
        <button type="submit">Save</button>
    </form>

This will fail when you use the form to add an item you need to add {% csrf_token %} to just before the start of the form

## The form cant handle data till we add this to views.py

UPDATE:> from django.shortcuts import render, HttpResponse, redirect

UPDATE ROUTE:>
def create_an_item(request):
    if request.method=="POST":
        new_item = Item()
        new_item.name = request.POST.get("name")
        new_item.done = "done" in request.POST
        new_item.save()
        return redirect(get_todo_list)
    return render(request, "item_form.html")

# Creating Forms in DJango

create a new file called forms.py in "todo" folder.

then add this code

from django import forms
from .models import [model name]

class [model name]Form(forms.ModelForm):
    class Meta:
        model = [model name]
        fields = (['field 1'], ['field 2'])

so it looks like this

from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'done')


## Update item_form.html

add {{  form  }}

under the token, remove all other code except the submit button.

## Update views.py

Update:> routing in view.py

def create_an_item(request):
    if request.method=="POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect(get_todo_list)
    else:
        form = ItemForm()
    return render(request, "item_form.html", {'form': form})

## Add Test Data

add form test and done is checked, there cant be any blanks as django is required by default.

## Change from an inline form to block form

add .as_p to the double form brace in item_form.html
{{  form.as_p  }}

# Edit Items

Update the form in todo_list.html

add the code below the endif
            <td>
                <form method="GET" action="edit/{{ item.id }}"><input type="submit" value="Edit"></form>
            </td>

this creates a submit button called edit so that you can edit the item.

   <table>
        {% for item in items %}
        <tr>
            {% if item.done %}
            <td><strike>{{ item.name }}</strike></td>
            {% else %}
            <td>{{ item.name }}</td>
            {% endif %}
             <td>
                <form action="toggle/{{ item.id }}" method="post">
                    {% csrf_token %}
                    <input type="submit" value="Toggle">
                </form>
            </td>
        </tr>
        {% empty %}
        <p>You have nothing to do.</p>
        {% endfor %}
    </table>

## Update views.py

add this route

    def edit_an_item(request, id):
    item =get_object_or_404(Item, pk=id)
    form = ItemForm(instance=item)
    return render(request, "item_form.html", {'form': form})

Dont forget to update top of file

from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

## Update url.py

from todo.views import get_todo_list, create_an_item, edit_an_item

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', get_todo_list ),
    url(r'^add$', create_an_item),
    url(r'^edit/(?P<id>\d+)$', edit_an_item)
]

### What its doing

'^edit/
(?P <- Tells computer its an expression
<id> <- Identifies where its looking
\d+)$' <- Looking for multiple digits

## Does actually update the information

the reason is that there is no method.

so you have to add this to the view.py

    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
        return redirect(get_todo_list)
    else:
        form = ItemForm(instance=item)

FULL CODE:>

def edit_an_item(request, id):
    item =get_object_or_404(Item, pk=id)

    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
        return redirect(get_todo_list)
    else:
        form = ItemForm(instance=item)
        
    return render(request, "item_form.html", {'form': form})


# Toggle Item

## Update todo_list.html

With a form and toggle submit button.

<td>
                <form action="toggle/{{ item.id }}" method="post">
                    <input type="submit" value="Toggle">
                </form>
            </td>

## Update views.py

def toggle_status(request, id):
    item =get_object_or_404(Item, pk=id)
    item.done = not item.done
    item.save()
    return redirect(get_todo_list)

This basically toggles been done and undone and done.

## Update urls.py

from todo.views import get_todo_list, create_an_item, edit_an_item, toggle_status

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', get_todo_list ),
    url(r'^add$', create_an_item),
    url(r'^edit/(?P<id>\d+)$', edit_an_item),
    url(r'^toggle/(?P<id>\d+)$', toggle_status)
]

# Testing Django

## Update tests.py

Updating with a test case

class TestDjango(TestCase):

    def test_is_this_thing_on(self):
        self.assertEqual(1, 0)


This will fail because its because looking for true but it will return false.

Use this command to run the test
python3 manage.py test

# Specific Testing

Rename tests.py to test_forms.py
Create test_views.py
Create test_models.py

## Form Tests

from django.test import TestCase
from .forms import ItemForm

# Create your tests here.
class TestToDoItemForm(TestCase):

    def test_can_create_an_item_with_just_a_name(self):
        form = ItemForm({'name': 'Create Tests'})
        self.assertTrue(form.is_valid())

    def test_correct_message_for_missing_name(self):
        form = ItemForm({'name': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [u'This field is required.'])

## View Tests

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

## Model Tests

from django.test import TestCase
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

# Coverage

## Install Coverage

'sudo pip3 install coverage'

## To Run

'coverage run manage.py test'

## View Report

'coverage report'

## Coverage only the todo folder

'coverage run --source=todo manage.py test'
'coverage report'

## Using Coverage to generate HTML
'coverage html'

Open up the index.html to view the contents.

If you click on models, it shows us we are missing a test.

## Update test_models.py

    def test_item_as_a_string(self):
        item = Item(name="Create a Test")
        self.assertEqual("Create a Test", str(item))

## Update our coverage

'coverage run --source=todo manage.py test'
'coverage html'

Then just refresh the page to see that it passes.

## Updating test_views.py

This is showing we are missing many tests.

The first one is form submissions.

def test_post_create_an_item(self):
        response = self.client.post("/add", {"name": "Create a Test"})
        item = get_object_or_404(Item, pk=1)
        self.assertEqual(item.done, False)

dont forget to add

from django.shortcuts import get_object_or_404

to line 2

## Update our coverage

'coverage run --source=todo manage.py test'
'coverage html'


## Two more Tests

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

## Update our coverage

'coverage run --source=todo manage.py test'
'coverage html'

# Testing apps.py

from django.apps import apps
from django.test import TestCase
from .apps import TodoConfig

# Create your tests here.
class TestTodoConfig(TestCase):

    def test_app(self):
        self.assertEqual("todo", TodoConfig.name)
        self.assertEqual("todo", apps.get_app_config("todo").name)

## Update our coverage

'coverage run --source=todo manage.py test'
'coverage html'

# Setting up Heroku

'heroku'

This opens up the toolbelt

'heroku apps'

This shows all the apps I have created

## Installing add-ons

'sudo pip3 install gunicorn'
'sudo pip3 install psycopg2'

### Note for Home Brew, had to install using 
brew install postgresql

#### Homebrew Commands
==> postgresql
To migrate existing data from a previous major version of PostgreSQL run:
  brew postgresql-upgrade-database

To have launchd start postgresql now and restart at login:
  brew services start postgresql
Or, if you don't want/need a background service you can just run:
  pg_ctl -D /usr/local/var/postgres start

## Requirements File

'pip3 freeze --local > requirements.txt'

# Create App in Heroku

heroku create [Unique app name] --region eu

heroku create my-simple-sjj-django-todo --region eu

'git remote -v'   <- Shows us how it is linked to github etc

# Create Datebase in Heroku

'heroku addons:create heroku-postgresql:hobby-dev'

# Get Database Address

The Database address can be found with

'heroku config'

'postgres://icecexwonfgiua:7f61809d102fd0bce9247a72a61f69b249de386035bdc65f7a672be40c29cd8a@ec2-54-246-89-234.eu-west-1.compute.amazonaws.com:5432/dd4bhelqq7bgjs'

Need to install 
'sudo pip3 install dj_database_url'

Update requirements
'pip3 freeze --local > requirements.txt'

## Update settings.py

Comment out the original DATABASES (line 77)

Create our own Database (line 84)

DATABASES = {'default': dj_database_url.parse("[database address]")}

Add this to line 14
'import dj_database_url'

## Time to Migrate

'python3 manage.py migrate'

# Attempting a First Deployment

'git push heroku master'

This will fail because of 

heroku config:set DISABLE_COLLECTSTATIC=1

## Fix for the previous error

Type this into the terminal

'heroku config:set DISABLE_COLLECTSTATIC=1'

Try

'git push heroku master'

This will now push to Heroku, however we don't have a procfile.

## Creation of Procfile

'echo web: gunicorn django_todo.wsgi:application > Procfile'

Try

'git push heroku master'

# Fix Allowed Hosts

We have to fix the security issue.

open the settings.py

and under the ALLOWED_HOSTS, we need to add the app name which in this case is
'my-simple-sjj-django-todo.herokuapp.com'

Then push to github and then push to heroku

# Setting up Enviro Variables

in the settings.py

## Database

Modify the DATABASE line to

'DATABASES = {'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))}'

This will get the DATABASE_URL from Heroku that we setup this on LINE 617

## HOSTNAME

Line 29 in settings.py, change to 
'ALLOWED_HOSTS = [os.environ.get('HOSTNAME')]'

then in the terminal type 
'heroku config:set HOSTNAME=my-simple-sjj-django-todo.herokuapp.com'

This is so when we push to github, if we decide to change the Host all we have to do is modify the new deployment method instead of settings.py

# Local Environments

Because we have added enviroment variables, we can no longer run

'python3 manage.py runserver' in the terminal,

so we need to add variables into our settings.py to say its a development enviroment

So on LINE 16 (below the imports)

This code needs to be added

if os.environ.get('DEVELOPMENT'):
    development = True
else:
    development = False

Then modify the code on LINE 32 (DEBUG = True)

to

DEBUG = development

Also we need to tell the settings that we want to use sqlite in development mode and postgre on the internet so we need to modify our DATABASES Code

if development: 
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
else:
    DATABASES = {'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))}

This will still fail because you have to set the variable and since im using VS CODE,

export DEVELOPMENT = 1 wont work.

so I have created a file called env.py and set the same variable in that.

NOTE MUST USE STRINGS FOR ENVIRONMENTAL VARIABLES - THANKS JO :)

So the env.py file has this code in it.

import os

os.environ["DEVELOPMENT"] = "Yes"
os.environ["HOSTNAME"] = "127.0.0.1"

the settings.py has these lines of code

Starting on Line 16

from os import path
if path.exists("env.py"):
  import env 

if os.environ.get('DEVELOPMENT'):
    development = True
else:
    development = False
print(development)

# Trying to fix deployment issues


# Secret Key

Using 

https://miniwebtool.com/django-secret-key-generator/

I modified the settings.py LINE 35 to

SECRET_KEY = os.environ.get('SECRET_KEY')

I used heroku config:set SECRET_KEY="[key]"

I also added to env.py

'os.environ["SECRET_KEY"] = "Key"'