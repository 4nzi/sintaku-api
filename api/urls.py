from django.urls import path, include
from .views import PostViewSet, ImageViewSet, ProfileViewSet, CommentViewSet, CreateUserView, MyProfileListView, MyPostListView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('images', ImageViewSet)
router.register('profiles', ProfileViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls.jwt')),
    path('register/', CreateUserView.as_view(), name='register'),
    path('myprofile/', MyProfileListView.as_view(), name='myprofile'),
    path("myposts/", MyPostListView.as_view(), name="myposts")
]
