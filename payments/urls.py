from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment, name='payment'),
    path('initiate/', views.initiate_payment, name='initiate_payment'), 
    path('notification/', views.payment_notification, name='payment_notification'),
    
]