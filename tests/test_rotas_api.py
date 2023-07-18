from flask import Flask, request
from flask_testing import TestCase
from api_copiloto.main import *
import pytest
import requests_mock
from unittest.mock import Mock, mock_open, patch
from unittest import mock


@pytest.fixture
def data():
    data = {
        'cliente': 'teste',
        'checkbox': [1],
        'hw': [1],
        'alarme': [1],
        'input_1': 'teste',
        'input_2': 'teste',
        'input_3': 1,
    }
    return data


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<title>Checkboxes</title>' in response.data


@mock.patch('api_copiloto.main.Gerar_arquivo')
@mock.patch('api_copiloto.main.validate_cc_id')
@mock.patch('api_copiloto.main.hardwares_is_None')
@mock.patch('api_copiloto.main.validate_function')
@mock.patch('api_copiloto.main.validate_path')
@mock.patch('api_copiloto.main.Get_values')
def test_submit_route(mock_get_values,mock_validate_path,mock_validate_func,mock_hws,mock_validate_cc_id,mock_gerar_arquivo,client,data):
    mock_gerar_arquivo.return_value = [201,'Pull Request Ok']
    mock_validate_cc_id.return_value = False
    mock_hws.return_value = False
    mock_validate_func.return_value = False
    mock_get_values.return_value = ['teste','teste',1]
    mock_validate_path.return_value = False
    response = client.post('/submit', data=data)

    assert response.status_code == 200
    assert b'<title>Submit</title>' in response.data


@mock.patch('api_copiloto.main.hardwares_is_None')
def test_popup_route_hw_none_True(mock_hws,client):
    mock_hws.return_value = True
    response = client.post('/submit', data={})
    assert response.status_code == 200
    assert b'<title>Popup</title>' in response.data



@mock.patch('api_copiloto.main.validate_mifares')
@mock.patch('api_copiloto.main.hardwares_is_None')
def test_popup_route_valida_mifare_True(mock_hws,mock_mifare,client,data):
    mock_hws.return_value = False
    mock_mifare.return_value = True
    response = client.post('/submit', data=data)
    assert response.status_code == 200
    assert b'<title>Popup</title>' in response.data



@mock.patch('api_copiloto.main.validate_function')
@mock.patch('api_copiloto.main.validate_mifares')
@mock.patch('api_copiloto.main.hardwares_is_None')
def test_popup_route_validate_function_True(mock_hws,mock_mifare,mock_validate_func,client,data):
    mock_hws.return_value = False
    mock_mifare.return_value = False
    mock_validate_func.return_value = True
    response = client.post('/submit', data=data)
    assert response.status_code == 200
    assert b'<title>Popup</title>' in response.data

@mock.patch('api_copiloto.main.validate_hardwares')
@mock.patch('api_copiloto.main.validate_function')
@mock.patch('api_copiloto.main.validate_mifares')
@mock.patch('api_copiloto.main.hardwares_is_None')
def test_popup_route_validate_hardwares_True(mock_hws,mock_mifare,mock_validate_func,mock_validate_hws,client,data):
    mock_hws.return_value = False
    mock_mifare.return_value = False
    mock_validate_func.return_value = False
    mock_validate_hws.return_value = True
    response = client.post('/submit', data=data)
    assert response.status_code == 200
    assert b'<title>Popup</title>' in response.data


@mock.patch('api_copiloto.main.validate_checkboxes')
@mock.patch('api_copiloto.main.validate_hardwares')
@mock.patch('api_copiloto.main.validate_function')
@mock.patch('api_copiloto.main.validate_mifares')
@mock.patch('api_copiloto.main.hardwares_is_None')
def test_popup_route_validate_checkboxes_True(mock_hws,mock_mifare,mock_validate_func,mock_validate_hws,mock_validate_checkboxes,client,data):
    mock_hws.return_value = False
    mock_mifare.return_value = False
    mock_validate_func.return_value = False
    mock_validate_hws.return_value = False
    mock_validate_checkboxes.return_value = True
    response = client.post('/submit', data=data)
    assert response.status_code == 200
    assert b'<title>Popup</title>' in response.data


@mock.patch('api_copiloto.main.validate_path')
@mock.patch('api_copiloto.main.validate_checkboxes')
@mock.patch('api_copiloto.main.validate_hardwares')
@mock.patch('api_copiloto.main.validate_function')
@mock.patch('api_copiloto.main.validate_mifares')
@mock.patch('api_copiloto.main.hardwares_is_None')
def test_popup_route_validate_path_True(mock_hws,mock_mifare,mock_validate_func,mock_validate_hws,mock_validate_checkboxes,mock_validate_path,client,data):
    mock_hws.return_value = False
    mock_mifare.return_value = False
    mock_validate_func.return_value = False
    mock_validate_hws.return_value = False
    mock_validate_checkboxes.return_value = False
    mock_validate_path.return_value = True
    response = client.post('/submit', data=data)
    assert response.status_code == 200
    assert b'<title>Popup</title>' in response.data


@mock.patch('api_copiloto.main.validate_cc_id')
@mock.patch('api_copiloto.main.validate_path')
@mock.patch('api_copiloto.main.validate_checkboxes')
@mock.patch('api_copiloto.main.validate_hardwares')
@mock.patch('api_copiloto.main.validate_function')
@mock.patch('api_copiloto.main.validate_mifares')
@mock.patch('api_copiloto.main.hardwares_is_None')
def test_popup_route_validate_cc_id_True(mock_hws,mock_mifare,mock_validate_func,mock_validate_hws,mock_validate_checkboxes,mock_validate_path,mock_validate_cc_id,client,data):
    mock_hws.return_value = False
    mock_mifare.return_value = False
    mock_validate_func.return_value = False
    mock_validate_hws.return_value = False
    mock_validate_checkboxes.return_value = False
    mock_validate_path.return_value = False
    mock_validate_cc_id.return_value = True
    response = client.post('/submit', data=data)
    assert response.status_code == 200
    assert b'<title>Popup</title>' in response.data