from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """Serializer per mostrare i dati pubblici di un utente"""
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'bio', 'role', 'followers_count', 'following_count']
        read_only_fields = ['id', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer per la registrazione di nuovi utenti standard"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'bio']

    def create(self, validated_data):
        # forza il ruolo a STANDARD per motivi di sicurezza durante la registrazione pubblica...
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            role=CustomUser.Role.STANDARD
        )
        return user