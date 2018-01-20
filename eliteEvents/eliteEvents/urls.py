from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('', include('website.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls)
]
