from django.contrib import admin

from digits.core import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj')


@admin.register(models.RiskQuestion)
class RiskQuestionAdmin(admin.ModelAdmin):
    list_display = ('category', 'order', 'description')
    list_filter = ('category',)
    ordering = ('category', 'order')
