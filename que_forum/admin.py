from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.models import User, Group

# Unregister the original User and Group models to customize their admin interface
admin.site.unregister(User)
admin.site.unregister(Group)

# Register the customized User and Group admin
admin.site.register(User)
admin.site.register(Group)

