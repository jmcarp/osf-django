from rest_framework import generics

from component.models import Component


##

from rest_framework import serializers

class ComponentSerializer(serializers.ModelSerializer):
    contributors = serializers.RelatedField(many=True)
    title = serializers.CharField(required=False)
    is_registration = serializers.CharField()
    is_fork = serializers.CharField()
    class Meta:
        model = Component
        fields = ('title', 'contributors', 'is_public', 'is_registration', 'is_fork')


##


from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response


from rest_framework.exceptions import APIException

class HttpGone(APIException):
    status_code = 410
    default_detail = 'Resource deleted'


class HttpUnauthorized(APIException):
    status_code = 401
    default_detail = 'Not authenticated'


class OsfPermissionMixin(object):

    def get_component(self, obj):
        return obj if isinstance(obj, Component) else obj.component


from guardian.shortcuts import get_perms

class HasPermissions(permissions.BasePermission, OsfPermissionMixin):

    # perms_map = {
    #     'PUT': ['write', 'admin'],
    #     'DELETE': ['write', 'admin'],
    # }
    def has_object_permission(self, request, view, obj):
        component = self.get_component(obj)
        user = request.user
        if not request.user:
            return False
        user_perms = get_perms(user, component)
        allowed_perms = view.perms_map.get(request.method, [])
        if not set(user_perms).intersection(allowed_perms):
            return False
        return True


class ContributorOrPublic(permissions.BasePermission, OsfPermissionMixin):

    def has_object_permission(self, request, view, obj):
        component = self.get_component(obj)
        if not component.is_public:
            if not request.user or not request.user.is_authenticated():
                raise HttpUnauthorized
            if not component.contributors.filter(id=request.user.id).first():
                return False
        return True


class ReadOnlyOrNotRegistration(permissions.BasePermission, OsfPermissionMixin):

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            component = self.get_component(obj)
            if component.is_registration:
                return False
        return True


class NotDeleted(permissions.BasePermission, OsfPermissionMixin):

    def has_object_permission(self, request, view, obj):
        component = self.get_component(obj)
        if component.is_deleted:
            raise HttpGone
        return True


##

class ComponentList(generics.ListCreateAPIView):
    queryset = Component.objects.filter(is_deleted=False)
    serializer_class = ComponentSerializer


class ComponentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (NotDeleted, ContributorOrPublic, ReadOnlyOrNotRegistration, HasPermissions)
    perms_map = {
        'GET': ['read', 'write', 'admin'],
        'PUT': ['write', 'admin'],
    }
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer



