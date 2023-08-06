import django.dispatch

# HubSpot contact is created, updated or deleted
contact_created = django.dispatch.Signal()
contact_updated = django.dispatch.Signal()
contact_deleted = django.dispatch.Signal()

# HubSpot company is created, updated or deleted
company_created = django.dispatch.Signal()
company_updated = django.dispatch.Signal()
company_deleted = django.dispatch.Signal()

# HubSpot deal is created, updated or deleted
deal_created = django.dispatch.Signal()
deal_updated = django.dispatch.Signal()
deal_deleted = django.dispatch.Signal()
