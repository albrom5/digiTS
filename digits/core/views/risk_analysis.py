from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from digits.core import forms, models


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def apr_list(request):
    user = request.user
    company = user.selected_company
    aprs = models.PreliminaryRiskAnalysis.objects.filter(
        company=company
    )
    context = {
        'apr_list': aprs
    }
    return render(request, 'core/apr_list.html', context)


@login_required
def apr_new(request):
    form = forms.RiskAnalysisForm()
    context = {
        'form': form
    }
    return render(request, 'core/apr_form_general.html', context)