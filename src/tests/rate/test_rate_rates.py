from django.urls import reverse


def test_rate_list(client):
    response = client.get(reverse('rate:list'))
    assert response.status_code == 200


def test_rate_latestrates(client):
    response = client.get(reverse('rate:latestrates'))
    assert response.status_code == 200


def test_rate_downloadlatestrates(client):
    response = client.get(reverse('rate:downloadlatestrates'))
    assert response.status_code == 200


# def test_rate_deleterate(client):
#     response = client.get(reverse('rate:deleterate'))
#     assert response.status_code == 200


# def test_rate_updaterate(client):
#     response = client.get(reverse('rate:updaterate'))
#     assert response.status_code == 200
