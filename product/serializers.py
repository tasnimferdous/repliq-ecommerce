from rest_framework import serializers

from core.models import Category


class CategorySerializer(serializers.Serializer):
    user = serializers.CharField(read_only = True)
    category_name = serializers.CharField(max_length = 255)
    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.category_name = validated_data.get('category_name', instance.category_name)
        instance.save()
        return instance