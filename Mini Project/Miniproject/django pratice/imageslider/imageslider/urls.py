"""
URL configuration for imageslider project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings    # to connect and serve uploaded media files when developing locally
# need Django to serve those files while running the development server
from django.conf.urls.static import static  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('image.urls')),
]

if settings.DEBUG:  # checks the project is running in development mode
    # URL path for your uploaded media and tells where to find those files on your computer
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

