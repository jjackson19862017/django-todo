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

# Create new Item Form Page

so in templates make a new file called "item_form.html"

# Add Route to views.py

def create_an_item(request):
    return render(request, "item_form.html")

# Update url.py

from todo.views import get_todo_list, create_an_item

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', get_todo_list ),
    url(r'^add$', create_an_item)
]

# Add form to item_form.html

<form method="POST">
        <label for="id_name">Name:</label>
        <input type="text" name="name" id="id_name"><br>
        <label for="id_done">Done:</label>
        <input type="checkbox" name="done" id="id_done"><br>
        <button type="submit">Save</button>
    </form>

This will fail when you use the form to add an item you need to add {% csrf_token %} to just before the start of the form

# The form cant handle data till we add this to views.py

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