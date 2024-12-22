from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь со встроенной моделью User
    rating = models.IntegerField(default=0)  # рейтинг пользователя

    def update_rating(self):
        """Обновление рейтинга текущего автора"""
        post_ratings = sum(post.rating for post in self.post_set.all()) * 3  #  Суммируем рейтинги всех статей автора, умножаем на 3
        comment_ratings = sum(comment.rating_comment for comment in self.user.comments.all())  # Суммируем рейтинги всех комментариев автора
        # Суммируем рейтинги всех комментариев к статьям автора
        for post in self.post_set.all():
            comment_ratings += sum(comment.rating_comment for comment in post.comments.all())

        self.rating = post_ratings + comment_ratings
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'

    POST_TYPE_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # 'связь один ко многим' с моделью Author
    choice_type = models.CharField(max_length=2, choices=POST_TYPE_CHOICES)  # Выбор типа сообщения
    time_in = models.DateTimeField(auto_now_add=True)  # автоматическое добавление даты и времени при создании поста
    categories = models.ManyToManyField(Category, through='PostCategory')  # 'связь многие ко многим' через PostCategory
    title = models.CharField(max_length=128)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        """Получаем начало статьи"""
        return self.content[:124] + '...' if len(self.content) > 124 else self.content

    def like(self):
        """Увеличиваем рейтинг"""
        self.rating += 1
        self.save()

    def dislike(self):
        """Уменьшаем рейтинг"""
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_comment = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)  # автоматическое добавление даты и времени при создании поста
    rating_comment = models.IntegerField(default=0)

    def like(self):
        """Увеличиваем рейтинг"""
        self.rating_comment += 1
        self.save()

    def dislike(self):
        """Уменьшаем рейтинг"""
        self.rating_comment -= 1
        self.save()
