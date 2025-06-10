
from django.contrib import admin
from django.urls import path, include
from authentication import views as auth_views # Import authentication views for homepage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('listings/', include('listings.urls')),
    path('', auth_views.homepage, name='homepage'), # Define homepage at root
]
