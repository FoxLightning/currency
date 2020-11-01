import json
import os
from unittest.mock import MagicMock

import pytest

from rate import tasks
from rate.models import Rate


external_data = ['src', 'tests', 'rate', 'external_data']

func_data_json = [
        (tasks.parse_privatbank, 'parse_privatbank.json'),
        (tasks.parse_monobank, 'parse_monobank.json'),
        (tasks.parse_vkurse, 'parse_vkurse.json'),
    ]

func_data_html = [
    (tasks.parse_alpha, 'parse_alpha.html'),
    (tasks.parse_oschadbank, 'parse_oschadbank.html'),
    (tasks.parse_prostobank, 'parse_prostobank.html'),
    # (tasks.parse_minfin, 'parse_minfin.html'),  # not a bank
    (tasks.parse_ukrgasbank, 'parse_ukrgasbank.html'),
    (tasks.parse_pumb, 'parse_pumb.html'),
    (tasks.parse_pravex, 'parse_pravex.html'),
]


@pytest.mark.parametrize("func,data", func_data_json)
def test_banks_json_2(func, data, mocker):
    count_rates = Rate.objects.count()
    json_file = open(os.path.join(*external_data, data))

    currencies = json.load(json_file)
    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = MagicMock(
        status_code=200,
        json=lambda: currencies
    )
    for _ in range(3):
        func()
        assert Rate.objects.count() - count_rates == 2


@pytest.mark.parametrize("func,data", func_data_html)
def test_banks_html(func, data, mocker):
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
