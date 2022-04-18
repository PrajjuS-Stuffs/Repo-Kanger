import os
import requests
import time

def getConfig(config_name):
    return os.environ[config_name]
try:
    GH_TOKEN = getConfig("GH_TOKEN")
    GH_USER = getConfig("GH_USER")
    GH_ORG = getConfig("GH_ORG")
except Exception:
    print(f"Fill all the configs plox\nExiting...")
    exit(0)

def list_repos():
    REPOS = []
    url = f"https://api.github.com/user/repos"
    params = {
        "per_page": "1000",
        "type": "owner"
    }
    headers = {"Authorization": f"token {GH_TOKEN}"}
    re = requests.get(url=url, params=params, headers=headers)
    json = re.json()
    if re.status_code != 200:
        print(f"Requrests Errored!\nStatus Code: {re.status_code}")
        print(json)
        return
    for url in json:
        REPOS.append(url['html_url'])
    return REPOS

def get_repo_names():
    NAMES = []
    all_repos = list_repos()
    for repo in all_repos:
        NAMES.append(repo.split('/')[4])
    return NAMES

def create_repo(name, private: bool):
    url = f"https://api.github.com/orgs/{GH_ORG}/repos"
    data = {
        "name": name,
        "private": private
    }
    headers = {"Authorization": f"token {GH_TOKEN}"}
    re = requests.post(url=url, json=data, headers=headers)
    json = re.json()
    if re.status_code != 201:
        print(f"Repository creating failed!\nStatus code: {re.status_code}")
        print(json)
    print(f"Repository {name} created!")

def clone_create_push():
    repo_names = get_repo_names()
    for repo in repo_names:
        try:
            os.system(f"git clone https://{GH_USER}/{repo}.git")
            os.system(f"cd {repo}")
            create_repo(f"{repo}", True)
            os.system(f"git remote add new-origin https://{GH_ORG}/{repo}.git")
            os.system("git push new-origin --mirror")
            os.system("git push new-origin refs/remotes/origin/*:refs/heads/*")
            os.system("git push new-origin --delete HEAD")
            print(f"Repository {repo} kanged!")
            os.system("cd ..")
            os.system(f"rm -rf {repo}")
            time.sleep(5)
        except Exception:
            print(f"{repo} failed!")

clone_create_push()
