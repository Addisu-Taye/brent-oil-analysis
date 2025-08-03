"""
Task ID:        Task-1
Created by:     Addisu Taye
Date Created:   30-JUL-2025
Purpose:        Provide utility functions for loading external metadata such as geopolitical and economic events.
Key Features:   - Loads event data from CSV
               - Converts event dates to datetime
               - Returns structured DataFrame for event correlation analysis
"""

import pandas as pd

def load_events(file_path="events/key_oil_events.csv"):
    """
    Loads key geopolitical and economic events related to oil markets.
    

    Parameters:
        file_path (str): Path to the events CSV file
    
    Returns:
            pd.DataFrame: Events with columns ['Event', 'Date', 'Description']
    """
    events = pd.read_csv(file_path)
    events['Date'] = pd.to_datetime(events['Date'])
    return events