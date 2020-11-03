from django.urls import reverse


def test_rate_feedback(client):
    response = client.get(reverse('rate:feedback'))
    assert response.status_code == 200


def test_rate_showrating(client):
    response = client.get(reverse('rate:showrating'))
    assert response.status_code == 200


def test_rate_error(client):
    response = client.get(reverse('rate:error'))
    assert response.status_code == 200
