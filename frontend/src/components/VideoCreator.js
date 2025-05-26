import React, { useState } from 'react';
import axios from 'axios';

const VideoCreator = () => {
    const [redditUrl, setRedditUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [videoPath, setVideoPath] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const response = await axios.post('http://localhost:5000/api/create-video', {
                redditUrl: redditUrl
            });

            setVideoPath(response.data.videoPath);
        } catch (err) {
            setError(err.response?.data?.error || 'An error occurred while creating the video');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="video-creator">
            <h2>Create Reddit Story Video</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="redditUrl">Reddit Post URL:</label>
                    <input
                        type="text"
                        id="redditUrl"
                        value={redditUrl}
                        onChange={(e) => setRedditUrl(e.target.value)}
                        placeholder="https://www.reddit.com/r/..."
                        required
                    />
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? 'Creating Video...' : 'Create Video'}
                </button>
            </form>

            {error && <div className="error">{error}</div>}

            {videoPath && (
                <div className="video-preview">
                    <h3>Your Video is Ready!</h3>
                    <video controls width="100%">
                        <source src={`http://localhost:5000/${videoPath}`} type="video/mp4" />
                        Your browser does not support the video tag.
                    </video>
                </div>
            )}
        </div>
    );
};

export default VideoCreator; 