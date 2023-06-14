import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import 'purecss/build/pure.css';
import './VideoInfo.css';

const VideoInfo = () => {
  const { videoId } = useParams(); // Access the video ID from the URL
  const [videoData, setVideoData] = useState(null); // State variable to store the fetched video data

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/video/' + videoId, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          const data = await response.json();
          console.log(data.main_ideas.replace(/'/g, '"'));
          setVideoData(data);
        } else {
          const errorData = await response.json();
          console.error(errorData.error);
        }
      } catch (error) {
        // Handle any errors
        console.error(error);
      }
    };
    fetchData();
  }, [videoId]);

  return (
    <div className='pure-g'>
      <div className="card">
        {videoData && (
          <>
            <h1 className='title'>Video Summary</h1>
            <div className='top'>
              <div className="pure-u-1-2">
                <img src={videoData.cover} alt="Video Cover" className="cover-image" />
              </div>
              <div className="video-details pure-u-10-24">
                <h1>{videoData.title}</h1>
                <p><b>Channel: </b>{videoData.channel}</p>
                <p><b>Category:</b> {videoData.category}</p>
              </div>
            </div>
              <div className='pure-u-1-1 main-ideas'>
                <h2>Main Ideas</h2>
                {videoData.main_ideas.slice(1, -1).replaceAll('.,','..,').split('., ').map((item, index) => (
                  // <p key={index}>{Object.keys(item)[0] + ' ' + Object.values(item)[0]}</p>
                  <p key={index}>{item}</p>
                ))}
              </div>
              <div className='pure-u-1-1 summary'>
                <h2>Summary</h2>
                <p>{videoData.summary}</p>
              </div>
              <div className='pure-u-1-1 summary'>
                <h2>Sentiment analysis</h2>
                <p>{videoData.sentiment_analysis}</p>
              </div>
          </>
        )}
      </div>
    </div>
  );
};

export default VideoInfo;
