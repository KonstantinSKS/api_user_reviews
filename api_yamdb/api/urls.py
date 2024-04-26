from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (get_jwt_token, signup, GenreViewSet, CategoryViewSet,
                    TitleViewSet, ReviewViewSet, CommentViewSet, UserViewSet)

app_name = 'api'


router_v1 = DefaultRouter()

router_v1.register(r"users", UserViewSet, basename="user")
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(r'^titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

auth_urlpatterns = [
    path('signup/', signup, name='signup'),
    path('token/', get_jwt_token, name='get_jwt_token'),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_urlpatterns)),
]
