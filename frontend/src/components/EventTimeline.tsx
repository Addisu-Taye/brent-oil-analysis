import React, { useState, useEffect } from 'react';
import { EventData } from '../types';
import { fetchData } from '../services/api';

export default function EventTimeline() {
  const [events, setEvents] = useState<EventData[]>([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    fetchData<EventData[]>('events').then(setEvents).catch(console.error);
  }, []);

  const filtered = events.filter(e => e.Event.toLowerCase().includes(filter.toLowerCase()));

  return (
    <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">Key Events Timeline</h2>
      <input
        type="text"
        placeholder="Filter events..."
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        className="w-full p-2 mb-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
      />
      <div className="space-y-3 max-h-80 overflow-y-auto">
        {filtered.map((e, i) => (
          <div key={i} className="border-l-2 border-red-500 pl-3 py-1">
            <p className="font-medium text-gray-800">{e.Date}</p>
            <p className="font-medium text-blue-600">{e.Event}</p>
            <p className="text-sm text-gray-600">{e.Description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}