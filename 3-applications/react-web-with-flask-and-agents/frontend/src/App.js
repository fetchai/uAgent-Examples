// Import necessary React libraries and components
import React, { useState } from 'react';
import SearchComponent from './components/SearchComponent';
import NewsFeed from './components/NewsFeed';
import './App.css';  // Import CSS for styling
// Define the main React functional component
function App() {
  // State hooks to manage news data, sentiment, and type of sentiment
  const [news, setNews] = useState([]);
  const [sentiment, setSentiment] = useState('');
  const [sentimentType, setSentimentType] = useState('');
  // Function to handle search operations
  const handleSearch = async (searchTerm) => {
    try {
      // API request to fetch news based on a search term
      const newsResponse = await fetch(`http://127.0.0.1:5000/api/news/${searchTerm}`);
      const newsData = await newsResponse.json();  // Convert response to JSON
      setNews(newsData);  // Update the news state
      console.log('Fetched news:', newsData);  // Log the fetched news data
      // API request to fetch sentiment analysis for the search term
      const sentimentResponse = await fetch(`http://127.0.0.1:5000/api/sentiment/${searchTerm}`);
      const sentimentData = await sentimentResponse.text();  // Get response as text
      console.log('Fetched sentiment:', sentimentData);  // Log the fetched sentiment
      processSentiment(sentimentData);  // Process the fetched sentiment text
    } catch (error) {
      console.error('Failed to fetch data:', error);  // Log any errors
      setNews([]);  // Reset news state on error
      setSentiment('');  // Reset sentiment state on error
      setSentimentType('');  // Reset sentiment type state on error
    }
  };
  // Helper function to process the sentiment text and update state
  const processSentiment = (sentimentText) => {
    const parts = sentimentText.split(':');  // Split sentiment text by colon
    const sentimentValue = parts[0].trim().toLowerCase();  // Extract sentiment label and normalize it
    setSentiment(sentimentText);  // Update sentiment state
    setSentimentType(sentimentValue);  // Update sentiment type state
  };

  return (
    <div className="App">
      <SearchComponent onSearch={handleSearch} />
      <NewsFeed news={news} />
      {sentiment && <div className={`sentiment-block ${sentimentType}`}>{sentiment}</div>}
    </div>
  );
}
export default App;