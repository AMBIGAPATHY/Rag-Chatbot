// frontend/app/components/ChatBox.tsx
'use client';

import { useState } from 'react';
import axios from 'axios';
import './ChatBox.css';

const ChatBox = () => {
  const [url, setUrl] = useState('');
  const [query, setQuery] = useState('');
  const [chatResponse, setChatResponse] = useState('');
  const [scrapeMessage, setScrapeMessage] = useState('');

  const handleScrape = async () => {
    try {
      const res = await axios.post('http://127.0.0.1:8000/scrape/', { url });
      setScrapeMessage(res.data.message || res.data.error);
    } catch (error) {
      setScrapeMessage('Error scraping content.');
    }
  };

  const handleChat = async () => {
    try {
      const res = await axios.post('http://127.0.0.1:8000/chat/', { query });
      setChatResponse(res.data.answer);
    } catch (error) {
      setChatResponse('Error generating response.');
    }
  };

  return (
    <div className="chatBox">
      <div className="section">
        <h2>Scrape Content</h2>
        <input
          type="text"
          placeholder="Enter URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="input"
        />
        <button onClick={handleScrape} className="button">Scrape</button>
        {scrapeMessage && <p className="message">{scrapeMessage}</p>}
      </div>

      <div className="section">
        <h2>Chat</h2>
        <input
          type="text"
          placeholder="Ask a question"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="input"
        />
        <button onClick={handleChat} className="button">Ask</button>
        {chatResponse && <p className="response">{chatResponse}</p>}
      </div>
    </div>
  );
};

export default ChatBox;
