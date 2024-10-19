import { SearchResponse } from '../types';

export const formatCSV = (searchResults: SearchResponse): string => {
    const headers = ['id', 'title', 'selftext', 'subreddit', 'score', 'num_comments', 'created_date', 'url'];
    return [
        headers.join(','),
        ...searchResults.results.map(post => {
            return [
                post.id,
                csvEscape(post.title),
                csvEscape(post.selftext),
                csvEscape(post.subreddit),
                post.score,
                post.num_comments,
                post.created_date,
                post.url
            ].map(value => csvEscape(value.toString())).join(',');
        })
    ].join('\n');
};

export const formatJSON = (searchResults: SearchResponse): string => {
    return JSON.stringify(searchResults, null, 2);
};

export const downloadFile = (content: string, type: string, filename: string) => {
    const blob = new Blob([content], { type: `${type};charset=utf-8;` });
    const link = document.createElement('a');
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
};

const csvEscape = (value: string): string => {
    if (value == null) return '""';
    value = value.replace(/"/g, '""');
    if (value.includes(',') || value.includes('"') || value.includes('\n')) {
        return `"${value}"`;
    }
    return value;
};