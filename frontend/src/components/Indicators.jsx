import React from 'react';

const Indicators = ({ data }) => {
  if (!data) return null;

  return (
    <div className="indicators-container">
      <div className="indicator-card">
        <h3>Current Price</h3>
        <p className="indicator-value">${data.latest_price}</p>
      </div>
      <div className="indicator-card">
        <h3>Average Price</h3>
        <p className="indicator-value">${data.average_price}</p>
      </div>
      <div className="indicator-card">
        <h3>Volatility</h3>
        <p className="indicator-value">{data.annualized_volatility}%</p>
      </div>
      <div className="indicator-card">
        <h3>Key Events</h3>
        <p className="indicator-value">{data.total_events}</p>
      </div>
      <div className="indicator-card">
        <h3>Change Points</h3>
        <p className="indicator-value">{data.detected_change_points}</p>
      </div>
    </div>
  );
};

export default Indicators;
