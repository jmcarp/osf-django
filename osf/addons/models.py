# -*- coding: utf-8 -*-

from django.db import models
from django.apps import apps
from django.db.models.loading import get_model

from osf import settings


class DuplicateAddonError(Exception):
    pass


class AddonMixin(object):

    def get_addon(self, name):
        attr = '{}_settings'.format(name)
        return getattr(self, attr, None)

    def get_addon_model(self, name):
        schema = self.__class__._meta.object_name.lower()
        config = settings.ADDON_CONFIGS['github']
        model_path = config.SETTINGS_MODELS[schema]
        return get_model(model_path)

    def create_addon(self, name):
        if self.get_addon(name):
            raise DuplicateAddonError
        model = self.get_addon_model(name)
        addon = model(owner=self)
        addon.save()
        return addon

    def get_or_create_addon(self, name):
        return self.get_addon(name) or self.create_addon(name)


class BaseUserSettings(models.Model):
    owner = models.OneToOneField('component.User', related_name='%(app_label)s_settings')
    class Meta:
        abstract = True


class BaseComponentSettings(models.Model):
    owner = models.OneToOneField('component.Component', related_name='%(app_label)s_settings')
    class Meta:
        abstract = True
