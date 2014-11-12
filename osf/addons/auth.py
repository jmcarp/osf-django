# -*- coding: utf-8 -*-

import abc

import six

from django.apps import apps
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import detail_route

from requests_oauthlib import OAuth2Session

from osf import settings

from .views import HasUserAddon


class OAuthStateError(Exception):
    pass


@six.add_metaclass(abc.ABCMeta)
class AuthViewSet(ViewSet):

    permission_classes = (HasUserAddon, )

    @abc.abstractproperty
    def addon(self):
        pass

    @property
    def config(self):
        return settings.ADDON_CONFIGS[self.addon]


class CredentialViewSet(AuthViewSet):

    @abc.abstractmethod
    def store_credentials(self, request):
        pass

    @detail_route(methods=['put'])
    def login(self, request):
        return Response(self.store_credentials(request))


class OAuthViewSet(AuthViewSet):

    def get_redirect_url(self, request):
        return request.build_absolute_uri(reverse('auth-finish'))

    @abc.abstractmethod
    def get_authorization_url(self, request):
        pass

    @abc.abstractmethod
    def handle_callback(self, request):
        pass

    @detail_route()
    def start(self, request):
        authorization_url = self.get_authorization_url(request)
        return HttpResponseRedirect(authorization_url)

    @detail_route()
    def finish(self, request):
        return Response(self.handle_callback(request))


class OAuth2ViewSet(OAuthViewSet):

    @property
    def state_key(self):
        return '{}_auth_state'.format(self.addon)

    def get_authorization_url(self, request):
        oauth_session = OAuth2Session(
            self.config.CLIENT_ID,
            scope=self.config.SCOPE,
            redirect_uri=self.get_redirect_url(request),
        )
        url, state = oauth_session.authorization_url(self.config.OAUTH_AUTH_URL)
        request.session[self.state_key] = state
        return url

    def fetch_token(self, request):
        if request.session.get(self.state_key) != request.GET.get('state'):
            raise OAuthStateError
        session = OAuth2Session(self.config.CLIENT_ID)
        token = session.fetch_token(
            self.config.OAUTH_TOKEN_URL,
            client_secret=self.config.CLIENT_SECRET,
            code=request.GET.get('code'),
        )
        return token['access_token'], token['token_type']
