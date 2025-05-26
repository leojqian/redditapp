import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Input.css";

export default function Input() {
  const [url, setUrl] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim()) {
      navigate("/loading", { state: { redditUrl: url } });
    }
  };

  return (
    <div className="input-page">
      <div className="logo-placeholder">(logo — don’t have one yet)</div>
      <h1 className="app-title">REDDIT TO TIKTOK</h1>
      <p className="sub-title">(temp app name)</p>

      <form className="input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Upload link here…"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="link-input"
        />
        <button type="submit" className="submit-button">
          Go
        </button>
      </form>
    </div>
  );
}
