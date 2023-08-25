from django.urls import path
from .views import CustomAuthToken,RegistrationView,redirect_to_original_url,shorten_url_view,retrieve_shortened_url,create_shortened_url,login_view

urlpatterns = [
    path('token-auth/',CustomAuthToken.as_view(),name='auth'),
    path('register/',RegistrationView.as_view(),name='register'),
    path('createurl/',create_shortened_url,name='create_url'),
    path('short-url/<str:short_url>/', retrieve_shortened_url, name='retrieve_shortened_url'),
    path('r/<str:short_url>/', redirect_to_original_url, name='redirect_to_original_url'),
    path('login/',login_view,name='login'),
    path('url/',shorten_url_view)
]
