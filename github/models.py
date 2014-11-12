# -*- coding: utf-8 -*-

from django.db import models

from osf.addons.models import BaseUserSettings, BaseComponentSettings


class GithubOauthSettings(models.Model):

    access_token = models.CharField(max_length=100)
    token_type = models.CharField(max_length=100)


class GithubUserSettings(BaseUserSettings):

    oauth_settings = models.ForeignKey('GithubOauthSettings', blank=True, null=True)

    @property
    def access_token(self):
        try:
            return self.oauth_settings.access_token
        except AttributeError:
            return None

    @access_token.setter
    def access_token(self, value):
        self.oauth_settings.access_token = value

    @property
    def token_type(self):
        try:
            return self.oauth_settings.token_type
        except AttributeError:
            return None

    @token_type.setter
    def token_type(self, value):
        self.oauth_settings.token_type = value


class GithubComponentSettings(BaseComponentSettings):

    user_settings = models.ForeignKey('GithubUserSettings', blank=True, null=True)

    user_name = models.CharField(max_length=100)
    repo_name = models.CharField(max_length=100)

    @property
    def is_authorized(self):
        return self.user_settings and self.user_settings.is_authorized
