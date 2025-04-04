from fastapi import APIRouter, HTTPException
from app.core.ai import analyze_code_with_ai
from app.core.platforms import post_comment_github, post_comment_bitbucket

router = APIRouter()

@router.post("/analyze-pr")
async def analyze_pr(data: dict):
    platform = data.get("platform")
    repo = data.get("repo")
    pr_id = data.get("pr_id")

    if not platform or not repo or not pr_id:
        raise HTTPException(status_code=400, detail="Missing required parameters")

    # Run AI analysis on the PR code
    feedback = analyze_code_with_ai(pr_id, platform, repo)

    # Post comments to the respective platform
    if platform == "github":
        response = post_comment_github(repo, pr_id, feedback)
    elif platform == "bitbucket":
        response = post_comment_bitbucket(repo, pr_id, feedback)
    else:
        raise HTTPException(status_code=400, detail="Unsupported platform")

    return {"message": "PR reviewed successfully", "response": response}