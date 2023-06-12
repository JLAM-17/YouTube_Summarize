import React, { useState } from 'react';


const VideoInput = () => {
  const [videoLink, setVideoLink] = useState('');
  const [captions, setCaptions] = useState([]);

  const handleInputChange = (event) => {
    setVideoLink(event.target.value);
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ videoLink }),
      });
      // console.log(response);
      if (response.ok) {
        const data = await response.json();
        console.log(data)
        setCaptions(data.captions);
        console.log(data.captions);
      } else {
        const errorData = await response.json();
        console.error(errorData.error);
      }
    } catch (error) {
      // Handle any errors
      console.error(error);
      
    } 
  };

  return (
    <div>
      <input
        type="text"
        value={videoLink}
        onChange={handleInputChange}
        placeholder="Enter YouTube video link"
      />
      <button onClick={handleSubmit}>Submit</button>

      {captions.length > 0 && (
        <div>
          <h2>Captions:</h2>
          <ul>
            {captions.map((caption, index) => (
              <li key={index}>{caption}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default VideoInput;
