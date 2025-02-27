import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from product.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_create_product(api_client):
    admin_user = User.objects.create_superuser(email='admin@example.com', password='test2025', name='test')
    api_client.force_authenticate(user=admin_user)

    url = '/product/create/'
    data = {'name': 'product1', 'description': 'descriptionssss', 'quantity': 10, 'price': 100}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201
    assert Product.objects.count() == 1
    product = Product.objects.first()
    assert product.name == 'product1'
    assert product.quantity == 10

@pytest.mark.django_db
def test_get_products(api_client):
    Product.objects.create(name='product1', description='descriptionssss', quantity=10, price=100, status=True)
    Product.objects.create(name='product1', description='descriptionssss', quantity=10, price=100, status=True)

    url = '/product/'
    response = api_client.get(url, format='json')
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['name'] == 'product1'
    assert response.data[1]['name'] == 'product1'

@pytest.mark.django_db
def test_get_detail_product(api_client):
    product = Product.objects.create(name='product1', description='descriptionssss', quantity=10, price=100, status=True)
    url = f'/product/{product.pk}/detail/'
    response = api_client.get(url, format='json')

    assert response.status_code == 200
    assert response.data['name'] == 'product1'

@pytest.mark.django_db
def test_update_product(api_client):
    admin_user = User.objects.create_superuser(email='admin@example.com', password='test2025', name='test')
    api_client.force_authenticate(user=admin_user)

    product = Product.objects.create(name='product1', description='descriptionssss', quantity=1, price=100, status=True)
    url = f'/product/{product.pk}/detail/'
    data = {'quantity': 50}
    response = api_client.patch(url, data, format='json')
    assert response.status_code == 200

    product.refresh_from_db()
    assert product.name == 'product1'
    assert product.quantity == 50

@pytest.mark.django_db
def test_delete_product(api_client):
    admin_user = User.objects.create_superuser(email='admin@example.com', password='test2025', name='test')
    api_client.force_authenticate(user=admin_user)

    product = Product.objects.create(name='product1', description='descriptionssss', quantity=10, price=100, status=True)
    url = f'/product/{product.pk}/detail/'
    response = api_client.delete(url, format='json')
    assert response.status_code == 204
    assert Product.objects.count() == 0