import React from 'react';
import { SearchResponse, RedditPost } from '../types';

interface SearchResultsProps {
    searchResults: SearchResponse;
    onDownloadCSV: () => void;
    onDownloadJSON: () => void;
}

const SearchResults: React.FC<SearchResultsProps> = ({ searchResults, onDownloadCSV, onDownloadJSON }) => {
    return (
        <div className="search-results">
            <h2>Search Results</h2>
            <p>Total results: {searchResults.total}</p>
            <div className="download-buttons">
                <button onClick={onDownloadCSV}>Download as CSV</button>
                <button onClick={onDownloadJSON}>Download as JSON</button>
            </div>
            <ul>
                {searchResults.results.map((post: RedditPost) => (
                    <li key={post.id}>
                        <h3><a href={post.url} target="_blank" rel="noopener noreferrer">{post.title}</a></h3>
                        <p>Subreddit: r/{post.subreddit}</p>
                        <p>Score: {post.score} | Comments: {post.num_comments}</p>
                        <p>Created: {post.created_date}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default SearchResults;