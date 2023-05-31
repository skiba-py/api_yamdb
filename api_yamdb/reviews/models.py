from django.db import models

from users.models import User


class Genre(models.Model):
    '''Модель жанров.'''
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    '''Модель категорий.'''
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    '''Модель произведений.'''
    name = models.CharField('Название произведения', max_length=100)
    description = models.TextField('Описание')
    genre = models.ManyToManyField(Genre, through='Genre')

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='category',
        verbose_name='Категория',
        null=True,
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='genre',
        verbose_name='Жанр',
        null=True,
    )

    class Meta:
        verbose_name='Произведение'
        verbose_name_plural='Произведения'

    def __str__(self):
        return self.name


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    
    class Meta:
        verbose_name='Комментарий'
        verbose_name_plural='Комментарии'

    def __str__(self):
        return self.text
    

class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review')

    class Meta:
        verbose_name='Отзыв'
        verbose_name_plural='Отзывы'

    def __str__(self):
        return self.text

