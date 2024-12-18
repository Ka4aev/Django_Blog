from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class User(AbstractUser):
    full_name = models.CharField(max_length=254, verbose_name="Полное имя")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    bio = models.TextField(blank=True, verbose_name="Информация о пользователе")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.full_name


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Автор")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое поста")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата и время публикации")
    likes = models.ManyToManyField(get_user_model(), related_name='liked_posts', blank=True, verbose_name="Лайки")

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.comments.count()

    def get_likes_count(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, verbose_name="Пост")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Автор комментария")
    content = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата и время комментария")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата и время обновления комментария")

    def __str__(self):
        return f"Комментарий от {self.author} на пост {self.post}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} лайкнул {self.post}"

    class Meta:
        unique_together = ('post', 'user')


