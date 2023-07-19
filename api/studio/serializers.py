from rest_framework.serializers import ModelSerializer

from studio.models import (
    Project, Category, MainCategory
)
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

class MainCategorySerializer(ModelSerializer):

    class Meta:
        model = MainCategory
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    main_category = MainCategorySerializer()
    class Meta:
        model = Category
        fields = '__all__'


class ProjectSerializer(ModelSerializer):
    owner = UserSerializer()
    category = CategorySerializer()

    class Meta:
        model = Project
        fields = '__all__'
