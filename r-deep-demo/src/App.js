import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');

  const handleKeyDown = (event) => {
    if (event.keyCode === 13) {
      event.preventDefault(); // Prevents the default action to be triggered (Newline)
      console.log(prompt); // Replace this with your function
      // Clear the prompt
      setPrompt('');
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
            <div className="output-prompt">
              {/* Future chatbot integration
              import { chatbotResponse } from './backdemo';
              const response = chatbotResponse(prompt);
              {response}
              */}
              Great news! I found 5 flights from Houston to Dallas!
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
