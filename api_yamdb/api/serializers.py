from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from reviews.models import Review, Comment, Genre, Category, Title
from users.models import User


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        max_length=150,
        required=True,
    )

    class Meta:
        model = User

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError("username can't be me")
        return value

    def validate(self, data):
        email = data.get("email")
        username = data.get("username")
        user_email_exists = User.objects.filter(email=email).exists()
        user_username_exists = User.objects.filter(username=username).exists()
        if (user_email_exists
                and not user_username_exists):
            raise serializers.ValidationError(
                "User with such email already exists")
        if (not user_email_exists
                and user_username_exists):
            raise serializers.ValidationError(
                "User with such username already exists")
        return data


class JwtSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        max_length=150,
        required=True,
    )
    confirmation_code = serializers.CharField(
        max_length=150, required=True
    )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class UserMeSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ("role",)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)


class TitleCreateOrUpdateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        year = timezone.now().year
        if year < value:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!')
        return value


class TitleReadOnlySerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=1)
    title = serializers.HiddenField(default=1)
    score = serializers.IntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(10))
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title', )
        read_only_fields = ('id', 'pub_date', )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = self.context.get('title')
            author_id = self.context.get('author')
            if Review.objects.filter(
                    title=title_id, author=author_id).exists():
                raise serializers.ValidationError(
                    'Нельзя оставлять больше одного отзыва!')
        return data

    def validate_score(self, value):
        if isinstance(value, int) and value <= 10 and value >= 1:
            return value
        raise serializers.ValidationError(
            "The score is not an integer or/ and"
            "its value is not in the range from 1 to 10")


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault())
    review = serializers.HiddenField(default=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['review'].write_only = True

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review', )
        read_only_fields = ('id', 'pub_date', )
