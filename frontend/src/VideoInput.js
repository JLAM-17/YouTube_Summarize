import React, { useState } from 'react';
import './VideoInput.css';
import { useNavigate } from 'react-router';
import { DotWave } from '@uiball/loaders'

const VideoInput = () => {
  const [videoLink, setVideoLink] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const navigate = useNavigate();

  const handleInputChange = (event) => {
    setVideoLink(event.target.value);
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('api/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ videoLink }),
      });
      // console.log(response);
      if (response.ok) {
        const data = await response.json();
        console.log(data.video_id)
        const videoId = data.video_id;
        navigate(`/video/${videoId}`);
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.error);
      }
    } catch (error) {
      setErrorMessage(error.message);   
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>      
      <div className="video-input-container">
      <h1><span className='gradient-text'>Summarize</span> YouTube videos <br></br> with <span className='gradient-text'>AI</span></h1>
        <div className="input-group">
          <input
            type="text"
            value={videoLink}
            onChange={handleInputChange}
            placeholder="Enter YouTube video link"
            className="video-input"
          />
          <button onClick={handleSubmit} className='submit-button'>Submit</button>
        </div>
        {/* Loader animation*/}
        {isLoading && <DotWave size={80} speed={1} color="#f50a41" />}
        {/* Error message popup */}
        {errorMessage && (
        <div className="error-popup box">
          <p>{errorMessage}</p>
          <button onClick={() => setErrorMessage(null)}>Close</button>
        </div>
      )}        
      </div>
    </div>
  );
};

export default VideoInput;
