from django.db import models
from django.dispatch import receiver
from django.db.models.loading import get_model


class Guid(models.Model):

    id = models.AutoField(primary_key=True)
    app_label = models.CharField(max_length=100)

    @property
    def content(self):
        schema = get_model(self.app_label)
        return schema.objects.get(id=self.id)


class GuidMixin(models.Model):

    id = models.OneToOneField(Guid, primary_key=True)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        raise NotImplementedError

    @classmethod
    def guid_for(cls):
        guid = Guid(app_label=get_app_label(cls))
        guid.save()
        return guid

    def save(self, *args, **kwargs):
        try:
            self.id
        except:
            self.id = self.guid_for()
        super(GuidMixin, self).save(*args, **kwargs)


def get_app_label(schema):
    return '{0}.{1}'.format(schema._meta.app_label, schema._meta.object_name)


from django.contrib.auth.models import AbstractUser


class User(GuidMixin, AbstractUser):
    pass

from guardian.shortcuts import get_perms, assign_perm, remove_perm

class Component(GuidMixin, models.Model):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey('Component', related_name='children', blank=True, null=True)
    contributors = models.ManyToManyField(User, related_name='components')
    is_deleted = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)

    registered_from = models.ForeignKey('Component', related_name='registrations', blank=True, null=True)
    forked_from = models.ForeignKey('Component', related_name='forks', blank=True, null=True)

    @property
    def is_registration(self):
        return bool(self.registered_from)

    @property
    def is_fork(self):
        return bool(self.forked_from)

    def add_contributor(self, contributor, permission='admin'):
        self.contributors.add(contributor)
        assign_perm(permission, contributor, self)

    def remove_contributor(self, contributor):
        self.contributors.remove(contributor)
        for perm in get_perms(contributor, self):
            remove_perm(perm, contributor, self)

    def clone(self):
        cloned = self.__class__.objects.get(id=self.id)
        cloned.id = self.guid_for()
        return cloned

    def copy_contributors(self, other):
        other.contributors = self.contributors.all()
        for contributor in self.contributors.all():
            for perm in get_perms(contributor, self):
                assign_perm(perm, contributor, other)

    def register(self):
        registration = self.clone()
        self.copy_contributors(registration)
        registration.registered_from = self
        registration.save()
        return registration

    def fork(self):
        fork = self.clone()
        self.copy_contributors(fork)
        fork.forked_from = self
        fork.save()
        return fork

    class Meta:
        permissions = (
            ('read', 'Read-only'),
            ('write', 'Read and write'),
            ('admin', 'Administrator'),
        )

    def __unicode__(self):
        return self.title


