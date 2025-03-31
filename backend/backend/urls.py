"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
# from django.views.generic import TemplateView 
# from . import views

urlpatterns = [
    #  path('', views.home, name='home'),  
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),  # Include authentication routes
    path('api/', include('help_requests.urls')),
    path('api/groups/', include('groups.urls')),
    path('api/events/', include('events.urls')),  
    path('api/notifications/', include('notifications.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
