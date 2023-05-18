
from django.urls import path
from . import views



urlpatterns = [
     path('register/', views.register , name ='register'),
    path('', views.login , name ='login'),
    path('index/', views.index , name ='index'),
    path('perfil/', views.perfil , name ='perfil'),
    path('generate_pdf/', views.generate_pdf , name ='generate_pdf'),
    
]
