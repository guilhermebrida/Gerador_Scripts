import json
import requests
from datetime import datetime
from decouple import config

def gh_sesh(user, token):
    s = requests.Session()
    s.auth = (user, token)
    s.headers ={ 
        "Content-type": "application/vnd.github+json"
    }
    return s

class GH_Response_Obj:
    def __init__(self, json_all, next_page):
        self.json_all = json_all
        self.next_page = next_page

def gh_get_request(gh_user, gh_token, url):
    s = gh_sesh(gh_user, gh_token)
    response = s.get(url)
    response_status = response.status_code
    if response_status > 200:
        print(f'\n This was the response code: {response_status}')
        exit()

    json = response.json()
    links = response.links

    try:
        next_page = links['next']['url']
    except:
        next_page = None

    full = GH_Response_Obj(json, next_page)

    return full

def gh_post_request(gh_user, gh_token, url, data):
    s = gh_sesh(gh_user, gh_token)
    response = s.post(url, data)
    response_status = response.status_code
    if response_status > 201:
        print(f'\n This was the response code: {response_status}')
        exit()

    json = response.json()

    return json 

def get_branch_sha(gh_user, gh_token, branch_name="teste"):
	url = f'https://api.github.com/repos/CreareSistemas/virloc8-teste-de-esteira/branches/{branch_name}'
	response =gh_get_request(gh_user, gh_token, url)
	sha = response.json_all['commit']['sha']
	return sha

def create_new_branch(gh_user, gh_token, master_branch_sha):
	now = str(datetime.now()).replace(' ', '__').replace(':', '-').replace('.', '')
	new_sync_branch = f'new_branch_{now}'
	url = f"https://api.github.com/repos/CreareSistemas/virloc8-teste-de-esteira/git/refs"

	data = {
		"ref": f'refs/heads/{new_sync_branch}',
		"sha": master_branch_sha
	}

	data = json.dumps(data)

	response =gh_post_request(gh_user, gh_token, url, data)

	return response

def main():
    gh_user = config("BRIDA_USER")
    gh_token = config("BRIDA_TOKEN")
    sha = get_branch_sha(gh_user, gh_token)
    print(sha)
    new_sync_branch = create_new_branch(gh_user, gh_token, sha)
    print(new_sync_branch)

if __name__ == '__main__':
	main()