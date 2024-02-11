import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';

function App() {

  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [history, setHistory] = useState([]);

  const handleKeyDown = async (event) => {
    if (event.keyCode === 13) {
      event.preventDefault(); // Prevents the default action to be triggered (Newline)
      // Add the current prompt to the history before making the API call
      // Note: At this point, we're not adding the response since we haven't received it yet
      setHistory([...history, { prompt, response: "Waiting for response..." }]);
      setPrompt(''); // Clear the prompt
      // Make an API call to send the prompt
      try {
        // Replace 'YOUR_API_ENDPOINT' with the actual endpoint URL
        // Feed prompt to the API
        const res = await axios.post('http://localhost:8888/api', { prompt }); // Assuming the API endpoint is /api
        // set response variable: res to be the API's response
        console.log(res.data); // Assuming the API returns the response in res.data
        setResponse(res.data); // Update the state with the API response
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
  }

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
          ></textarea>
          <div className="image-input-section">
            <label htmlFor="image-upload">Upload image:</label>
            <input type="file" id="image-upload" />
          </div>
          <div className="output-section">
            {/* Displaying the output response from the API */}
            <div className="output-prompt">{response || "Output will be displayed here."}</div>
            {/* Displaying the chat history of prompts with lower opacity*/}
            {history.map((item, index) => (
              <div key={index} style={{opacity: 0.5}}>
                <p><strong>Prompt:</strong> {item.prompt}</p>
                <p><strong>Response:</strong> {item.response}</p>
                </div>
                ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
