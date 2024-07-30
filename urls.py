from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls),
    path('admin/', views.home, name='home'),
    path('scan/', views.home, name='scan'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
