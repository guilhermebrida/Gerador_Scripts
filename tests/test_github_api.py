from api_copiloto.git_api import get_commit_sha, create_branch,create_pull_request

def test_get_sha_igual_200():
    sha = get_commit_sha()
    assert sha[1] == 200

def test_sha_deve_ser_valido():
    sha = get_commit_sha()
    assert len(sha[0]) == 40

def test_deve_retornar_201_ao_criar_nova_branch():
    assert create_branch('teste') == 201

def test_deve_retornar_201_ao_criar_um_pull_request(mocker):
    mocker.patch('requests.post')
    assert create_pull_request('teste') == 201


def test_deve_retornar_201_ao_criar_um_pull_request(mocker):
    mocker.patch('requests.post')  # Mock da função requests.post
    response_mock = mocker.Mock()
    response_mock.status_code = 201
    requests_post_mock = mocker.patch('requests.post', return_value=response_mock)
    create_pull_request('teste')
    # requests_post_mock.assert_called_once_with(expected_url, headers=expected_headers, json=expected_data)