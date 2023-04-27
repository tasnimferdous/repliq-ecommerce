"""
Tests for the discount API.
"""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Discount

from product.serializers import DiscountSerializer


DISCOUNTS_URL = reverse('product:discount-list')

def detail_url(discount_id):
    """Create and return a discount detail url."""
    return reverse('product:discount-detail', args=[discount_id])

def create_discount(**params):
    """Create and return a sample discount"""
    discount = Discount.objects.create(**params)
    return discount


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)


def create_super_user(email='user@example.com', password='testpass123'):
    """Create and return a superuser."""
    user = get_user_model().objects.create_superuser(email = email, password = password)
    return user


class PublicDiscountsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_discounts(self):
        """Test auth is required for retrieving discounts."""
        res = self.client.get(DISCOUNTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDiscountsApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_super_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_discount_success(self):
        """Test creating a discount successfully"""
        payload = {
            'user' : self.user,
            'discount_title': 'test discount',
            'discount_percent': Decimal('10.5'),
        }
        res = self.client.post(DISCOUNTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        discount = Discount.objects.get(discount_title=payload['discount_title'])
        self.assertEqual(discount.user, self.user)
        self.assertEqual(res.data['discount_title'], discount.discount_title)
    
    def test_update_discount_success(self):
        """Test update of a discount"""
        discount = create_discount(
            user = self.user,
            discount_title = 'test discount',
            discount_percent = Decimal('20')
        )
        payload = {
            'discount_title':'updated discount',
            'discount_percent':Decimal('30.5'),
        }
        url = detail_url(discount.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        discount.refresh_from_db()
        self.assertEqual(discount.discount_title, payload['discount_title'])
        self.assertEqual(discount.discount_percent, payload['discount_percent'])
        self.assertEqual(discount.user, self.user)
    
    def test_delete_discount(self):
        """Test deleting a discount successful."""
        discount = create_discount(
            user = self.user,
            discount_title = 'test discount',
            discount_percent = Decimal('20')
        )

        url = detail_url(discount.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Discount.objects.filter(id=discount.id).exists())