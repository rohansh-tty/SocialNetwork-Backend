from django.shortcuts import render, redirect
from app.serializer import UserSerializer, FriendRequestSerializer, UserResponseSerializer
from rest_framework.response import Response
from rest_framework import status
from app.models import User, FriendRequest
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User as DjangoUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from django.core.cache import cache
from functools import wraps
from django.http import HttpResponse
from time import time


def rate_limit(limit=10, period=60):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_id = request.user.id
            cache_key = f'rate_limit_{user_id}'
            
            # Get the current count and last reset time
            cache_data = cache.get(cache_key, {'count': 0, 'last_reset': time()})
            current_time = time()
            
            # Check if the period has elapsed and reset if necessary
            if current_time - cache_data['last_reset'] > period:
                cache_data = {'count': 0, 'last_reset': current_time}
            
            # Check if the limit has been reached
            if cache_data['count'] >= limit:
                return HttpResponse('Rate limit exceeded', status=429)
            
            # Increment the count and update the cache
            cache_data['count'] += 1
            cache.set(cache_key, cache_data, period * 2)  # Set a longer expiration to ensure proper resets
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 1000
    
class TokenUserMixin:
    def get_user_from_token(self):
        try:
            auth_header = self.request.headers.get('Authorization')
            if not auth_header:
                raise AuthenticationFailed('Authorization header is missing')
            
            access_token = auth_header.split(' ')[1]
            token = AccessToken(access_token)
            print(token.payload)
            user_id = token.payload.get('user_id')
            
            if not user_id:
                raise AuthenticationFailed('Invalid token payload')
            
            user = get_object_or_404(DjangoUser, id=user_id)
            return user
        except Exception as e:
            raise AuthenticationFailed(str(e))


@api_view(['POST'])
def signup(request):
    print(request.data, type(request.data))
    
    serializer = UserSerializer(data=request.data, partial=True)
    print(serializer.is_valid())
    if serializer.is_valid():
        serializer.save()
        # create django user
        print(request.data['name'], request.data['email'], request.data['password'])
        django_user = DjangoUser.objects.create_user(username=request.data['name'], email=request.data['email'], password=request.data['password'])
        django_user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def login(request):
    print(request.data, type(request.data))
    email = request.data['email']
    password = request.data['password']
    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    if user.password != password:
        return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = UserSerializer(user)
    if user.password == password:
        return Response({"email": user.email, "id": user.id}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def logout(request):
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_friends(request):
    user_id = request.query_params["id"]
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user.friends, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_friend_requests(request):
    serializer = FriendRequestSerializer(request.user.friend_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@rate_limit(limit=3, period=60)
def send_friend_request(request):
    print(request.data)
    serializer = FriendRequestSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_friend_request(request):
    print(request.data)
    friend_request = get_object_or_404(FriendRequest, id=request.data['params']["id"])
    serializer = FriendRequestSerializer(friend_request, data=request.data['body'], partial=True)
    if serializer.is_valid():
        friend_request.status = request.data['body']["status"]
        if request.data['body']["status"] == "accepted":
            friend_request.receiver.friends.add(friend_request.sender)
            friend_request.sender.friends.add(friend_request.receiver)
        friend_request.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView, TokenUserMixin):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        django_user = self.get_user_from_token()
        user = get_object_or_404(User, email=django_user.email)
        serializer = UserResponseSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class FriendListView(ListAPIView, TokenUserMixin):
    serializer_class = UserResponseSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
        
    def get_queryset(self):
        django_user = self.get_user_from_token()
        print(django_user.email)
        user = get_object_or_404(User, email=django_user.email)
        print(user.email)
        return user.friends.all()
    


class FriendRequestListView(ListAPIView, TokenUserMixin):
    serializer_class = FriendRequestSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        django_user = self.get_user_from_token()
        print(self.request.query_params)
        print(django_user)
        user = get_object_or_404(User, email=django_user.email)
        if self.request.query_params["filter"] == "sent":
            print(user.email)
            return FriendRequest.objects.filter(sender=user.email)
        elif self.request.query_params["filter"] == "received":
            print(user.email)
            return FriendRequest.objects.filter(receiver=user.email)
        return FriendRequest.objects.none()
    
    

class UserSearchView(ListAPIView):
    serializer_class = UserSerializer 
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        query = self.request.query_params["q"]
        if query:
            return User.objects.filter(Q(name__icontains=query)|Q(email__icontains=query))
        return User.objects.none()