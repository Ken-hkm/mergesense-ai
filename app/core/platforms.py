import requests
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def post_comment_github(repo, pr_id, feedback):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_id}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"body": feedback}

    response = requests.post(url, json=data, headers=headers)
    return response.json()

BITBUCKET_TOKEN = os.getenv("BITBUCKET_TOKEN")

def post_comment_bitbucket(repo, pr_id, feedback):
    url = f"https://api.bitbucket.org/2.0/repositories/{repo}/pullrequests/{pr_id}/comments"
    headers = {"Authorization": f"Bearer {BITBUCKET_TOKEN}"}
    data = {"content": {"raw": feedback}}

    response = requests.post(url, json=data, headers=headers)
    return response.json()