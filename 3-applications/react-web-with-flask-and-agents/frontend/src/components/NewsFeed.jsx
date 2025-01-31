import React from 'react';
function NewsFeed({ news }) {
    return (
        <div className="news-feed">
            <h2>News Titles</h2>
            {news.length > 0 ? (
                <ul>
                    {news.map((item, index) => (
                        <li key={index}>
                            <a href={item.url} target="_blank" rel="noopener noreferrer">{item.title}</a>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No news found.</p>
            )}
        </div>
    );
}
export default NewsFeed;