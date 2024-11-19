import React, { useState } from 'react';
import './SearchComponent.css';
function SearchComponent({ onSearch }) {
    const [searchTerm, setSearchTerm] = useState('');
    const handleSubmit = (event) => {
        event.preventDefault();
        onSearch(searchTerm);
    };
    return (
        <div className="search-area">
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Enter Company Name"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
                <button type="submit">Search</button>
            </form>
        </div>
    );
}
export default SearchComponent;