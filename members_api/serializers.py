from rest_framework import serializers
from django.contrib.auth import authenticate
from members.models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id', 
            'member', 
            'bio', 
            'display_image', 
            'location', 
            'status', 
            'animal'
            )
         
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label = "Username",
        write_only = True
    )
    password = serializers.CharField(
        label = "Password",
        style = {'input_type': 'password'},
        trim_whitespace = False,
        write_only = True
    )

    def validated(self, attributes):
        username = attributes.get('username')
        password = attributes.get('password')

        if username and password:
            #authenticate using django auth framework
            user = authenticate(
                        request = self.context.get('request'),
                        username = username,
                        password = password
                        )
            
            if not user:
                message = 'Access denied: wrong username or password'
                raise serializers.ValidationError(message, code='authorization')
        
        else:
            message = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(message, code='authorization')
        
        attributes['user'] = user
        return attributes

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')
        extra_kwargs = {
            'username': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )

        user.set_password(validated_data['password'])
        user.save()
        #create user profile
        Profile.objects.create(user=user)

        return user
        
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email',)

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("password",)
    
    #validate encoded pk and token
    def validate(self, data):
        password = data.get("password")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data")
        
        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")
        
        user.set_password(password)
        user.save()
        return data

