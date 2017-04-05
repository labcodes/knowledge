from links.models import Link
from rest_framework import serializers


class LinkSerializer(serializers.Serializer):
    title = serializers.CharField()
    published_at = serializers.SerializerMethodField(source="created")
    url = serializers.URLField()
    author = serializers.CharField()
    tags = serializers.CharField()

    def get_published_at(self, obj):
        return obj.created
