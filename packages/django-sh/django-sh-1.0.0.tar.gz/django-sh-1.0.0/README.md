# django-sh
Django shell 


## Installation
```
pip install django-sh
```

## Add django-sh to INSTALLED_APPS
```
INSTALLED_APPS = [
    # ...
    "sh",
    # ...
]
```

## Add the urls
```
from django.urls import include

urlpatterns = [
    # ...
    path('sh/', include('sh.urls')),
    # ...
]

```