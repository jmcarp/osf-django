# from django.db import models
# from django.dispatch import receiver
# from django.db.models.signals import pre_save


# class Bob(models.Model):
#     pass

# class Guid(models.Model):
#     pass


# class GuidModel(models.Model):
#     id = models.ForeignKey(Guid, primary_key=True, related_name='record')
#     class Meta:
#         abstract = True
#     def get_absolute_url(self):
#         raise NotImplementedError


# @receiver(pre_save)
# def ensure_guid(sender, instance, **kwargs):
#     if not issubclass(sender, GuidModel):
#         return
#     if not instance.id:
#         guid = Guid()
#         instance.id = guid
