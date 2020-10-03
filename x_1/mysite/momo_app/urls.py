from django.conf.urls import url 
from momo_app import views 
from django.urls import path



urlpatterns = [
    path('', views.index),   
    path('api/', views.api), 
    path('momo_api/', views.momo_api),       

]