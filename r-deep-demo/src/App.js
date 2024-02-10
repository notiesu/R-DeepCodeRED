import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/* Adjusted for R&Deep Demo text and background */}
        <div className="App-logo-text">R&Deep Demo</div>
      </header>
      <main className="App-main">
        <section className="prompt-section">
          <h2>Please type the prompt below:</h2>
          <textarea className="prompt-input" placeholder="Type here..."></textarea>
          <div className="image-input-section">
            <label htmlFor="image-upload">Upload image:</label>
            <input type="file" id="image-upload" />
          </div>
          <div className="output-section">
            <div className="output-prompt">Output will be displayed here.</div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
