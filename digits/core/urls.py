from django.urls import path

from digits.core import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='custom_login'),
    path(
        'usuarios/trocar_senha/', views.CustomPasswordChangeView.as_view(),
        name='custom_password_change'
    ),
    path('usuarios/<int:pk>/editar/', views.user_edit, name='user_edit'),
    path('aprs/', views.apr_list, name='apr_list'),
]