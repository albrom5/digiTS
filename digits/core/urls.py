from django.urls import path

from digits.core import views

app_name = 'core'

urlpatterns = [
    path('', views.apr_list, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='custom_login'),
    path(
        'usuarios/trocar_senha/', views.CustomPasswordChangeView.as_view(),
        name='custom_password_change'
    ),
    path('usuarios/<int:pk>/editar/', views.user_edit, name='user_edit'),
    path('aprs/', views.apr_list, name='apr_list'),
    path('apr/nova/', views.apr_new, name='apr_new'),
    path('apr/<int:pk>', views.apr_detail, name='apr_detail'),
    path('apr/<int:pk>/pdf/', views.APRDetailPDF.as_view(), name='apr_detail_pdf'),
    path('apr/<int:pk>/sign/', views.apr_sign, name='apr_sign'),
    path('apr/<int:pk>/delete/', views.apr_delete, name='apr_delete'),
]
