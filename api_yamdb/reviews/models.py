from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg

User = get_user_model()

MAX_LENGTH_NAME = 256
MAX_LENGTH_SLUG = 50


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=MAX_LENGTH_NAME
    )
    slug = models.SlugField(
        'Идентификатор категории',
        max_length=MAX_LENGTH_SLUG, unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)
        indexes = [
            models.Index(fields=['slug'], name='category_slug_idx')
        ]

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=MAX_LENGTH_NAME
    )
    slug = models.SlugField(
        'Идентификатор жанра',
        max_length=MAX_LENGTH_SLUG, unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)
        indexes = [
            models.Index(fields=['slug'], name='genre_slug_idx')
        ]

    def __str__(self):
        return self.name


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанры'
    )

    name = models.CharField(
        'Название произведения',
        max_length=MAX_LENGTH_NAME
    )
    year = models.IntegerField('Год выхода')
    description = models.TextField('Описание')

    @property
    def rating(self):
        return (
            self.reviews.aggregate(average_score=Avg('score'))['average_score']
        )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('year',)
        default_related_name = 'titles'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['genre', 'title'],
                name='unique_genre_title'
            )
        ]

    def __str__(self):
        return f'{self.genre}, {self.title}'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    text = models.TextField('Текст')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1, 'Оценка не может быть меньше 1!'),
            MaxValueValidator(10, 'Оценка не может быть больше 10!'),
        ]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        ordering = ['-pub_date', ]
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date', ]
        default_related_name = 'comments'

    def __str__(self):
        return self.text
