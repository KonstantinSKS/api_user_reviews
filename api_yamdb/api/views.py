from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import status

from .serializers import (JwtSerializer, UserSerializer, SignupSerializer,
                          GenreSerializer, CategorySerializer,
                          TitleCreateOrUpdateSerializer,
                          TitleReadOnlySerializer, UserMeSerializer,
                          ReviewSerializer, CommentSerializer)
from users.models import User
from reviews.models import Genre, Category, Title, Review
from . viewsets import CreateDestroyReadViewSet
from .permissions import (UpdatingNotYourContentPermission, IsAdminOrSuperUser,
                          IsAdminOrReadOnly)
from .filters import TitleFilter


@api_view(["POST"])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    email = serializer.validated_data.get("email")
    user, created = User.objects.get_or_create(
        email=email, username=username)
    if created:
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject="YaMDb signup",
            message=f"Your confirmation code is: {confirmation_code}",
            from_email=settings.EMAIL_ADMIN,
            recipient_list=[user.email],
        )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_jwt_token(request):
    serializer = JwtSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data.get("username")
    )
    token = serializer.validated_data.get("confirmation_code")
    if default_token_generator.check_token(user, token):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrSuperUser,)
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed('PUT')
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=["get", "patch"], url_path="me",
            permission_classes=(IsAuthenticated,),
            serializer_class=UserMeSerializer,
            )
    def my_profile(self, request):
        user = request.user
        if request.method == "PATCH":
            serializer = self.get_serializer(user, data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenreViewSet(CreateDestroyReadViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(CreateDestroyReadViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg(
        'reviews__score')).order_by('id')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadOnlySerializer
        return TitleCreateOrUpdateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (UpdatingNotYourContentPermission, )

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed('PUT')
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        reviews = title.reviews.all()
        return reviews

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['author'] = self.request.user
        context['title'] = self.kwargs.get('title_id')
        return context

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        author = self.request.user
        serializer.save(author=author, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (UpdatingNotYourContentPermission, )

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed('PUT')
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        author = self.request.user
        serializer.save(author=author, review=review)
