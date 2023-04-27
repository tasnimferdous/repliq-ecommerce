"""
Tests for the tag API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from product.serializers import TagSerializer


TAGS_URL = reverse('product:tag-list')

def detail_url(tag_id):
    """Create and return a tag detail url."""
    return reverse('product:tag-detail', args=[tag_id])

def create_tag(user = None, **params):
    """Create and return a sample tag"""
    tag = {
        'tag_name': 'sample tag',
    }
    tag.update(params)
    tag = Tag.objects.create(user = user, **params)
    return tag


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)


def create_super_user(email='user@example.com', password='testpass123'):
    """Create and return a superuser."""
    user = get_user_model().objects.create_superuser(email = email, password = password)
    return user


class PublicTagsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_tags(self):
        """Test auth is required for retrieving tags."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_super_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_tag_success(self):
        """Test creating a tag successfully"""
        payload = {
            'user' : self.user,
            'tag_name': 'test tag',
        }
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        tag = Tag.objects.get(tag_name=payload['tag_name'])
        self.assertEqual(tag.user, self.user)
        self.assertEqual(res.data['tag_name'], tag.tag_name)
        # self.assertNotIn('password', res.data)
    
    def test_update_tag_success(self):
        """Test update of a tag"""
        # original_color = 'Maroon'
        tag = create_tag(
            user = self.user,
            tag_name = 'test tag',
        )
        payload = {'tag_name':'updated tag'}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.tag_name, payload['tag_name'])
        self.assertEqual(tag.user, self.user)
    
    def test_delete_tag(self):
        """Test deleting a tag successful."""
        tag = create_tag(user=self.user, tag_name='test tag')

        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(id=tag.id).exists())