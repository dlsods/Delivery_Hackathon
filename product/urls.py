from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import PostsViewSet, CommentsViewSet, RatingViewSet, FavouritesListView

router = SimpleRouter()
router.register('posts', PostsViewSet, 'posts')
router.register('comments', CommentsViewSet, 'comments')
router.register('ratings', RatingViewSet, 'ratings')

urlpatterns = [
    path('', include(router.urls)),
    path('favourites_list/', FavouritesListView.as_view())
]
