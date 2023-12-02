from django.contrib import admin
from django.urls import path
from hackathon import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('generate_result/', views.generate_result, name='generate_result'),
    path('delete_data/', views.delete_data, name='delete_data'),
]
