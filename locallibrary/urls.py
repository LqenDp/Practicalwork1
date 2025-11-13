from django.contrib import admin
from django.urls import path, include  # Make sure this import is correct
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('', RedirectView.as_view(url='catalog/')),  # Redirect root to catalog
]
