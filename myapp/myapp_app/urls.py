from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_screen, name='home-screen'),
    path('/', views.home_screen, name='home-screen'),
    path('new-url-search/', views.short_url_screen, name='search-screen'),
    path('bored/', views.bored_screen, name='bored-screen'),
    path('bored/bored-results/', views.bored_results_screen, name='bored-results-screen')
]
