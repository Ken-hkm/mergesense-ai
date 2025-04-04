import requests

def post_comment_github(repo, pr_id, feedback, headers):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_id}/comments"
    data = {"body": feedback}

    response = requests.post(url, json=data, headers=headers)
    return response.json()

def post_comment_bitbucket(repo, pr_id, feedback, headers):
    url = f"https://api.bitbucket.org/2.0/repositories/{repo}/pullrequests/{pr_id}/comments"
    data = {"content": {"raw": feedback}}

    response = requests.post(url, json=data, headers=headers)
    return response.json()