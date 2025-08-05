import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';
import './../styles/chartStyles.css';

const MainChart = ({ prices, events, changePoints }) => {
  const chartRef = useRef();

  useEffect(() => {
    if (!prices.length) return;

    const margin = { top: 40, right: 40, bottom: 60, left: 60 };
    const width = 1000 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    // Clear previous chart
    d3.select(chartRef.current).selectAll("*").remove();

    // Create SVG
    const svg = d3.select(chartRef.current)
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Parse dates
    const parseDate = d3.timeParse("%Y-%m-%d");
    const data = prices.map(d => ({
      date: parseDate(d.Date),
      price: +d.Price
    }));

    // Set scales
    const x = d3.scaleTime()
      .domain(d3.extent(data, d => d.date))
      .range([0, width]);

    const y = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.price) * 1.1])
      .range([height, 0]);

    // Add axes
    svg.append("g")
      .attr("class", "axis x-axis")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(x).ticks(10));

    svg.append("g")
      .attr("class", "axis y-axis")
      .call(d3.axisLeft(y));

    // Add grid lines
    svg.append("g")
      .attr("class", "grid")
      .call(d3.axisLeft(y).tickSize(-width).tickFormat(""));

    // Add line
    const line = d3.line()
      .x(d => x(d.date))
      .y(d => y(d.price));

    svg.append("path")
      .datum(data)
      .attr("class", "price-line")
      .attr("d", line);

    // Add change points
    changePoints.forEach(point => {
      const date = parseDate(point.date);
      svg.append("line")
        .attr("class", "change-point-line")
        .attr("x1", x(date))
        .attr("x2", x(date))
        .attr("y1", 0)
        .attr("y2", height);
      
      svg.append("text")
        .attr("class", "change-point-label")
        .attr("x", x(date) + 5)
        .attr("y", 20)
        .text(point.event);
    });

    // Add event markers
    events.forEach(event => {
      const date = parseDate(event.Date);
      svg.append("circle")
        .attr("class", "event-marker")
        .attr("cx", x(date))
        .attr("cy", y(data.find(d => +d.date === +date)?.price || height))
        .attr("r", 5);
    });

    // Add labels
    svg.append("text")
      .attr("class", "y-label")
      .attr("transform", "rotate(-90)")
      .attr("y", -margin.left + 15)
      .attr("x", -height / 2)
      .text("Price (USD)");

    svg.append("text")
      .attr("class", "x-label")
      .attr("x", width / 2)
      .attr("y", height + margin.bottom - 10)
      .text("Date");

  }, [prices, events, changePoints]);

  return (
    <div className="chart-container">
      <h2>Brent Crude Oil Price History</h2>
      <div ref={chartRef} className="price-chart"></div>
    </div>
  );
};

export default MainChart;
