from decouple import config
import requests
import base64

def create_branch(new_branch):
    url = f'https://api.github.com/repos/CreareSistemas/virloc8-teste-de-esteira/git/refs'
    headers = {
        'Authorization': f'Bearer {config("BRIDA_TOKEN")}',
        'Content-Type': 'application/vnd.github+json'
    }
    data = {
        'ref': f'refs/heads/{new_branch}',
        'sha': get_commit_sha()[0]
    }
    response = requests.post(url, headers=headers, json=data)
    # print(response.content)
    print(response.status_code)
    if response.status_code == 201:
        print(f'Branch "{new_branch}" criada com sucesso!')
    else:
        print('Erro ao criar a branch:', response.text)

def commit_file_to_github(file_path, branch_name, hw, cliente):
    create_branch(branch_name)
    file_name = f'{branch_name}_{hw[0]}.txt'
    with open(file_path, 'rb') as file:
        file_content = file.read()
    url = f'https://api.github.com/repos/CreareSistemas/virloc8-teste-de-esteira/contents/Virtec/{hw[1]}/Cliente/{cliente}/{file_name}'
    headers = {
        "Authorization": f'Bearer {config("BRIDA_TOKEN")}',
        "Content-type": "application/vnd.github+json"
    }
    data = {
        "message": f"Gerador de script: {branch_name}",
        "content": base64.b64encode(file_content).decode("utf-8"),
        "branch": f'{branch_name}'
    }
    r = requests.put(url, headers=headers, json=data)
    return r.status_code


def get_commit_sha():
    url = f'https://api.github.com/repos/CreareSistemas/virloc8-teste-de-esteira/branches/main'
    headers = {
        'Authorization': f'Bearer {config("BRIDA_TOKEN")}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commit_sha = response.json()['commit']['sha']
        return commit_sha,response.status_code
    else:
        print('Erro ao obter o SHA do commit:', response.text)
    return None

def create_pull_request(branch_name):
    url = f'https://api.github.com/repos/CreareSistemas/virloc8-teste-de-esteira/pulls'
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'Bearer {config("BRIDA_TOKEN")}'
    }
    data = {
        'title': branch_name,
        'body': 'Pull request automático',
        'head': branch_name,
        'base': 'main'
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    if response.status_code == 201:
        pull_request = response.json()
        print('Pull request criado com sucesso!')
        print('URL do pull request:', pull_request['html_url'])
        return response.status_code,pull_request['html_url']
    else:
        print('Erro ao criar o pull request:', response.text)
        print(response.status_code,response.json()['errors'][0]['message'])
        return response.status_code,response.json()['errors'][0]['message']
