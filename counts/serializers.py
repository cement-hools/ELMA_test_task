from rest_framework import serializers
from rest_framework.serializers import Serializer


class UrlSerializer(Serializer):
    url = serializers.URLField()
    query = serializers.CharField()


class ResultSerializer(Serializer):
    url = serializers.URLField()
    count = serializers.IntegerField()
    status = serializers.CharField()


class QuerySerializer(Serializer):
    """Сериалайзер событий."""

    urls = UrlSerializer(many=True, required=True)
    max_timeout = serializers.IntegerField(required=True)


class AnswerSerializer(Serializer):
    """Сериалайзер событий."""

    urls = ResultSerializer(many=True)
