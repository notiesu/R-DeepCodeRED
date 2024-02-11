import React, { useState, useEffect, useRef } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';
// Import the SVG file as a component
import { ReactComponent as YourSvg } from './imagebf.svg';

function App() {

  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [history, setHistory] = useState([]);

  // Ref for the chat history container to manage scroll
  const chatHistoryRef = useRef(null);

  // Effect to scroll to the latest message
  useEffect(() => {
    if (chatHistoryRef.current) {
      const { scrollHeight, clientHeight } = chatHistoryRef.current;
      chatHistoryRef.current.scrollTo({ top: scrollHeight - clientHeight, behavior: 'smooth' });
    }
  }, [history]);

  const handleKeyDown = async (event) => {
    if (event.keyCode === 13) {
      event.preventDefault(); // Prevents the default action to be triggered (Newline)
      // Add the current prompt to the history before making the API call
      // Note: At this point, we're not adding the response since we haven't received it yet (default is "Waiting for response...")
      const newEntry = { prompt, response: "Waiting for response..." };
      setHistory(history => [...history, newEntry]); // Append new entry to maintain chronological order
      setPrompt('');
      // Make an API call to send the prompt
      try {
        // Replace 'YOUR_API_ENDPOINT' with the actual endpoint URL
        // Feed prompt to the API
        const res = await axios.post('http://localhost:8888/api', { prompt }); // Assuming the API endpoint is /api
        // set response variable: res to be the API's response
        console.log(res.data); // Assuming the API returns the response in res.data
        setResponse(res.data); // Update the state with the API response
        setHistory(currentHistory => [...currentHistory.slice(0, -1), { prompt, response: res.data }]);
      } catch (error) {
        console.error("Error fetching response:", error);
        setResponse("Failed to get response.");
      }
      // Clear the prompt
      // setPrompt('');
    }
  }

  const handlePromptChange = (event) => {
    setPrompt(event.target.value);
  };

  return (
    <div className="App">
      <header className="App-header">
        {/* Adjusted for R&Deep Demo text and background */}
        <div className="App-logo-text">R&Deep Demo</div>
      </header>
      <main className="App-main">
        <section className="prompt-section">
          <h2>Please type the prompt below:</h2>
          <textarea 
            className="prompt-input" 
            placeholder="Type here..."
            value={prompt}
            onChange={handlePromptChange}
            onKeyDown={handleKeyDown}
          />{/* Chat history container with auto-scroll */}
          <div className="chat-history" ref={chatHistoryRef} style={{ maxHeight: '200px', overflowY: 'auto', margin: '20px 0' }}>
            {history.map((item, index) => (
              <div key={index}>
                <p><strong>Prompt:</strong> {item.prompt}</p>
                <p><strong>Response:</strong> {item.response}</p>
              </div>
            ))}
            </div>
          {/* Wrapper for SVG for better control */}
          <div className="svg-wrapper" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <YourSvg style={{ width: '100px', height: '100px', margin: '20px auto' }} />
          </div>
          <div className="output-section">
            {/* Displaying the output response from the API */}
            <div className="output-prompt">{response || "Output will be displayed here."}</div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
