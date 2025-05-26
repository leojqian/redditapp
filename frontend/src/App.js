import React from 'react';
import './App.css';
import VideoCreator from './components/VideoCreator';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Reddit Story Video Creator</h1>
      </header>
      <main>
        <VideoCreator />
      </main>
    </div>
  );
}

export default App;
