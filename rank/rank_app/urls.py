from django.urls import path
from .  import views

urlpatterns = [
    path('', views.search , name='search'),
    path('result/', views.movie_result, name='movie_result'),
    
]