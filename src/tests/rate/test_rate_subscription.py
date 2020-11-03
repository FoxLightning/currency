from django.urls import reverse


# def test_rate_sublist(client):
#     response = client.get(reverse('rate:sublist'))
#     assert response.status_code == 200


# def test_rate_dellsub(client):
#     response = client.get(reverse('rate:dellsub'))
#     assert response.status_code == 200


def test_rate_addsubscription(client):
    response = client.get(reverse('rate:addsubscription'))
    assert response.status_code == 200
