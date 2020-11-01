import json
import os
from unittest.mock import MagicMock

from rate import tasks
from rate.models import Rate

external_data = ['src', 'tests', 'rate', 'external_data']


def test_banks_json(mocker):
    func_data = [
        (tasks.parse_privatbank, 'parse_privatbank.json'),
        (tasks.parse_monobank, 'parse_monobank.json'),
        (tasks.parse_vkurse, 'parse_vkurse.json'),
    ]
    for func, data in func_data:
        count_rates = Rate.objects.count()
        json_file = open(os.path.join(*external_data, data))

        currencies = json.load(json_file)
        requests_get_patcher = mocker.patch('requests.get')
        requests_get_patcher.return_value = MagicMock(
            status_code=200,
            json=lambda: currencies
        )
        for _ in range(2):
            func()
            assert Rate.objects.count() - count_rates == 2


def test_banks_html(mocker):
    func_data = [
        (tasks.parse_alpha, 'parse_alpha.html'),
        (tasks.parse_oschadbank, 'parse_oschadbank.html'),
        (tasks.parse_prostobank, 'parse_prostobank.html'),
        # (tasks.parse_minfin, 'parse_minfin.html'),
        (tasks.parse_ukrgasbank, 'parse_ukrgasbank.html'),
        (tasks.parse_pumb, 'parse_pumb.html'),
        (tasks.parse_pravex, 'parse_pravex.html'),
    ]
    for func, data in func_data:
        count_rates = Rate.objects.count()
        html_file = open(os.path.join(*external_data, data))
        txt_file = '\n'.join(html_file.readlines())
        requests_get_patcher = mocker.patch('requests.get')
        requests_get_patcher.return_value = MagicMock(
            status_code=200,
            text=txt_file
        )
        for _ in range(3):
            func()
            assert Rate.objects.count() - count_rates == 2

# def test_parse_privatbank(mocker):
#     count_rates = Rate.objects.count()
#     json_file = open(os.path.join(*external_data, '1_privatbank.json'))

#     currencies = json.load(json_file)
#     requests_get_patcher = mocker.patch('requests.get')
#     requests_get_patcher.return_value = MagicMock(
#         status_code=200,
#         json=lambda: currencies
#     )
#     tasks.parse_privatbank()
#     assert Rate.objects.count() - count_rates == 2

#     # we save rates if amount of buy or sale field was changed
#     tasks.parse_privatbank()
#     assert Rate.objects.count() - count_rates == 2


# def test_parse_monobank(mocker):
#     json_file = open(os.path.join(*external_data, '2_monobank.json'))
#     currencies = json.load(json_file)
#     requests_get_patcher = mocker.patch('requests.get')
#     count_rates = Rate.objects.count()
#     requests_get_patcher.return_value = MagicMock(
#         status_code=200,
#         json=lambda: currencies
#     )
#     tasks.parse_monobank()
#     assert Rate.objects.count() - count_rates == 2
#     tasks.parse_monobank()
#     assert Rate.objects.count() - count_rates == 2
