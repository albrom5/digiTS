from django.contrib import admin
from digits.core.models import User

@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')    

