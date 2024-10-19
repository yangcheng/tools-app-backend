from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import praw
from app.core.config import settings
from datetime import datetime



router = APIRouter()

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id=settings.REDDIT_CLIENT_ID,
    client_secret=settings.REDDIT_CLIENT_SECRET,
    user_agent=settings.REDDIT_USER_AGENT,
)

class RedditPost(BaseModel):
    id: str
    title: str
    selftext: str
    subreddit: str
    score: int
    num_comments: int
    created_utc: float
    created_date: str
    url: str


class SearchResponse(BaseModel):
    results: List[RedditPost]
    total: int
    has_more: bool

@router.get("/search", response_model=SearchResponse)
async def search_reddit(
    keyword: str = Query(..., description="Keyword to search for on Reddit"),
    limit: Optional[int] = Query(10, description="Maximum number of results to return", ge=1, le=100)
):
    try:
        search_results = []
        for submission in reddit.subreddit("all").search(keyword, limit=limit):
            post = RedditPost(
                id=submission.id,
                title=submission.title,
                selftext=submission.selftext,
                subreddit=submission.subreddit.display_name,
                score=submission.score,
                num_comments=submission.num_comments,
                created_utc=submission.created_utc,
                created_date=datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                url=f"https://www.reddit.com{submission.permalink}"
            )
            search_results.append(post)
        
        response = SearchResponse(
            results=search_results,
            total=len(search_results),
            has_more=False  # For now, we're not implementing pagination
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while searching Reddit: {str(e)}")
