from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Comment, Movie
from .serializers import (CommentViewSerializer, MovieDetailSerializer,
                          MovieListSerializer)


class MultipleSerializerMixin:

    detail_serializer_class = None
    partial_update_serializer_class = None
    create_serializer_class = None

    def get_serializer_class(self):
        return {
            "retrieve": self.detail_serializer_class,
            "partial_update": self.partial_update_serializer_class,
            "create": self.create_serializer_class,
        }.get(self.action, super().get_serializer_class())


class MovieViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = MovieListSerializer
    detail_serializer_class = MovieDetailSerializer

    def get_queryset(self):
        return Movie.objects.all()

    @action(detail=True, methods=['GET'])
    def comments(self, _, pk=None):
        movie = get_object_or_404(Movie, pk=pk)
        comments = Comment.objects.filter(movie=movie)
        serializer = CommentViewSerializer(comments, many=True)
        return Response(serializer.data)


class CommentViewSet(ModelViewSet):

    serializer_class = CommentViewSerializer

    def get_queryset(self):
        return Comment.objects.all()
