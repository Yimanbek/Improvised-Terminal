import pytest
from order.models import Order, OrderItem
from product.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_add_product_to_order(api_client):
    admin_user = User.objects.create_superuser(email='admin@example.com', password='test2025', name='test')
    api_client.force_authenticate(user=admin_user)
    order = Order.objects.create()
    product = Product.objects.create(name='product1', description='descriptionssss', quantity=10, price=100,  status=True)

    url = f'/order/order-item/add-product/{order.id}/'
    data = {'product': product.id, 'quantity': 2}
    resp = api_client.post(url, data, format='json')

    assert resp.status_code == 201
    assert OrderItem.objects.count() == 1

    item_id = resp.data['id']
    item = OrderItem.objects.get(id = item_id)

    assert item.product == product
    assert item.quantity == 2

    product.refresh_from_db()
    assert product.quantity == 8

    order.refresh_from_db()
    assert float(order.total_amount_to_paid) == 200.00

@pytest.mark.django_db
def test_remove_order_item(api_client):
    admin_user = User.objects.create_superuser(email='admin@example.com', password='test2025', name='test')
    api_client.force_authenticate(user=admin_user)
    order = Order.objects.create()
    product = Product.objects.create(name='product1', description='descriptionssss', quantity=10, price=100,  status=True)

    url = f'/order/order-item/add-product/{order.id}/'
    data = {'product': product.id, 'quantity': 2}
    resp = api_client.post(url, data, format='json')

    item_id = resp.data['id']
 
    item = OrderItem.objects.get(id=item_id) 

    product.refresh_from_db()
    order.refresh_from_db()
    assert product.quantity == 8

    url = f'/order/order-item/{item.id}/'
    resp = api_client.delete(url)
    assert resp.status_code == 204

    product.refresh_from_db()
    assert product.quantity == 10