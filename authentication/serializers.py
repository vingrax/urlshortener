from rest_framework import serializers,viewsets
from django.contrib.auth.models import User
from .models import ShortenedURL

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ('username','password')

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ShortenedURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = ('original_url','short_url')

class ShortenedURLViewSet(viewsets.ModelViewSet):
    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)