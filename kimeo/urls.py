"""kimeo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from kimeo import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from KimeoApp import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    url(r'^$', views.home),
    url(r'^api/', include(router.urls)),
    url(r'^home', views.home),
    url(r'^about', views.about),
    url(r'^portfolio', views.portfolio),
    url(r'^actions', views.actions),
    url(r'^control', views.control),
    url(r'^movement', views.movement),
    url(r'^message', views.message),
    url(r'^monitoring', views.monitoring),
    url(r'^contact', views.contact),
    url(r'mail',views.mail),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()