"""
Tests for models.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def create_user(email = 'test@example.com', password = 'pass123'):
    """Create & return a new user"""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    """ Test model. """
    def test_create_user_with_email_successful(self):
        """ Test for creating a user with an email is successfull. """
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test for a user without an email to raise valueError"""
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user('', 'testpass123')

    def test_create_superuser(self):
        """Test for creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'testpass123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_category(self):
        """Test for creating category"""
        category = models.Category.objects.create(
            category_name = 'test category',
        )
        self.assertEqual(str(category), category.category_name)


    def test_create_tag(self):
        """Test for creating tag"""
        tag = models.Tag.objects.create(
            tag_name = 'test tag',
        )
        self.assertEqual(str(tag), tag.tag_name)

    def test_create_discount(self):
        """Test for creating discount"""
        discount = models.Discount.objects.create(
            discount_title = 'test discount',
            discount_percent = Decimal('20.2')
        )
        self.assertEqual(str(discount), discount.discount_title)

    def test_create_product(self):
        """Test creating a product successfully"""
        category = models.Category.objects.create(category_name='test category')
        discount = models.Discount.objects.create(
            discount_title = 'test discount',
            discount_percent = Decimal('20.2')
        )
        product = models.Product.objects.create(
            product_title = 'test product',
            product_price = Decimal('5.5'),
            product_color = 'test color',
            product_detail = 'test product detail',
            product_category = category,
            product_discount = discount,
        )
        self.assertEqual(str(product), product.product_title)
