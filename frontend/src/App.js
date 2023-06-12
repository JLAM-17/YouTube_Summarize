import React, { useState, useEffect } from 'react';
import VideoInput from './VideoInput';

function App() {
  const [message, setMessage] = useState('');

  // useEffect(() => {
  //   fetch('/api')
  //     .then(response => response.json())
  //     .then(data => setMessage(data.message));
  // }, []);

  return (
    <div className="App">
      <h1>Welcome to My Video Summarizer</h1>
      <VideoInput />
    </div>
  );
}

export default App;
