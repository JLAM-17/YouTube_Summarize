import React, { useState, useEffect } from 'react';
import VideoInput from './VideoInput';
import VideoInfo from './VideoInfo';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';


function App() {
  useEffect(() => {
    document.title = "YouTube Summarizer";
  }, []);

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route exact path="/" element={<VideoInput></VideoInput>} />
          <Route path="/video/:videoId" element={<VideoInfo></VideoInfo>} />
        </Routes>
      </div>
    </Router>
    );
}

export default App;
