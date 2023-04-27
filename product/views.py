from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Category,
    Tag,
    Discount,
)
from product.serializers import (
    CategorySerializer,
    TagSerializer,
    DiscountSerializer,
)

# Category views---------------------------------------------------
class CategoryView(APIView):
    serializer_class = CategorySerializer()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data['user'] = request.user
            serializer.create(validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CategoryDetailView(APIView):
    serializer_class = CategorySerializer()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        category = Category.objects.get(pk = id)
        serializer = CategorySerializer(category, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        category = Category.objects.get(pk = id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Tag views--------------------------------------------------------
class TagView(APIView):
    serializer_class = TagSerializer()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        tag = Tag.objects.all()
        serializer = TagSerializer(tag, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TagSerializer(data = request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data['user'] = request.user
            serializer.create(validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TagDetailView(APIView):
    serializer_class = TagSerializer()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        tag = Tag.objects.get(pk = id)
        serializer = TagSerializer(tag, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        tag = Tag.objects.get(pk = id)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Discount views--------------------------------------------------------
class DiscountView(APIView):
    serializer_class = DiscountSerializer()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        discount = Discount.objects.all()
        serializer = DiscountSerializer(discount, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DiscountSerializer(data = request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data['user'] = request.user
            serializer.create(validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DiscountDetailView(APIView):
    serializer_class = DiscountSerializer()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        discount = Discount.objects.get(pk = id)
        serializer = DiscountSerializer(discount, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        discount = Discount.objects.get(pk = id)
        discount.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

