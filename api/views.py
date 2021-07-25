from rest_framework import viewsets,  generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Post, Image, Profile, Comment
from .serializers import PostSerializer, ImageSerializer, ProfileSerializer, CommentSerializer, UserSerializer
from .pagenation import CustomPagination


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # リクエストからユーザをセットする
    def perform_create(self, serializer):
        serializer.save(userProfile=self.request.user)


class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # クエリのフィルター
    def get_queryset(self):
        return self.queryset.filter(userProfile=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(userPost=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-created_at')
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        return queryset


class MyPostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # クエリのフィルター
    def get_queryset(self):
        return self.queryset.filter(userPost=self.request.user)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def list(self, request):
        response = {'message': 'GET method is not allowed'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk=None):
        response = {'message': 'GET method is not allowed'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(userComment=self.request.user)
