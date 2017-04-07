"""gatewayAPI URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include,url
from django.contrib import admin
import gateway.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',gateway.views.home),
    url(r'^setLoadBalance/(?P<cmts>\w.+)/(?P<d2LoadBalance>[0-1]+)/(?P<d3LoadBalance>[0-1]+)', gateway.views.setLoadBalance),
    url(r'^getDevicesCMTS/', gateway.views.getDevicesCMTS),
    url(r'^getDevicesPE/', gateway.views.getDevicesPE)
]