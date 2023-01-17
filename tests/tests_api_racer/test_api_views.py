from http import HTTPStatus

import pytest
import xmltodict

from tests.conftest import DATA_VALUE, FULL_DATA
from web_report import handle_response

DR_URL = '/api/v1/drivers/'
REP_URL = '/api/v1/report/'


@pytest.mark.parametrize('param, expected_result', [
    (f'{REP_URL}''?format=json', HTTPStatus.OK),
    (f'{REP_URL}''?format=xml', HTTPStatus.OK),
    (f'{REP_URL}''?format=fake_format', HTTPStatus.BAD_REQUEST),
    (f'{DR_URL}''?format=json&order=desc', HTTPStatus.OK),
    (f'{DR_URL}''?format=xml&order=desc', HTTPStatus.OK),
    (f'{DR_URL}''?format=xml&order=asc', HTTPStatus.OK),
    (f'{DR_URL}''?format=json&order=asc', HTTPStatus.OK),
    (f'{DR_URL}''?format=json', HTTPStatus.OK),
    (f'{DR_URL}''?format=xml', HTTPStatus.OK),
    (f'{DR_URL}''?format=fake_format', HTTPStatus.BAD_REQUEST),
    (f'{DR_URL}''driver_id=SVF?format=xml', HTTPStatus.OK),
    (f'{DR_URL}''driver_id=SVF?format=json', HTTPStatus.OK),
    (f'{DR_URL}''driver_id=SVF?format=fake_format', HTTPStatus.BAD_REQUEST),
])
def test_links_to_resp_status(get_drivers, data_code, param, expected_result, client):
    response = client.get(param)
    assert expected_result == response.status_code


@pytest.mark.parametrize('param, expected_result', [('json', HTTPStatus.OK), ('xml', HTTPStatus.OK)])
def test_handle_response(param, expected_result, app):
    with app.app_context():
        resp = app.make_response(handle_response(from_request=param, racer=FULL_DATA))
    assert expected_result == resp.status_code


@pytest.mark.parametrize('param, expected_result',
                         [('?format=json', FULL_DATA),
                          ('/undefined_page/', None)])
def test_report_api_json(get_drivers, client, param, expected_result):
    response = client.get(f'{REP_URL}{param}')
    assert expected_result == response.json


def test_report_api_xml(get_drivers, client):
    response = client.get(f'{REP_URL}''?format=xml')
    content = xmltodict.parse(response.get_data())
    for value in DATA_VALUE:
        assert value in str(content)


@pytest.mark.parametrize('param, expected_result',
                         [('?format=json&order=desc', FULL_DATA),
                          ('/undefined_page/', None)])
def test_report_api_asc_json(get_drivers, client, param, expected_result):
    response = client.get(f'{REP_URL}{param}')
    assert expected_result == response.json


@pytest.mark.parametrize('param', ['?format=xml&order=desc', '?format=xml&order=asc'])
def test_report_api_asc_xml(get_drivers, client, param):
    response = client.get(f'{REP_URL}{param}')
    content = xmltodict.parse(response.get_data())
    for value in DATA_VALUE:
        assert value in str(content)


@pytest.mark.parametrize('param, expected_result',
                         [('driver_id=SVF?format=json', FULL_DATA),
                          ('/undefined_page/', None)])
def test_report_api_asc_json(data_code, client, param, expected_result):
    response = client.get(f'{DR_URL}{param}')
    assert expected_result == response.json


def test_detail_driver_api_xml(data_code, get_drivers, client):
    response = client.get(f'{DR_URL}''driver_id=SVF?format=xml')
    content = xmltodict.parse(response.get_data())
    for value in DATA_VALUE:
        assert value in str(content)
