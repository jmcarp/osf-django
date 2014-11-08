from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
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

    @property
    def has_guid(self):
        try:
            self.id
            return True
        except:
            return False

    def get_absolute_url(self):
        raise NotImplementedError


def get_app_label(schema):
    return '{0}.{1}'.format(schema._meta.app_label, schema._meta.object_name)


@receiver(pre_save)
def ensure_guid(sender, instance, **kwargs):
    if not issubclass(sender, GuidMixin):
        return
    if not instance.has_guid:
        guid = Guid(app_label=get_app_label(sender))
        guid.save()
        instance.id = guid


from django.contrib.auth.models import AbstractUser


class User(GuidMixin, AbstractUser):
    pass


class Component(GuidMixin, models.Model):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey('Component', related_name='children', blank=True, null=True)
    contributors = models.ManyToManyField(User, related_name='components')

    def __unicode__(self):
        return self.title

