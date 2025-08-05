import React from 'react';

const Navbar = () => {
  return (
    <nav className="navbar">
      <h1>Brent Crude Oil Price Dashboard</h1>
      <div className="nav-links">
        <a href="#prices">Price History</a>
        <a href="#analysis">Change Analysis</a>
        <a href="#events">Key Events</a>
      </div>
    </nav>
  );
};

export default Navbar;
