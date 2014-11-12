# -*- coding: utf-8 -*-

# OSF configuration

NAME = 'github'

SETTINGS_MODELS = {
    'user': 'github.GithubUserSettings',
    'component': 'github.GithubComponentSettings',
}


# GitHub configuration

CLIENT_SECRET = '...'

# GitHub access scope
SCOPE = ['repo']

# Set GitHub privacy on OSF permissions change
SET_PRIVACY = False

# GitHub hook domain
HOOK_DOMAIN = None
HOOK_CONTENT_TYPE = 'json'

CLIENT_ID = 'ad1cf36eda5064fc7f4c'
CLIENT_SECRET = 'f775dcb3042b8562e49efc8604fb589775dbc1f7'

