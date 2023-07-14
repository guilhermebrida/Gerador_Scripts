from api_copiloto.git_api import get_commit_sha, create_branch, create_pull_request,commit_file_to_github
from unittest.mock import Mock, mock_open
from unittest import mock
import requests_mock
from decouple import config
import requests
import pytest



def test_get_sha_igual_200():
    sha = get_commit_sha()
    assert sha[1] == 200

def test_sha_deve_ser_valido():
    sha = get_commit_sha()
    assert len(sha[0]) == 40

def test_deve_retornar_201_ao_criar_nova_branch(monkeypatch):
    url = 'https://api.github.com/repos/CreareSistemas/virloc8-teste-de-esteira/git/refs'
    headers = {
        'Authorization': f'Bearer {config("BRIDA_TOKEN")}',
        'Content-Type': 'application/vnd.github+json'
    }
    data = {
        'ref': 'refs/heads/teste',
        'sha': get_commit_sha()[0]
    }
    expected_response = {'status_code': 201, 'json': {}, 'text': ''}
    class MockResponse:
        def __init__(self, status_code, json=None, text=''):
            self.status_code = status_code
            self.json_value = json
            self.text = text

    def mock_post(url, **kwargs):
        assert kwargs['headers'] == headers
        assert kwargs['json'] == data
        return MockResponse(expected_response['status_code'], expected_response['json'], expected_response['text'])

    monkeypatch.setattr(requests, 'post', mock_post)
    create_branch('teste')
    assert expected_response['status_code'] == 201


def test_deve_retornar_201_ao_criar_novo_commit(monkeypatch):
    url = 'https://api.github.com/repos/CreareSistemas/virloc8-teste-de-esteira/contents/Virtec/Virloc8/Cliente/teste/teste_VL8.txt'

    expected_response = {'status_code': 201, 'json': {}, 'text': ''}

    class MockResponse:
        def __init__(self, status_code, json=None, text=''):
            self.status_code = status_code
            self.json_value = json
            self.text = text

    def mock_post(url, **kwargs):
        assert kwargs['headers']['Authorization'] == f'Bearer {config("BRIDA_TOKEN")}'
        assert kwargs['headers']['Content-Type'] == 'application/vnd.github+json'
        return MockResponse(expected_response['status_code'], expected_response['json'], expected_response['text'])

    monkeypatch.setattr(requests, 'post', mock_post)
    with mock.patch('builtins.open', mock_open(read_data='arquivo de teste'.encode())):
        commit_file_to_github('downloads/teste.txt','teste','Virloc8','teste')
    assert expected_response['status_code'] == 201


def test_deve_retornar_201_ao_criar_novo_pull_request(monkeypatch):
    url = 'https://api.github.com/repos/CreareSistemas/virloc8-teste-de-esteira/pulls'
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'Bearer {config("BRIDA_TOKEN")}'
    }
    data = {
        'title': 'teste',
        'body': 'Pull request automático',
        'head': 'teste',
        'base': 'main'
    }
    expected_response = {'status_code': 201, 'json': {'html_url': 'https://github.com/...'}, 'text': ''}


    class MockResponse:
        def __init__(self, status_code, json=None, text=''):
            self.status_code = status_code
            self.json_value = json
            self.text = text

        def json(self):
            return self.json_value

    def mock_post(url, **kwargs):
        assert kwargs['headers'] == headers
        assert kwargs['json'] == data
        return MockResponse(expected_response['status_code'], expected_response['json'], expected_response['text'])

    monkeypatch.setattr(requests, 'post', mock_post)
    create_pull_request('teste')
    assert expected_response['status_code'] == 201


