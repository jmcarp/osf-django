# -*- coding: utf-8 -*-

# OSF configuration

NAME = 'github'

SETTINGS_MODELS = {
    'user': 'github.GithubUserSettings',
    'component': 'github.GithubComponentSettings',
}


# GitHub configuration

CLIENT_ID = 'changeme'
CLIENT_SECRET = 'changeme'

OAUTH_AUTH_URL = 'https://github.com/login/oauth/authorize'
OAUTH_TOKEN_URL = 'https://github.com/login/oauth/access_token'

# GitHub access scope
SCOPE = ['repo']

