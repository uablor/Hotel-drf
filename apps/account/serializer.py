
from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.http import urlsafe_base64_decode
# from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.exceptions import AuthenticationFailed
# from rest_framework.authentication import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.exceptions import AuthenticationFailed
# from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
# from rest_framework.response import Response

# from django.utils.encoding import force_bytes, force_str
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.contrib.auth.tokens import default_token_generator


class GroupSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    class Meta:
        model = User
        fields = ["email", "password", "password2", "first_name", "last_name", "phone"]
        
    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create(
            email=validated_data["email"],
            password=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone=validated_data["phone"],
        )

        user.set_password(validated_data["password"])
        user.save()
        return user


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "last_login": {"required": False},
            "date_joined": {"required": False},
            "created_at": {"required": False},
            "updated_at": {"required": False},
            "updated_at": {"required": False},
            "password": {"write_only": True},
        }

    def validate_password(self, value):

        validate_password(value)
        return value

    def create(self, validated_data):

        validated_data["password"] = make_password(validated_data["password"])
        
        validated_data['is_verify'] = False
        validated_data["is_active"] = True
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("password", None)
        return super().update(instance, validated_data)

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if self.instance:
            fields.pop("password")
            
        if request.method in ["POST", "PUT", "PATCH"]:
            user = request.user
            if (
                not user.is_superuser
                and not user.groups.filter(permissions__codename=" ").exists()
                ):
                fields.pop("is_staff")
                fields.pop("is_superuser")
                fields.pop("groups")
                fields.pop("user_permissions")
        return fields
    # def to_representation(self, instance):
    #     # Get the original representation
    #     representation = super().to_representation(instance)
    #     request = self.context.get("request")

    #     if request and request.method in ["POST", "PUT", "PATCH"]:
    #         user = request.user

    #         if (
    #             not user.is_superuser
    #             and not user.groups.filter(permissions__codename="change_is_superuser").exists()
    #         ):
    #             representation.pop("is_staff", None)
    #             representation.pop("is_superuser", None)
    #             representation.pop("groups", None)
    #             representation.pop("permissions", None)

    #     return representation


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["user_id"] = user.id
        token["email"] = user.email
        token["username"] = user.first_name + user.last_name
        # token["is_verify"] =  user.is_verify

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if not user.is_verify:
            raise AuthenticationFailed('User account is not verified. Please verify your email.')
        return data
    
    
class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required= True, write_only = True)
    new_password = serializers.CharField(required= True, write_only = True, validators=[validate_password])
    new_password2 = serializers.CharField(required= True, write_only = True)
    class Meta:
        model = User
        fields = ['password','new_password','new_password2']

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError({"password": "Current password is incorrect."})
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password2": "New password fields didn't match."})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class ResetPasswordSerializer(serializers.Serializer):
    
    password = serializers.CharField(write_only=True, required = True, validators = [validate_password])
    confirm_password = serializers.CharField(write_only=True, required = True)
        
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        data.pop('confirm_password')
        make_password(data['password'])
        return data
        
        
    #     try:
    #         # Decode user ID
    #         user_id = force_str(urlsafe_base64_decode(data['uidb64']))
    #         user = User.objects.get(pk=user_id)
    #     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    #         raise serializers.ValidationError("Invalid UID")

    #     # Verify the token
    #     if not default_token_generator.check_token(user, data['token']):
    #         raise serializers.ValidationError("Invalid token")

    #     # Check if passwords match
    #     if data['password'] != data['confirm_password']:
    #         raise serializers.ValidationError("Passwords do not match.")

    #     # Hash the password before returning
    #     data['password'] = make_password(data['password'])
    #     data.pop('confirm_password')

    #     # Add the user to the data to update the password later
    #     data['user'] = user
        
    #     return data
    
    # def save(self, **kwargs):
    #     validated_data = self.validated_data
    #     user = validated_data['user']
    #     user.password = validated_data['password']
    #     user.save()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    class Meta:
        fields = "email"
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is not associated with any account.")
        return value


class LogOutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    class Meta:
        fields = "refresh_token"

    def validate_refresh_token(self, value):
        try:
            token = RefreshToken(value)
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError(f"Error blacklisting token: {e}")
        return  value

