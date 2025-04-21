from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_network, name='get_network'),
    path('bias/', views.get_bias, name='bias'),
    path('condition/', views.condition, name='condition'),
    path('condition/<str:predefined>/', views.condition, name='condition_with_id'),
    path('csrf/', views.csrf, name="csrf"),
    path('session/', views.session_key, name="session")
]
