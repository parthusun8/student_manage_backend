"""Students URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from django.conf import settings
from django.urls import URLPattern, URLResolver


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]


# urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])

# def list_urls(lis, acc=None):
#     if acc is None:
#         acc = []
#     if not lis:
#         return
#     l = lis[0]
#     if isinstance(l, URLPattern):
#         yield acc + [str(l.pattern)]
#     elif isinstance(l, URLResolver):
#         yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
#     yield from list_urls(lis[1:], acc)

# for p in list_urls(urlconf.urlpatterns):
#     print(''.join(p))