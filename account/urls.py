from django.urls import path,include
from account.views import UserRegistrationView,UserLoginView,UserProfileView,UserListView,UserDetailView

urlpatterns = [
    path('user/register/',UserRegistrationView.as_view(),name='register'),
    path('user/login/',UserLoginView.as_view(),name='login'),
    path('user/profile/',UserProfileView.as_view(),name='Profile'),
    path('users/',UserListView.as_view(),name='Users'),
    path('users/<int:user_id>/',UserDetailView.as_view(),name='UserDetail'),
]