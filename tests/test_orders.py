import pytest
from order.models import Order

@pytest.mark.django_db
def test_create_order(api_client):
    url = '/order/order-create/'
    response = api_client.post(url, {}, format='json')
    assert response.status_code == 201
    assert Order.objects.count() == 1
    order = Order.objects.first()
    assert order.status == 'pending'
    assert order.total_amount_to_paid == 0

@pytest.mark.django_db
def test_pay_order(api_client):
    order = Order.objects.create(total_amount_to_paid=100.00)
    url = f'/order/order-paid/{order.pk}/paid/'
    data = {'amount': 150.00}
    response = api_client.post(url, data, format='json')
    assert response.status_code == 200

    order.refresh_from_db()
    assert order.status == 'paid'
    assert float(order.odd_money) == 50.0
