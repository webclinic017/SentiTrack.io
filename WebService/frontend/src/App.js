import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios'
import Plot from 'react-plotly.js';

function Statistics() {
    axios.get('http://127.0.0.1:5000/performance').then(response => {
      document.getElementById("returns").innerHTML = response.data['returns'] + "%";
      document.getElementById("accuracy").innerHTML = response.data['accuracy'] + "%";
    }).catch(error => {
      console.log(error)
    })
    
    axios.get('http://127.0.0.1:5000/mentions').then(response => {
      document.getElementById("tick1").innerHTML = response.data['Ticker1'];
      document.getElementById("tick2").innerHTML = response.data['Ticker2'];
      document.getElementById("tick3").innerHTML = response.data['Ticker3'];
      document.getElementById("tick4").innerHTML = response.data['Ticker4'];
      document.getElementById("tick5").innerHTML = response.data['Ticker5'];
    }).catch(error => {
      console.log(error)
    })
  return (
    <div className="left-half">
      <h1>SentiTrack.io</h1>
      <h2 id = "returns">0</h2>
      <h5>Historical Performance</h5>
      <h2 id = "accuracy">0</h2>
      <h5>Accuracy</h5>
      <h2 id = "tick1">""</h2>
      <h2 id = "tick2">""</h2>
      <h2 id = "tick3">""</h2>
      <h2 id = "tick4">""</h2>
      <h2 id = "tick5">""</h2>
      <h5>Top Retail Mentions</h5>
    </div>
  )
}

function Graph() {
  return (
    <Plot
        data={[
          {
            x: [1, 2, 3],
            y: [2, 6, 3],
            type: 'scatter',
            mode: 'lines',
            name: 'sentiment',
            line: {color: '#17BECF'}
          },
        ]}
        layout = {{
          xaxis: {
            autorange : true
          },
          paper_bgcolor: "rgb(50, 50, 50)",
          plot_bgcolor: "rgb(50, 50, 50)",
        }}
      />
  )
}

function App() {
  return (
    <section>
      <Statistics></Statistics>
      <div className="right-half">
        <div id='chart'>
          <Graph></Graph>
        </div>
      </div>
    </section>
  );
}

export default App;