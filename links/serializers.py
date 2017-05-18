from links.models import Link
from rest_framework import serializers


class LinkSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    published_at = serializers.SerializerMethodField(source="created")
    url = serializers.URLField()
    author = serializers.CharField(read_only=True)
    tags = serializers.CharField(required=False)

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        return Link.objects.create(**validated_data)

    def get_published_at(self, obj):
        return obj.created
