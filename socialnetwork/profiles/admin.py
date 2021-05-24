from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ProfileCreationForm
from .models import Friendship, Profile


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = Profile
    add_form = ProfileCreationForm

    fieldsets = (
        ('Username', {'fields': ('username',)}),
        ('Media', {'fields': ('avatar',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'bio', 'birth_date', 'gender')}),
        ('Location', {'fields': ('country', 'city')}),
        ('Contact Info', {'fields': ('email', 'phone')}),
        ('', {'fields': ('is_active', 'is_staff', 'is_superuser', 'date_joined')}),
    )


admin.site.register(Profile, CustomUserAdmin)
admin.site.register(Friendship)
