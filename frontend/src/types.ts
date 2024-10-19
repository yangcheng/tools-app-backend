export interface User {
    email: string;
}

export interface RedditPost {
    id: string;
    title: string;
    selftext: string;
    subreddit: string;
    score: number;
    num_comments: number;
    created_utc: number;
    created_date: string;
    url: string;
}

export interface SearchResponse {
    results: RedditPost[];
    total: number;
    has_more: boolean;
    query: string;
}
