import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { BASE_URL } from "./config/apiConfig";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Function to fetch and display logs
const fetchAndDisplayLogs = async () => {
  try {
    const response = await fetch(`${BASE_URL}/get-logs`);
    const data = await response.json();
    if (data.logs) {
      console.warn("Backend Logs:\n", data.logs);
    }
  } catch (error) {
    console.error("Failed to fetch logs:", error);
  }
};

setInterval(fetchAndDisplayLogs, 5000);
