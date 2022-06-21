import os
from time import sleep
from github import Github

def getConfig(config_name):
    return os.environ[config_name]
try:
    GH_TOKEN = getConfig("GH_TOKEN")
except Exception:
    print(f"Fill all the configs plox\nExiting...")
    exit(0)

g = Github(GH_TOKEN)

def get_all_repos():
    REPOS = []
    for repo in g.get_user().get_repos(type="owner"):
        REPOS.append(repo.full_name)
    return REPOS

def create_org_repo(org: str, name: str, is_private: bool = True):
    repo = g.get_organization(org).create_repo(name=name, private=is_private)
    return repo.full_name

def import_repo(to_repo: str, repo_name: str, username: str, password: str, vcs: str = "git"):
    repo = g.get_repo(to_repo)
    kang = repo.create_source_import(vcs=vcs, vcs_url=f"https://github.com/{repo_name}.git", vcs_username=username, vcs_password=password)
    return kang.html_url

if __name__ == "__main__":
    print("Starting Kang Process...\n\n")
    for user_repo in get_all_repos():
        try:
            print(f"Kanging Repo: {user_repo}\n")
            user_short_repo = user_repo.split("/")[1]
            org_repo = create_org_repo("PrajjuS-Stuffs", user_short_repo)
            print(f"Org Repo Created: {org_repo}\n")
            kang_repo = import_repo(org_repo, user_repo, GH_TOKEN, GH_TOKEN)
            print(f"Kang Successful: {kang_repo}\n")
            sleep(5)
            print("Sleeping for 5 secs...\n\n")
        except Exception as e:
            print(f"Errored: {e}")

