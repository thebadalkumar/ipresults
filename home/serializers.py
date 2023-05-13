from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import BCA

class StudentSerializer(serializers.ModelSerializer):
    semester = serializers.JSONField()
    institution = serializers.StringRelatedField(read_only=True)
    batch = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BCA
        fields = '__all__'


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']