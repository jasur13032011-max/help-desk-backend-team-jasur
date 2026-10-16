from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # To'g'ridan-to'g'ri api.urls ga ulanishi shart!
]