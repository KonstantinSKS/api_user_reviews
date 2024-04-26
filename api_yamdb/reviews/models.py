from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year

from users.models import User


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='адрес',
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:15]


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='адрес',
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:15]


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=(validate_year,)
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Slug жанра',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Slug категории',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.IntegerField(
        verbose_name='Оценка произведения',
        validators=[
            MaxValueValidator(10, message='Score должен быть меньше 10!'),
            MinValueValidator(1, message='Score должен быть больше 1!')
        ]
    )
    title = models.ForeignKey(Title, verbose_name='title',
                              on_delete=models.CASCADE,
                              related_name='reviews')
    author = models.ForeignKey(User, verbose_name='user',
                               on_delete=models.CASCADE,
                               related_name='reviews')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ('-pub_date', )
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments', verbose_name='отзыв'
    )
    text = models.TextField(verbose_name='текст комментария')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True)

    author = models.ForeignKey(User, verbose_name='user',
                               on_delete=models.CASCADE,
                               related_name='comments')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ('-pub_date', )

    def __str__(self):
        return self.text[:15]
