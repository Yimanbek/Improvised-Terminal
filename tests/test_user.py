import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_create_superuser():
    user = User.objects.create_superuser(email="admin@example.com", password="test2025", name='test')
    assert user.is_staff is True
    assert user.is_superuser is True
    assert user.email == "admin@example.com"

@pytest.mark.django_db
def test_create_user(api_client):
    admin_user = User.objects.create_superuser(email='admin@example.com', password='test2025', name='test')
    api_client.force_authenticate(user=admin_user)

    response = api_client.post('/user/admin/create/', {'email':'admintwo@example.com', 'password':'test2025', 'name':'test'}, format='json')

    assert response.status_code == 201
    assert User.objects.count() == 2
    user = User.objects.first()
    assert user.name == 'test'