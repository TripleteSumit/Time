from rest_framework import serializers
from .models import Teacher, Subject
from drf_spectacular.utils import extend_schema_field


class UserProileSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']


class TeacherProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ['name', 'email', 'phone_no', 'department', 'subject']

    subject = UserProileSubjectSerializer(many=True)
    department = serializers.StringRelatedField()
    name = serializers.SerializerMethodField(method_name='get_name')
    email = serializers.SerializerMethodField(method_name='get_email')

    @extend_schema_field(str)
    def get_name(self, obj):
        return f"{self.context['user'].first_name} {self.context['user'].last_name}"

    @extend_schema_field(str)
    def get_email(self, obj):
        return self.context['user'].email
