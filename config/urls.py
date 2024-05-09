# type: ignore
from django.contrib import admin 
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HOME, name='home'),
    path('base/', views.BASE,name='base'),  
    path('products/',views.PRODUCT, name='products'),
    path('products/<str:id>', views.PRODUCT_DETAIL_PAGE, name='product_detail'),
    path('search/', views.SEARCH, name='search'),
    path('contact/', views.Contact_Page, name ='contact'),
    path('register/', views.HandleRegister, name='register'),
    path('login/', views.HandleLogin, name='login'),
    path('logout/', views.HandleLogout, name='logout'),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)