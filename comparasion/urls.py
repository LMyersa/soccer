from django.urls import path
from . import views

urlpatterns = [
    path('comparasion/<str:filter_type>/', views.load_comparasion, name='comparasion'),
    path('', views.home, name="home")
]