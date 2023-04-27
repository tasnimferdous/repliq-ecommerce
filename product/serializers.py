from rest_framework import serializers

from core.models import (
    Category,
    Tag,
    Discount,
)


class CategorySerializer(serializers.Serializer):
    user = serializers.CharField(read_only = True)
    category_name = serializers.CharField(max_length = 255)
    
    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.category_name = validated_data.get('category_name', instance.category_name)
        instance.save()
        return instance


class TagSerializer(serializers.Serializer):
    user = serializers.CharField(read_only = True)
    tag_name = serializers.CharField(max_length = 255)

    def create(self, validated_data):
        return Tag.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.tag_name = validated_data.get('tag_name', instance.tag_name)
        instance.save()
        return instance


class DiscountSerializer(serializers.Serializer):
    user = serializers.CharField(read_only = True)
    discount_title = serializers.CharField(max_length = 255)
    discount_percent = serializers.DecimalField(max_digits=5, decimal_places=2)

    def create(self, validated_data):
        return Discount.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.discount_title = validated_data.get('discount_title', instance.discount_title)
        instance.discount_percent = validated_data.get('discount_percent', instance.discount_percent)
        instance.save()
        return instance