from django_filters import rest_framework as rest_filters, NumberFilter, CharFilter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import *
from rest_framework.response import Response

from .models import *
from .serializers import *
from django_filters import rest_framework as filters
from .permissions import *


class LessonFilter(filters.FilterSet):
    class Meta:
        model = Lesson
        fields = ('user', )

from rest_framework import filters


class LessonView(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [rest_filters.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = LessonFilter
    search_fields = ['title']

    def get_serializer_class(self):
        if self.action == 'list':
            return LessonSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'like']:
            return [IsAuthorOrIsAdmin()]
        elif self.action in ['like']:
            return [IsAuthenticated()]
        return []
        return []

    @action(detail=True, methods=['post'])
    def like(self, request, pk):
        lesson = self.get_object()
        user = request.user
        like_obj, created = Like.objects.get_or_create(lesson=lesson, user=user)
        if like_obj.is_liked:
            like_obj.is_liked = False
            like_obj.save()
            return Response('disliked')
        else:
            like_obj.is_liked = True
            like_obj.save()
            return Response('liked')


class CommentsView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return []


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class RatingView(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return []


class FavoriteView(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}
