from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import authentication_classes,permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .serializers import RegistrationSerializer,ShortenedURLSerializer
from .models import ShortenedURL
import random,string,hashlib
#Login
class CustomAuthToken(ObtainAuthToken):
    def post(self, request,*args, **kwargs):
        response = super().post(request,*args,**kwargs)
        token = Token.objects.get(key = response.data['token'])
        return Response({'token':token.key,'user_id':token.user_id})
#Registration
class RegistrationView(APIView):
    def post(self,request):
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user = user)
            return Response({'token':token.key,'user_id':user.id},status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#URL Functions
def generate_short_url(length=8):
    print(type(length))
    characters = string.ascii_letters + string.digits
    while True:
        random_string = ''.join(random.choice(characters) for _ in range(length))
        hash_object = hashlib.md5(random_string.encode())
        short_url = hash_object.hexdigest()[:length]
        
        if not ShortenedURL.objects.filter(short_url=short_url).exists():
            return short_url
        return generate_short_url()

def redirect_to_original_url(request, short_url):
    try:
        shortened_url = ShortenedURL.objects.get(short_url=short_url)
        original_url = shortened_url.original_url
        return redirect(original_url)
    except ShortenedURL.DoesNotExist:
        return HttpResponse("Short URL not found", status=404)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_shortened_url(request):
    user = request.user

    original_url = request.data.get('original_url')
    if not original_url:
        return Response({'error':'Original URL is required.'},status=status.HTTP_400_BAD_REQUEST)
    existing_shortened_url = ShortenedURL.objects.filter(original_url=original_url).first()
    if existing_shortened_url:
        serializer =ShortenedURLSerializer(existing_shortened_url)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        
    
    short_url = generate_short_url()

    shortened_url = ShortenedURL.objects.create(
        original_url = original_url,
        short_url = short_url,
        user = user
    )

    serializer =ShortenedURLSerializer(shortened_url)
    return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def retrieve_shortened_url(request, short_url):
    user = request.user

    try:
        shortened_url = ShortenedURL.objects.get(short_url=short_url, user=user)
    except ShortenedURL.DoesNotExist:
        return Response({'error': 'Shortened URL not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ShortenedURLSerializer(shortened_url)
    return Response(serializer.data)

def login_view(request):
    return render(request,'authentication/index.html')


@permission_classes([IsAuthenticated])
def shorten_url_view(request):
    return render(request,'authentication/urlinput.html')
