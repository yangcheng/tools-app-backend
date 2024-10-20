import React from 'react';
import { SearchResponse, RedditPost } from '../types';
import { formatCSV, formatJSON, downloadFile } from '../utils/downloadUtils';

interface SearchResultsProps {
    searchResults: SearchResponse;
}

const SearchResults: React.FC<SearchResultsProps> = ({ searchResults }) => {
    const handleDownloadCSV = () => {
        const csvContent = formatCSV(searchResults);
        const fileName = `reddit_search_results_${searchResults.query}.csv`;
        downloadFile(csvContent, 'text/csv', fileName);
    };

    const handleDownloadJSON = () => {
        const jsonContent = formatJSON(searchResults);
        const fileName = `reddit_search_results_${searchResults.query}.json`;
        downloadFile(jsonContent, 'application/json', fileName);
    };

    return (
        <div className="search-results">
            <h2>Search Results</h2>
            <p>Total results: {searchResults.total}</p>
            <div className="download-buttons">
                <button onClick={handleDownloadCSV}>Download as CSV</button>
                <button onClick={handleDownloadJSON}>Download as JSON</button>
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
