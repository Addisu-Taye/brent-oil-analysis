import React, { useEffect, useState } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine
} from 'recharts';
import { PriceData, ChangePointData } from '../types';
import { fetchData } from '../services/api';

export default function PriceChart() {
  const [data, setData] = useState<PriceData[]>([]);

  useEffect(() => {
    const load = async () => {
      try {
        const prices = await fetchData<PriceData[]>('prices');
        const changePoints = await fetchData<ChangePointData[]>('change_points');
        setData(prices);
      } catch (err) {
        console.error("Failed to load price data", err);
      }
    };
    load();
  }, []);

  return (
    <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200 h-80">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">Brent Oil Price Trend</h2>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="Date" tick={{ fontSize: 12 }} interval="preserveStartEnd" angle={-45} textAnchor="end" height={60} />
          <YAxis label={{ value: 'Price (USD)', angle: -90, position: 'insideLeft', fontSize: 12 }} />
          <Tooltip formatter={(value) => `$${Number(value).toFixed(2)}`} />
          <Legend />
          <Line type="monotone" dataKey="Price" stroke="#4F46E5" name="Brent Price" dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}