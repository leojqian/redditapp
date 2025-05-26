import React, { useEffect, useState, useRef } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./Loading.css";

export default function Loading() {
  const [progress, setProgress] = useState(0);
  const [jobId, setJobId] = useState(null);
  const [showSpinner, setShowSpinner] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const redditUrl = location.state?.redditUrl;

  const hasGenerated = useRef(false);
  const hasNavigated = useRef(false);

  // Start generation
  useEffect(() => {
    const generate = async () => {
      try {
        const res = await fetch("http://localhost:5000/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ reddit_url: redditUrl }),
        });
        const data = await res.json();
        setJobId(data.job_id);
      } catch (err) {
        console.error("Generation failed:", err);
      }
    };

    if (redditUrl && !hasGenerated.current) {
      hasGenerated.current = true;
      generate();
    }
  }, [redditUrl]);

  // Poll for completion & use fake progress
  useEffect(() => {
    if (!jobId) return;

    const interval = setInterval(async () => {
      try {
        console.log("Polling for status of job:", jobId);
        const res = await fetch(`http://localhost:5000/status/${jobId}`);
        const data = await res.json();
        console.log("Response from /status:", data);

        if (data.status === "done" && !hasNavigated.current) {
          hasNavigated.current = true;
          clearInterval(interval);
          setProgress(100);
          setTimeout(() => {
            navigate("/output", { state: { jobId } });
          }, 500);
        } else {
          setProgress((prev) => {
            const next = Math.min(prev + 5, 95);
            if (next === 95) setShowSpinner(true);
            return next;
          });
        }
      } catch (err) {
        console.error("Polling error:", err);
        clearInterval(interval);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [jobId, navigate]);

  return (
    <div className="loading-page">
      <div className="logo-placeholder">(logo — don’t have one yet)</div>
      <h1 className="app-title">REDDIT TO TIKTOK</h1>
      <p className="sub-title">(temp app name)</p>

      <div className="loading-bar-container">
        {progress < 95 ? (
          <>
            <p className="loading-text">LOADING... {progress}%</p>
            <div className="loading-bar">
              <div
                className="loading-bar-fill"
                style={{ width: `${progress}%` }}
              />
            </div>
          </>
        ) : (
          <>
            <p className="loading-text">FINALIZING...</p>
            <div className="spinner" />
          </>
        )}
      </div>
    </div>
  );
}
