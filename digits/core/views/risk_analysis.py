from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from digits.core.models import PreliminaryRiskAnalysis


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def apr_list(request):
    user = request.user
    company = user.selected_company
    aprs = PreliminaryRiskAnalysis.objects.filter(
        company=company
    )
    context = {
        'apr_list': aprs
    }
    return render(request, 'core/apr_list.html', context)