import React from 'react';

const ChangePoints = ({ data }) => {
  return (
    <div className="change-points-container">
      <h3>Significant Change Points</h3>
      <div className="change-points-list">
        {data.map((point, index) => (
          <div key={index} className="change-point-card">
            <div className="change-point-header">
              <span className="change-point-date">{point.date}</span>
              <span className="change-point-impact">
                {point.impact_percent > 0 ? '↑' : '↓'} {Math.abs(point.impact_percent)}%
              </span>
            </div>
            <h4>{point.event}</h4>
            <p>{point.description}</p>
            <div className="price-change">
              <span>Before: ${point.pre_mean.toFixed(2)}</span>
              <span>After: ${point.post_mean.toFixed(2)}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChangePoints;
