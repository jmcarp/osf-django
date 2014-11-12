# -*- coding: utf-8 -*-

import importlib

from django.conf.urls import patterns, include, url
from django.contrib import admin

from osf import views, settings


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'osf.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^components/$', views.ComponentList.as_view()),
    url(r'^components/(?P<pk>\d+)/$', views.ComponentDetail.as_view()),
)

for addon in settings.INSTALLED_ADDONS:
    urls = importlib.import_module('{}.urls'.format(addon))
    try:
        urlpatterns.append(url('', include(urls.urlpatterns)))
    except AttributeError:
        pass
