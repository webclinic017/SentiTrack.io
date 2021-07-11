import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios'
import Plot from 'react-plotly.js';

function getPerformance(){
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
}

function Statistics() {
  getPerformance();
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
  const [data, setData] = useState({Time: [], Sentiment: [], Market: []});
  useEffect(() => {
    axios.get('http://127.0.0.1:5000/data').then(res => {
       setData(res.data)
    }).catch(err => console.log(err));
  }, [])
  var traces = [
    {x:data.Time, 
     y:data.Sentiment,
     yaxis: 'y1',
     line: {color: '#5E0DAC'},
     name: "Sentiment",
    }, 

    {x:data.Time, 
     y:data.Market,
     yaxis: 'y2',
     line: {color: '#FF4F00'},
     name: "S&P500",
    }
  ]
  return (
    <Plot
    data = {traces}
        layout = {{
          autosize: false,
          height: 724,
          width: 1000,
          xaxis: {
            autorange: true,
            tickfont: {color: 'white'},
            rangeslider: {},
            showgrid: false,
          },
          yaxis: {
            title: 'Sentiment', 
            side: 'left', 
            linecolor: 'white', 
            tickfont:{color:'white'}, 
            color: 'white', 
            autorange: true, 
            showgrid: false,
          },
          yaxis2: {
            title: 'S&P500 Price', 
            side: 'right', 
            overlaying: 'y', 
            tickfont:{color:'white'}, 
            color: 'white', 
            autorange: true,
            showgrid: false,
          },
          template: 'plotly_dark',
          paper_bgcolor:'rgba(0, 0, 0, 0)',
          plot_bgcolor:'rgba(0, 0, 0, 0)',
        }}
    />
  )
}

function App() {
  return (
    <section>
      <Statistics></Statistics>
      <div className="right-half">
        <div className='chart'>
          <Graph></Graph>
        </div>
      </div>
    </section>
  );
}

export default App;