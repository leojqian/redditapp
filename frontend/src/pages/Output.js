import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./Output.css";

function Output() {
  const navigate = useNavigate();
  const location = useLocation();
  const jobId = location.state?.jobId;

  return (
    <div className="output-page">
      <div className="logo-placeholder">(logo — don’t have one yet)</div>
      <h1 className="app-title">REDDIT TO TIKTOK</h1>
      <p className="sub-title">(temp app name)</p>

      <div className="button-row">
        <a
          href={`http://localhost:5000/video/${jobId}`}
          download="output.mp4"
          className="action-button"
        >
          ⬇ Download Video
        </a>
        <button className="action-button" onClick={() => navigate("/")}>
          Try Another Link
        </button>
      </div>

      <div className="video-center">
        <video controls height="500">
          <source
            src={`http://localhost:5000/video/${jobId}`}
            type="video/mp4"
          />
          Your browser does not support the video tag.
        </video>
      </div>
    </div>
  );
}

export default Output;
