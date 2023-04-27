"""
Tests for the category API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Category

from product.serializers import CategorySerializer


CATEGORIES_URL = reverse('product:category-list')

def detail_url(category_id):
    """Create and return a category detail url."""
    return reverse('product:category-detail', args=[category_id])

def create_category(user = None, **params):
    """Create and return a sample category"""
    category = {
        'category_name': 'sample category',
    }
    category.update(params)
    category = Category.objects.create(user = user, **params)
    return category


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicCategoriesApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_categories(self):
        """Test auth is required for retrieving categories."""
        res = self.client.get(CATEGORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoriesApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_category_success(self):
        """Test creating a category successfully"""
        payload = {
            'user' : self.user,
            'category_name': 'test category',
        }
        res = self.client.post(CATEGORIES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        category = Category.objects.get(category_name=payload['category_name'])
        self.assertEqual(category.user, self.user)
        self.assertEqual(res.data['category_name'], category.category_name)
        # self.assertNotIn('password', res.data)
    
    def test_update_category_success(self):
        """Test update of a category"""
        # original_color = 'Maroon'
        category = create_category(
            user = self.user,
            category_name = 'test category',
        )
        payload = {'category_name':'updated category'}
        url = detail_url(category.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.category_name, payload['category_name'])
        self.assertEqual(category.user, self.user)
    
    def test_delete_category(self):
        """Test deleting a category successful."""
        category = create_category(user=self.user, category_name='test category')

        url = detail_url(category.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=category.id).exists())