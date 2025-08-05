import React from 'react';

const EventsTimeline = ({ events }) => {
  return (
    <div className="events-timeline-container">
      <h3>Key Oil Market Events</h3>
      <div className="timeline">
        {events.map((event, index) => (
          <div key={index} className="timeline-item">
            <div className="timeline-date">{event.Date}</div>
            <div className="timeline-content">
              <h4>{event.Event}</h4>
              <p>{event.Description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EventsTimeline;
