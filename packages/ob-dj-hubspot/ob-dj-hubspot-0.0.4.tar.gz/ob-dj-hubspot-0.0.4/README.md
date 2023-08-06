## OBytes Django HubSpot App

HubSpot Django Application is designed to integrate with HubSpot to sync contacts, companies and deals from and to HubSpot.

## Quick start

1. Install `ob_dj_hubspot` latest version `pip install ob_dj_hubspot`

2. Add "ob_dj_hubspot" to your `INSTALLED_APPS` setting like this:

```python
   # settings.py
   INSTALLED_APPS = [
        ...
        "ob_dj_hubspot.core.hubspot",
   ]
# TODO: ADD Other settings
```


3. Include the  URLs in your project urls.py like this::

```python
    path("hubspot/", include("ob_dj_hubspot.apis.hubspot.urls")),
```

4. Run ``python manage.py migrate`` to create the hubspot models.


## Developer Guide

1. Clone github repo `git clone [url]`

2. `pipenv install --dev`

3. `pre-commit install`

4. Run unit tests `pytest`

