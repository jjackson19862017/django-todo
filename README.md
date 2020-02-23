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