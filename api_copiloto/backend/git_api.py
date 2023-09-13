from decouple import config,AutoConfig, Config, RepositoryEnv
import requests
import base64
import os

def Get_token():
    token = os.environ.get('TOKEN_GITHUB')
    if token == None:
        token = config('TOKEN_GITHUB')
    return token


def create_branch(new_branch):
    url = f'https://api.github.com/repos/CreareSistemas/iot-virtec-scripts/git/refs'
    headers = {
        # 'Authorization': f'Bearer {os.environ.get("TOKEN_GITHUB")}',
        'Authorization': f'Bearer {Get_token()}',
        'Content-Type': 'application/vnd.github+json'
    }
    data = {
        'ref': f'refs/heads/{new_branch}',
        'sha': get_commit_sha()[0]
    }
    
    response = requests.post(url, headers=headers, json=data)


def commit_file_to_github(file_path, branch_name, hw, cliente):
    create_branch(branch_name)
    file_name = f'{branch_name}_{hw[0]}.txt'
    with open(file_path, 'rb') as file:
        file_content = file.read()
    url = f'https://api.github.com/repos/CreareSistemas/iot-virtec-scripts/contents/Virtec/{hw[1]}/Cliente/{cliente}/{file_name}'
    headers = {
        # "Authorization": f'Bearer {os.environ.get("TOKEN_GITHUB")}',
        "Authorization": f'Bearer {Get_token()}',
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
    url = f'https://api.github.com/repos/CreareSistemas/iot-virtec-scripts/branches/main'
    headers = {
        # 'Authorization': f'Bearer {os.environ.get("TOKEN_GITHUB")}'
        'Authorization': f'Bearer {Get_token()}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commit_sha = response.json()['commit']['sha']
        return commit_sha,response.status_code
    return response

def create_pull_request(branch_name):
    url = f'https://api.github.com/repos/CreareSistemas/iot-virtec-scripts/pulls'
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        # 'Authorization': f'Bearer {os.environ.get("TOKEN_GITHUB")}'
        'Authorization': f'Bearer {Get_token()}'
    }
    data = {
        'title': branch_name,
        'body': 'Pull request automático',
        'head': branch_name,
        'base': 'main'
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        pull_request = response.json()
        return response.status_code,pull_request['html_url']
    else:
        return response.status_code,response.json()['errors'][0]['message']
