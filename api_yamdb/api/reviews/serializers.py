from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title
)

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    description = serializers.CharField(required=False)

    rating = serializers.IntegerField(default=0, read_only=True)

    class Meta:
        model = Title
        fields = [
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
            'rating'
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = CategorySerializer(instance.category).data
        response['genre'] = GenreSerializer(
            instance.genre.all(), many=True
        ).data
        return response


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    description = serializers.CharField(required=False)
    rating = serializers.IntegerField(default=0)

    class Meta:
        model = Title
        fields = [
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
            'rating'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    def validate(self, attrs):
        request = self.context['request']
        if request.method != 'POST':
            return attrs
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            not Review.objects
            .filter(title=title, author=request.user)
            .exists()
        ):
            return attrs
        raise ValidationError('Может существовать только один отзыв!')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        read_only_fields = ('review',)
        model = Comment
