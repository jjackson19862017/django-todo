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