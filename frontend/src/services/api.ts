const API_BASE = 'http://localhost:5000/api';

export const fetchData = async <T,>(endpoint: string): Promise<T> => {
  const response = await fetch(`${API_BASE}/${endpoint}`);
  if (!response.ok) throw new Error(`Failed to fetch ${endpoint}`);
  return await response.json();
};