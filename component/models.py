from django.db import models
from authentication.models import User


class Guid(models.Model):
    id = models.IntegerField(primary_key=True)

class GuidModel(models.Model):
    guid = models.ForeignKey('Guid')

    def save(self, *args, **kwargs):
        if not saved:
            my_guid = Guid()
            self.guid = my_guid
        ret = super(GuidModel, self).save(*args, **kwargs)
        return ret

    class Meta:
        abstract = True

class Component(GuidModel):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey('Component', related_name='children', blank=True, null=True)
    contributors = models.ManyToManyField(User, related_name='components')

    def __unicode__(self):
        return self.title
