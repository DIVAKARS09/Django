from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin Interface
    path('admin/', admin.site.urls),
    
    # Include all patterns from the application named 'project' at the root level ('')
    path('', include('project.urls')),
]
