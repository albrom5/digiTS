from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from digits.core import forms, models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': [
            'first_name', 'last_name', 'email', 'is_active', 'is_staff',
            'companies', 'selected_company', 'role', 'password'
        ]}),
    )
    add_fieldsets = (
        (None, {'fields': ['email', 'password1', 'password2']}),
    )
    ordering = ('email',)
    form = forms.UserChangeForm


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj')


@admin.register(models.RiskQuestion)
class RiskQuestionAdmin(admin.ModelAdmin):
    list_display = ('category', 'order', 'description')
    list_filter = ('category',)
    ordering = ('category', 'order')


class RiskAnswerInline(admin.TabularInline):
    model = models.RiskAnswer
    extra = 0


class RiskSignatureInline(admin.TabularInline):
    model = models.RiskAnalysisSignature
    extra = 0


@admin.register(models.PreliminaryRiskAnalysis)
class PreliminaryRiskQuestionAdmin(admin.ModelAdmin):
    list_display = ('activity_type',)
    inlines = [RiskAnswerInline, RiskSignatureInline]
