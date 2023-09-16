from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def home(request):
    return render(request, 'home.html')