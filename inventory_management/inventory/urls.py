from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)


urlpatterns = [
    # To register a new user
    path('auth/register/', RegisterView.as_view(), name='register'),
    # To login
    path('auth/login/', LoginView.as_view(), name='login'),
    # To create a new item
    path('items/', ItemCreateView.as_view(), name='item-create'),
    # To perform Get, Update and Delete operation on Item
    path('item/<int:item_id>/', IndividualItemOperationView.as_view(), name='item-detail'),

    # Token retrieval endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
