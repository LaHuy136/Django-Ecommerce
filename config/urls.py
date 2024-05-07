# type: ignore
from django.contrib import admin 
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.HOME, name='home'),
    path('base/', views.BASE,name='base'),
]
