from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
import uuid


def upload_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['sintaku/avatars', str(instance.userProfile.id) + str(instance.nickName) + str(".") + str(ext)])


def upload_image_path(instance, filename):
    return '/'.join(['sintaku/posts', str(instance.post) + str("_") + str(filename)])


def upload_thum_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['sintaku/thums', str(instance.userPost.id) + str(instance.title) + str(".") + str(ext)])


# カスタムユーザー(email認証)
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Email is must')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, editable=False)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, editable=False)
    nickName = models.CharField(max_length=20)
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userProfile',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True,
                            upload_to=upload_avatar_path)

    def __str__(self):
        return self.nickName


class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, editable=False)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    thum = models.ImageField(blank=True, null=True, upload_to=upload_thum_path)
    created_at = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='liked', blank=True, )
    userPost = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userPost',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Image(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, editable=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='images')
    file = models.ImageField(upload_to=upload_image_path)
    caption = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.post) + " _ " + str(self.pk)


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, editable=False)
    text = models.CharField(max_length=100)
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userComment',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
