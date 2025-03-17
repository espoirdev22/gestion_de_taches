from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import validate_email

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[validate_email],
        required=True
    )
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password', 
            'confirm_password', 
            'first_name', 
            'last_name', 
            'user_type'
        ]
        extra_kwargs = {
            'username': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, data):
        # Validation des mots de passe
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        
        # Validation de l'unicité du nom d'utilisateur et de l'email
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Ce nom d'utilisateur existe déjà."})
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Cet email est déjà utilisé."})
        
        return data

    def create(self, validated_data):
        # Suppression du champ confirm_password avant création
        validated_data.pop('confirm_password')
        
        # Création de l'utilisateur
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            user_type=validated_data.get('user_type', 'student')
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'user_type',
            'profile_picture'
        ]
        read_only_fields = ['id']