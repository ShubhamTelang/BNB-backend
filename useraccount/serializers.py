from rest_framework import serializers
from .models import User

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email','password','password2']
        extra_kwargs = {
            'password': {'write_only':True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm password does not match")
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id','name','avatar_url'
        )


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=222)
    class Meta:
        model=User
        fields =['email','password']
