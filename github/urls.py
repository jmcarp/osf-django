# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from osf.addons.views import AuthRouter

from . import views


auth_router = AuthRouter()
auth_router.register(viewset=views.GithubAuthViewSet)

urlpatterns = patterns('',
    url('^addons/', include(auth_router.urls)),
    url('^components/(?P<id>\d+)/addons/github/', include([
        url('^config/', views.GithubComponentConfigViews.as_view()),
    ])),
)
