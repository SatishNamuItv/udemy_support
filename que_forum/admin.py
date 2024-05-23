from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User, Group, Permission

# Unregister the default UserAdmin
admin.site.unregister(User)

class CustomUserAdmin(DefaultUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.groups.filter(name='Admins').exists():
            obj.is_superuser = True  # Make user a superuser
            group, created = Group.objects.get_or_create(name='Admins')
            if created:
                permissions = Permission.objects.all()  # Assign all permissions
                group.permissions.set(permissions)
            obj.groups.add(group)
            obj.user_permissions.set(Permission.objects.all())
            obj.save()
        elif obj.groups.filter(name='Mentors').exists():
            obj.is_superuser = False  # Ensure mentors are not superusers
            group, created = Group.objects.get_or_create(name='Mentors')
            obj.groups.add(group)
            obj.save()

# Register the custom UserAdmin
admin.site.register(User, CustomUserAdmin)
