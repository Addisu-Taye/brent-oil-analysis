import React, { useEffect, useState } from 'react';
import PriceChart from './components/PriceChart';
import EventTimeline from './components/EventTimeline';
import IndicatorCard from './components/IndicatorCard';
import { fetchData } from './services/api';
import { IndicatorData } from './types';

export default function App() {
  const [indicators, setIndicators] = useState<IndicatorData | null>(null);

  useEffect(() => {
    fetchData<IndicatorData>('indicators').then(setIndicators).catch(console.error);
  }, []);

  if (!indicators) {
    return <div className="p-8">Loading dashboard...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-2xl font-bold text-gray-900">Birhan Energies</h1>
          <p className="text-gray-600">Brent Oil Price Change Point Dashboard</p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <IndicatorCard title="Latest Price" value={`$${indicators.latest_price}`} />
          <IndicatorCard title="Average Price" value={`$${indicators.average_price}`} />
          <IndicatorCard title="Volatility" value={`${indicators.annualized_volatility}%`} />
          <IndicatorCard title="Change Points" value={indicators.detected_change_points} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="lg:col-span-2">
            <PriceChart />
          </div>
          <EventTimeline />
        </div>
      </main>

      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 text-center text-gray-500 text-sm">
          © 2025 Birhan Energies | Data Science Division
        </div>
      </footer>
    </div>
  );
}