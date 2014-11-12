# -*- coding: utf-8 -*-

import abc

import six

from rest_framework import generics, permissions, routers
from rest_framework.response import Response

from osf.views import HasPermissions

from component.models import Component


class HasUserAddon(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        if not super(HasUserAddon, self).has_permission(request, view):
            return False
        return request.user.get_addon(view.addon) is not None


class BaseComponentPermission(permissions.BasePermission):

    def get_component(self, obj):
        return obj if isinstance(obj, Component) else obj.component


class HasComponentAddon(BaseComponentPermission):

    def has_object_permission(self, request, view, obj):
        component = self.get_component(obj)
        return bool(component.get_addon(view.addon))


class AuthRouter(routers.SimpleRouter):

    routes = [
        # Dynamically generated detail routes.
        # Generated using @detail_route decorator on methods of the viewset.
        routers.DynamicDetailRoute(
            url=r'{prefix}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={},
        ),
    ]

    def register(self, prefix=None, viewset=None, basename=None):
        prefix = prefix or '{}/auth'.format(viewset.addon)
        super(AuthRouter, self).register(prefix, viewset, basename)

    def get_default_base_name(self, viewset):
        return 'auth'


@six.add_metaclass(abc.ABCMeta)
class BaseComponentConfigViews(generics.GenericAPIView):

    permission_classes = (HasComponentAddon, HasPermissions)
    lookup_field = 'id'
    model = Component

    @abc.abstractproperty
    def addon(self):
        pass

    perms_map = {
        'GET': ['write', 'admin'],
        'PUT': ['write', 'admin'],
    }

    @abc.abstractmethod
    def get_config(self, component, addon):
        pass

    @abc.abstractmethod
    def set_config(self, component, addon):
        pass

    def get_objects(self):
        component = self.get_object()
        addon = component.get_addon(self.addon)
        return component, addon

    def get(self, request, id):
        component, addon = self.get_objects()
        return Response(self.get_config(request.user, component, addon))

    def put(self, request, id):
        component, addon = self.get_objects()
        return Response(self.set_config(request.user, component, addon, request.DATA))
