from rest_framework import serializers

from core.models import Category


class CategorySerializer(serializers.Serializer):
    category_name = serializers.CharField(max_length = 255)
    def create(self, validated_data):
        return Category.objects.create(**validated_data)