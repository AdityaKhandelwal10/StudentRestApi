from rest_framework import serializers 
from .models import Student
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True, validators = [UniqueValidator(queryset = Student.objects.all())])

    password = serializers.CharField(write_only = True, required = True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True, required = True)

    class Meta:
        model = Student
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
            
        else:
            return attrs

    def create(self, validated_data):
        student  = Student.objects.create_user(validated_data['username'],validated_data['email'],
        validated_data['password'])

        student.first_name = validated_data['first_name']
        student.last_name = validated_data['last_name']
        student.save()

        return student
