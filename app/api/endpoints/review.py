from fastapi import APIRouter, HTTPException, Request
from app.core.ai import analyze_code_with_ai
from app.core.platforms import post_comment_github, post_comment_bitbucket

router = APIRouter()

@router.post("/analyze-pr")
async def analyze_pr(request: Request):
    data = await request.json()
    platform = data.get("platform")
    repo = data.get("repo")
    pr_id = data.get("pr_id")

    if not platform or not repo or not pr_id:
        raise HTTPException(status_code=400, detail="Missing required parameters")
    headers = {
        "Authorization": request.headers.get("Authorization"),
        "Content-Type": "application/json"  # Ensure content type is passed
    }
    # Run AI analysis on the PR code
    feedback = analyze_code_with_ai(pr_id, platform, repo, headers)

    print(feedback)
    # Post comments to the respective platform
    if platform == "github":
        response = post_comment_github(repo, pr_id, feedback,headers)
    elif platform == "bitbucket":
        response = post_comment_bitbucket(repo, pr_id, feedback,headers)
    else:
        raise HTTPException(status_code=400, detail="Unsupported platform")

    return {"message": "PR reviewed successfully", "response": response}