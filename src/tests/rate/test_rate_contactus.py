from django.urls import reverse

from rate.models import ContactUs


def test_rate_contactuslist(client):
    response = client.get(reverse('rate:contactuslist'))
    assert response.status_code == 200


def test_rate_contactuscreate(client):
    url = reverse('rate:contactuscreate')
    response = client.get(url)
    assert response.status_code == 200


def test_rate_contactuscreate_post_empty_data(client):
    start = ContactUs.objects.count()
    url = reverse('rate:contactuscreate')
    response = client.post(url, data={})
    assert response.status_code == 200
    assert response.context_data['form'].errors == {
        'email': ['This field is required.'],
        'subject': ['This field is required.'],
        'massage': ['This field is required.']
    }
    assert ContactUs.objects.count() == start


def test_rate_contactuscreate_post_wrong_email(client):
    start = ContactUs.objects.count()
    url = reverse('rate:contactuscreate')
    response = client.post(url, data={
        'email': 'wrongemail',
        'subject': 'word',
        'massage': 'word',
    })
    assert response.status_code == 200
    assert response.context_data['form'].errors == {
        'email': ['Enter a valid email address.']
    }
    assert ContactUs.objects.count() == start
