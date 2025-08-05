export interface PriceData {
  Date: string;
  Price: number;
}

export interface EventData {
  Event: string;
  Date: string;
  Description: string;
}

export interface ChangePointData {
  date: string;
  pre_mean: number;
  post_mean: number;
  impact_percent: number;
  event: string;
  description: string;
}

export interface IndicatorData {
  latest_price: number;
  average_price: number;
  annualized_volatility: number;
  total_events: number;
  detected_change_points: number;
}