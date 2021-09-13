from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError


User = get_user_model()

def validate_rating(rating):
    if rating < 0:
        raise ValidationError(('Рейтинг не может быть ниже 0'),params={'rating': rating},)
    elif rating > 5:
        raise ValidationError(('Рейтинг не может быть выше 5'),params={'rating': rating},)
    else:
        return rating


class Lesson(models.Model):
    title = models.CharField(max_length=50)
    preview = models.ImageField(upload_to='previews')
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='author')
    video = models.FileField(upload_to='videos')
    text = models.TextField()


class Comment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='comment')
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)


class Rating(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='rating_lesson')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='rating_user')
    rating = models.SmallIntegerField(default=0, validators=[validate_rating])


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=False)