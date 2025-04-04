import google.generativeai as genai
import os
import requests

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def fetch_pr_changes(pr_id, platform, repo):
    """Fetch PR/MR code diffs based on the platform"""

    platform = platform.lower()

    if platform == "bitbucket":
        return fetch_bitbucket_changes(pr_id, repo)
    elif platform == "github":
        return fetch_github_changes(pr_id, repo)
    # elif platform == "gitlab":
    #     return fetch_gitlab_changes(pr_id, repo)

    return f"Unsupported platform: {platform}"


def fetch_bitbucket_changes(pr_id, repo):
    """Fetch PR diffs from Bitbucket"""
    api_url = f"https://api.bitbucket.org/2.0/repositories/{repo}/pullrequests/{pr_id}/diff"
    headers = {"Authorization": f"Bearer {os.getenv('BITBUCKET_API_TOKEN')}"}

    response = requests.get(api_url, headers=headers)
    return response.text if response.status_code == 200 else f"Failed to fetch Bitbucket PR changes: {response.text}"


def fetch_github_changes(pr_id, repo):
    """Fetch PR diffs from GitHub"""
    api_url = f"https://api.github.com/repos/{repo}/pulls/{pr_id}/files"
    headers = {"Authorization": f"Bearer {os.getenv('GITHUB_API_TOKEN')}"}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        files = response.json()
        return "\n".join([f"File: {file['filename']}\n{file['patch']}" for file in files if 'patch' in file])

    return f"Failed to fetch GitHub PR changes: {response.text}"

#
# def fetch_gitlab_changes(pr_id, repo):
#     """Fetch MR diffs from GitLab"""
#     api_url = f"https://gitlab.com/api/v4/projects/{repo}/merge_requests/{pr_id}/changes"
#     headers = {"Authorization": f"Bearer {os.getenv('GITLAB_API_TOKEN')}"}
#
#     response = requests.get(api_url, headers=headers)
#
#     if response.status_code == 200:
#         changes = response.json().get("changes", [])
#         return "\n".join([f"File: {change['new_path']}\n{change['diff']}" for change in changes])
#
#     return f"Failed to fetch GitLab MR changes: {response.text}"
#

def split_text(text, max_length=5000):
    """Splits text into smaller chunks for processing"""
    return [text[i : i + max_length] for i in range(0, len(text), max_length)]

def analyze_code_with_ai(pr_id, platform, repo):
    """Analyze PR/MR code changes using Gemini AI"""
    changed_code = fetch_pr_changes(pr_id, platform, repo)

    if "Failed to fetch" in changed_code or "Unsupported platform" in changed_code:
        return changed_code

    chunks = split_text(changed_code)  # Split large diffs
    responses = []

    for chunk in chunks:
        prompt = f"""
        Review the following code changes and suggest improvements:

        {chunk}

        Consider readability, performance, and security.
        """

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        if response and response.text:
            responses.append(response.text)

    return "\n".join(responses) if responses else "No response from AI"