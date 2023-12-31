from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy


def user_edit(request, pk):
    context = {}
    return render(request, 'core/user_form.html', context) 


class CustomLoginView(LoginView):

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        user = form.get_user()

        if not user.has_changed_password:
            return redirect('core:custom_password_change')

        return redirect('core:home')


class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.has_changed_password = True
        user.save()
        return super().form_valid(form)
