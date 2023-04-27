from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Category
from product.serializers import CategorySerializer

# Create your views here.

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

