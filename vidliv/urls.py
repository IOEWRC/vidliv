"""vidliv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import extra_views
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from registration.views import view_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.default.urls')),
    path('', include('home.urls')),
    path('', extra_views.landing_page, name='landing_page'),
    path('user/<str:username>', view_profile, name='user_profile'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')), name='favicon'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'vidliv.extra_views.error_404'
handler500 = 'vidliv.extra_views.error_500'
handler400 = 'vidliv.extra_views.error_400'
handler403 = 'vidliv.extra_views.error_403'
