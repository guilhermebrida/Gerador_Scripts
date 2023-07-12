from api_copiloto.main import get_commit_sha, create_branch

def test_get_sha_igual_200():
    sha = get_commit_sha()
    assert sha[1] == 200

def test_sha_deve_ser_valido():
    sha = get_commit_sha()
    assert len(sha[0]) == 40

def test_deve_retornar_201_ao_criar_nova_branch():
    assert create_branch('teste') == 201