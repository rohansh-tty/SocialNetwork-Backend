from django.urls import path
from app.views import signup, login, send_friend_request, update_friend_request, FriendListView, UserSearchView, FriendRequestListView, UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup', signup, name='signup'),
    path('add-friend', send_friend_request, name="add-friend"),
    path('update-friend-request', update_friend_request, name="update-friend-request"),
    path('remove-friend',login, name="remove-friend"),
    path('friends', FriendListView.as_view(), name="friends"),
    path('search', UserSearchView.as_view(), name="search"),
    path('friend-requests', FriendRequestListView.as_view(), name="friend-requests"),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile', UserProfileView.as_view(), name="profile"),

]

