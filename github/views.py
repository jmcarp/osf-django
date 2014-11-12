# -*- coding: utf-8 -*-

from osf.addons.auth import OAuth2ViewSet
from osf.addons.views import BaseComponentConfigViews

from .models import GithubOauthSettings


class GithubAuthViewSet(OAuth2ViewSet):

    addon = 'github'

    def handle_callback(self, request):
        access_token, token_type = self.fetch_token(request)
        oauth_settings = GithubOauthSettings(
            access_token=access_token,
            token_type=token_type,
        )
        oauth_settings.save()
        user_addon = request.user.get_addon(self.addon)
        user_addon.oauth_settings = oauth_settings
        user_addon.save()
        return {'status': 'success'}


class GithubComponentConfigViews(BaseComponentConfigViews):

    addon = 'github'

    def get_config(self, user, component, addon):
        return {
            'authorized': addon.is_authorized,
            'user': addon.user_name,
            'repo': addon.repo_name,
        }

    def set_config(self, user, component, addon, data):
        if addon.user_settings and addon.user_settings.owner != user:
            raise
        user_name = data.get('user')
        repo_name = data.get('repo')
        try:
            repo = client.repo(user, repo)
        except:
            raise
        addon.user_name = user_name
        addon.repo_name = repo_name
