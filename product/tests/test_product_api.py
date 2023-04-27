"""
Tests for the product API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Product,
    TagConnector,
    CategoryConnector,
    DiscountConnector,
)

from product.serializers import ProductSerializer


PRODUCTS_URL = reverse('product:product-list')

def detail_url(product_id):
    """Create and return a product detail url."""
    return reverse('product:product-detail', args=[product_id])

def create_tag(**params):
    """Create and return a sample tag"""
    product = Product.objects.create(**params)
    return product


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)


def create_super_user(email='user@example.com', password='testpass123'):
    """Create and return a superuser."""
    user = get_user_model().objects.create_superuser(email = email, password = password)
    return user


class PublicProductApiTests(TestCase):
    """Test unauthenticated api requests for product"""
    def setUp(self):
        self.client = APIClient()
    
    def test_retrieve_products(self):
        """Test auth is required for retrieving products."""
        res = self.client.get(PRODUCTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)