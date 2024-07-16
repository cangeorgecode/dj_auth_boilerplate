from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile_view'),
    path('edit/', views.profile_edit_view, name='profile_edit_view'),
    path('onboarding/', views.profile_edit_view, name='profile_onboarding'),
    path('settings/', views.profile_settings_view, name='profile_settings_view'),
    path('emailchange/', views.profile_emailchange, name='profile_emailchange'),
    path('emailverify/', views.profile_emailverify, name='profile_emailverify'),
    path('delete/', views.profile_delete_view, name='profile_delete_view'),
]