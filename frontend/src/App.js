// frontend/src/App.js

import React, { useEffect, useState } from "react";
import axios from "axios";
import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";

const COLORS = ["#00C49F", "#FF8042", "#8884d8"]; // Positive, Negative, Neutral

function App() {
  const [headlines, setHeadlines] = useState([]);
  const [summary, setSummary] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/headlines")
      .then(res => setHeadlines(res.data.data))
      .catch(err => console.error(err));

    axios.get("http://127.0.0.1:8000/summary")
      .then(res => {
        const chartData = Object.entries(res.data).map(([key, value]) => ({
          name: key,
          value,
        }));
        setSummary(chartData);
      })
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h1>📰 Real-Time News Sentiment</h1>

      <h2>Sentiment Summary</h2>
      <PieChart width={400} height={300}>
        <Pie
          data={summary}
          cx={200}
          cy={150}
          labelLine={false}
          outerRadius={100}
          fill="#8884d8"
          dataKey="value"
          label={({ name }) => name}
        >
          {summary.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>

      <h2>Latest Headlines</h2>
      <ul>
        {headlines.map((item, index) => (
          <li key={index}>
            <strong>[{item.sentiment}]</strong>{" "}
            <a href={item.url} target="_blank" rel="noreferrer">{item.title}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
