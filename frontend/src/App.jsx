import { useState, useEffect } from "react"; // Imports React hooks for managing data
import axios from "axios"; // Imports Axios to talk to your FastAPI backend

function App() {

  // State variables to hold our form data and API responses
  const [userId] = useState("123"); // Hardcoded user ID for this prototype
  const [ambience, setAmbience] = useState("forest");
  const [text, setText] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [entries, setEntries] = useState([]);
  const [insights, setInsights] = useState(null);

  // This URL points exactly to your running FastAPI backend
  const API_URL = "http://127.0.0.1:8000/api/journal";

  // Automatically load past entries and insights when the page opens
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {

      const entriesRes = await axios.get(`${API_URL}/${userId}`);
      setEntries(entriesRes.data);

      const insightsRes = await axios.get(`${API_URL}/insights/${userId}`);
      setInsights(insightsRes.data);

    } catch (error) {
      console.error("Error loading data", error);
    }
  };

  // Triggers the Gemini LLM analysis route
  const handleAnalyze = async () => {

    if (!text) return alert("Please write something first!");

    try {

      const res = await axios.post(`${API_URL}/analyze`, { text });
      setAnalysis(res.data);

    } catch (error) {

      console.error(error);
      alert("Analysis failed! Make sure your backend server is running.");

    }
  };

  // Saves the completed journal entry to MongoDB
  const handleSave = async () => {

    if (!text) return alert("Please write something first!");

    try {

      let payload = { userId, ambience, text };

      // If the user already clicked analyze, attach the AI data
      if (analysis) {
        payload.emotion = analysis.emotion;
        payload.keywords = analysis.keywords;
        payload.summary = analysis.summary;
      }

      await axios.post(API_URL, payload);

      // Clear fields and reload data
      setText("");
      setAnalysis(null);
      loadData();

    } catch (error) {

      console.error(error);
      alert("Save failed!");

    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif", maxWidth: "800px", margin: "auto" }}>

      <h1>ArvyaX Wellness Journal</h1>

      {/* Section 1: Writing and Analyzing */}
      <div style={{ border: "1px solid black", padding: "15px", marginBottom: "20px" }}>

        <h2>1. New Session</h2>

        <select
          value={ambience}
          onChange={(e) => setAmbience(e.target.value)}
          style={{ marginBottom: "10px" }}
        >
          <option value="forest">Forest</option>
          <option value="ocean">Ocean</option>
          <option value="mountain">Mountain</option>
        </select>

        <br />

        <textarea
          rows="4"
          style={{ width: "100%" }}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="How did you feel during this session?"
        />

        <br /><br />

        <button onClick={handleAnalyze}>Analyze with AI</button>

        <button
          onClick={handleSave}
          style={{ marginLeft: "10px", backgroundColor: "#4CAF50", color: "white" }}
        >
          Save Entry
        </button>

        {/* Analysis Result */}
        {analysis && (
          <div style={{ backgroundColor: "#e9ecef", padding: "10px", marginTop: "15px", borderRadius: "5px" }}>
            <p><strong>Emotion:</strong> {analysis.emotion}</p>
            <p><strong>Summary:</strong> {analysis.summary}</p>
            <p><strong>Keywords:</strong> {analysis.keywords?.join(", ")}</p>
          </div>
        )}

      </div>

      {/* Section 2: Insights Dashboard */}
      <div style={{ border: "1px solid black", padding: "15px", marginBottom: "20px" }}>

        <h2>2. Your Mental Insights</h2>

        {insights ? (
          <ul>
            <li><strong>Total Sessions:</strong> {insights.totalEntries}</li>
            <li><strong>Top Emotion:</strong> {insights.topEmotion}</li>
            <li><strong>Favorite Ambience:</strong> {insights.mostUsedAmbience}</li>
            <li><strong>Recent Focus:</strong> {insights.recentKeywords?.join(", ")}</li>
          </ul>
        ) : (
          <p>Loading insights...</p>
        )}

      </div>

      {/* Section 3: Past Entries */}
      <div style={{ border: "1px solid black", padding: "15px" }}>

        <h2>3. Past Entries</h2>

        {entries.slice().reverse().map((entry, idx) => (

          <div
            key={idx}
            style={{ borderBottom: "1px solid #ccc", paddingBottom: "10px", marginBottom: "10px" }}
          >

            <p>
              <strong>{entry.ambience.toUpperCase()}</strong> |
              <em> Emotion: {entry.emotion || "None"}</em>
            </p>

            <p>{entry.text}</p>

          </div>

        ))}

      </div>

    </div>
  );
}

export default App;