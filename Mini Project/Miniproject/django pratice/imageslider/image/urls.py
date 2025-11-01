from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_image, name='upload_image'),
    path('delete/<int:pk>/', views.delete_image, name='delete_image'),
    
]
