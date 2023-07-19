from rest_framework_gis.serializers import ModelSerializer
from accounts.models import (
    Profile
)

from studio.models import Category
from django.contrib.auth import get_user_model

User = get_user_model()


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['specialty']

class ProfileSerializer(ModelSerializer):
    # category = CategorySerializer()

    class Meta:
        model=Profile
        fields = '__all__'

class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields  = '__all__'