from django.core.exceptions import ObjectDoesNotExist
from django_filters import rest_framework as rest_filter
from rest_framework import viewsets, filters, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as rf

from .models import Post, Comment, Rating, Like, Favourite
from .serializers import PostListSerializer, PostDetailSerializer, CreatePostSerializer, CommentSerializer, \
    RatingSerializer, FavouritePostsSerializer
from .permissions import IsAuthorOrIsAdmin, IsAuthor


class PostFilter(rest_filter.FilterSet):
    created = rest_filter.DateTimeFromToRangeFilter()

    class Meta:
        model = Post
        fields = ('status', 'created')


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer
    filter_backends = [rest_filter.DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_class = PostFilter
    search_fields = ['title', 'body']
    ordering_fields = ['created', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        return CreatePostSerializer

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, user=user)
            like.is_liked = not like.is_liked
            if like.is_liked:
                like.save()
            else:
                like.delete()
            message = 'нравится' if like.is_liked else 'ненравится'
        except Like.DoesNotExist:
            Like.objects.create(post=post, user=user, is_liked=True)
            message = 'нравится'
        return Response(message, status=200)

    @action(['POST'], detail=True)
    def favourite(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            favourite = Favourite.objects.get(post=post, user=user)
            favourite.is_favourite = not favourite.is_favourite
            if favourite.is_favourite:
                favourite.save()
            else:
                favourite.delete()
            message = 'добавлено в избранные' if favourite.is_favourite else 'удалено из избранных'
        except Favourite.DoesNotExist:
            Favourite.objects.create(post=post, user=user, is_favourite=True)
            message = 'добавлено в избранные'
        return Response(message, status=200)

    def get_permission(self):
        if self.action == 'create' or self.action == 'like' or self.action == 'favourite':
            return [IsAuthenticated()]
        return [IsAuthorOrIsAdmin()]


class CommentsViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permission(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthor()]


class RatingViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthor()]


class FavouritesListView(ListAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouritePostsSerializer
    filter_backends = [rf.DjangoFilterBackend]
    filterset_fields = ['user', ]
