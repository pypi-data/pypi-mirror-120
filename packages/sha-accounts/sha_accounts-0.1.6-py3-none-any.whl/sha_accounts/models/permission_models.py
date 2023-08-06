from django.db import models
from djrest_wrapper.interfaces import BaseModel


class AbstractPermission(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True
        verbose_name = 'permission'
        verbose_name_plural = 'permissions'


class Permission(AbstractPermission):
    pass
