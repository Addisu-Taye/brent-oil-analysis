# src/change_point_model.py

"""
Task ID:         Task-2
Created by:      Addisu Taye
Date Created:    30-JUL-2025
Purpose:         Perform Bayesian Change Point Analysis on Brent oil prices using PyMC.
Key Features:    - Implements a single change point model with MCMC sampling
                 - Estimates pre- and post-change means and uncertainty
                 - Generates posterior diagnostics and visualizations
"""

import pandas as pd
import pymc as pm
import numpy as np
import arviz as az
import matplotlib.pyplot as plt
import os
# --- FIX: PyMC v5 uses PyTensor for its backend ---
import pytensor.tensor as at
# --- NEW: Import data loading function from the dedicated module ---
from load_data import load_brent_prices


def run_change_point_model(df, output_dir="reports"):
    """
    Runs a Bayesian change point model on oil price data.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    price = df['Price'].values
    n = len(price)

    with pm.Model() as model:
        tau = pm.DiscreteUniform('tau', lower=0, upper=n - 1)
        mu_1 = pm.Normal('mu_1', mu=np.mean(price), sigma=10)
        mu_2 = pm.Normal('mu_2', mu=np.mean(price), sigma=10)
        sigma = pm.HalfNormal('sigma', sigma=10)

        mu = at.switch(at.ge(tau, np.arange(n)), mu_1, mu_2)
        
        likelihood = pm.Normal('y', mu=mu, sigma=sigma, observed=price)

        # MCMC Sampling
        trace = pm.sample(draws=2000, tune=1000, target_accept=0.95)

    az.plot_trace(trace, var_names=['mu_1', 'mu_2', 'sigma', 'tau'])
    plt.savefig(f"{output_dir}/trace_plot.png")
    plt.close()

    tau_samples = trace.posterior['tau'].values.flatten()
    most_probable_tau = int(pd.Series(tau_samples).mode()[0])
    change_date = df.iloc[most_probable_tau]['Date']

    plt.hist(tau_samples, bins=50, alpha=0.7, color='skyblue', density=True)
    plt.axvline(most_probable_tau, color='red', linestyle='--', label=f'MAP: {most_probable_tau}')
    plt.title("Posterior Distribution of Change Point (tau)")
    plt.xlabel("Time Index")
    plt.legend()
    plt.savefig(f"{output_dir}/posterior_tau.png")
    plt.close()

    return trace, change_date, most_probable_tau


def main():
    """Main execution function."""
    print("🔍 Starting Bayesian Change Point Analysis...")

    try:
        # --- NEW: Use the robust data loading function ---
        data_df = load_brent_prices()
    except FileNotFoundError as e:
        print(f"❌ Error: {e}. Please ensure data files are in the correct location.")
        return

    print(f"✅ Data loaded: {len(data_df)} records from {data_df['Date'].min().date()} to {data_df['Date'].max().date()}")

    trace, change_date, tau_idx = run_change_point_model(data_df)
    
    print("\n✅ Bayesian Analysis Complete.")
    print(f"Most probable change point occurred at index: {tau_idx}")
    print(f"Corresponding date: {change_date.strftime('%Y-%m-%d')}")
    print("Check the 'reports/' folder for visualizations.")


if __name__ == "__main__":
    main()