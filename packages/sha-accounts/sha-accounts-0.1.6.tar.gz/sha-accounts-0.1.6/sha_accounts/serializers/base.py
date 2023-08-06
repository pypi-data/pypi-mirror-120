from rest_framework.serializers import ModelSerializer
from djrest_wrapper.exceptions import DuplicateModelExp
from django.db import IntegrityError

class BaseSerializer(ModelSerializer):
    def create(self,validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise DuplicateModelExp(f'User is already exists')
