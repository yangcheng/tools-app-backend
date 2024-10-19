import React, { useState } from 'react';

interface SearchBoxProps {
    onSearch: (keyword: string) => Promise<void>;
}

const SearchBox: React.FC<SearchBoxProps> = ({ onSearch }) => {
    const [searchKeyword, setSearchKeyword] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSearch = async () => {
        setIsLoading(true);
        await onSearch(searchKeyword);
        setIsLoading(false);
    };

    return (
        <div className="search-box">
            <input
                type="text"
                placeholder="Search..."
                value={searchKeyword}
                onChange={(e) => setSearchKeyword(e.target.value)}
            />
            <button onClick={handleSearch} disabled={isLoading}>
                {isLoading ? 'Searching...' : 'Search'}
            </button>
        </div>
    );
};

export default SearchBox;