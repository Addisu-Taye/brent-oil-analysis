import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_CONFIG } from './config';
import './App.css';
import Navbar from './components/Navbar';
import MainChart from './components/MainChart';
import Indicators from './components/Indicators';
import ChangePoints from './components/ChangePoints';
import EventsTimeline from './components/EventsTimeline';

function App() {
  const [state, setState] = useState({
    priceData: [],
    events: [],
    changePoints: [],
    indicators: null,
    loading: true,
    error: null
  });

  useEffect(() => {
    const controller = new AbortController();
    const { signal } = controller;

    const fetchData = async () => {
      try {
        console.log('Starting data fetch...');
        
        const endpoints = [
          axios.get(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.PRICES}`, { signal }),
          axios.get(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.EVENTS}`, { signal }),
          axios.get(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.CHANGE_POINTS}`, { signal }),
          axios.get(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.INDICATORS}`, { signal })
        ];

        const responses = await Promise.all(endpoints);
        
        console.log('API responses:', responses);

        setState({
          priceData: responses[0].data,
          events: responses[1].data,
          changePoints: responses[2].data,
          indicators: responses[3].data,
          loading: false,
          error: null
        });
        
      } catch (err) {
        if (axios.isCancel(err)) {
          console.log('Request canceled:', err.message);
        } else {
          console.error('Fetch error:', {
            error: err,
            message: err.message,
            response: err.response?.data
          });
          setState(prev => ({
            ...prev,
            loading: false,
            error: err.response?.data?.message || err.message
          }));
        }
      }
    };

    fetchData();

    return () => controller.abort();
  }, []);

  if (state.loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p className="loading-text">Loading dashboard data...</p>
        <div className="loading-debug">
          <p>Debug info:</p>
          <ul>
            <li>Backend: {API_CONFIG.BASE_URL}</li>
            <li>Check browser's Network tab</li>
          </ul>
        </div>
      </div>
    );
  }

  if (state.error) {
    return (
      <div className="error-container">
        <h2>⚠️ Application Error</h2>
        <div className="error-message">{state.error}</div>
        <div className="troubleshooting">
          <h3>Troubleshooting Steps:</h3>
          <ol>
            <li>Ensure backend is running at {API_CONFIG.BASE_URL}</li>
            <li>Check console for detailed errors (F12 → Console)</li>
            <li>Verify network requests in Network tab</li>
            <li>Refresh the page (Ctrl+F5)</li>
          </ol>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <Navbar />
      <div className="dashboard-container">
        <div className="main-content">
          <Indicators data={state.indicators} />
          <MainChart 
            prices={state.priceData} 
            events={state.events} 
            changePoints={state.changePoints} 
          />
          <div className="analysis-section">
            <ChangePoints data={state.changePoints} />
            <EventsTimeline events={state.events} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;