# ==============================================================================
# Setup and Data Loading
# ==============================================================================
import pandas as pd
import pymc as pm
import numpy as np
import arviz as az
import matplotlib.pyplot as plt
import os
import pytensor.tensor as at
#from google.colab import drive

# Mount Google Drive to access data files
#drive.mount('/content/drive')

# Define the data loading function
def load_brent_prices(data_path="./data/BrentOilPrices.csv"):
    """
    Loads and preprocesses Brent oil price data from a CSV file.
    """
    try:
        df = pd.read_csv(data_path, parse_dates=['Date'])
        df.columns = ['Date', 'Price']
        df.sort_values(by='Date', inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df
    except FileNotFoundError:
        print(f"❌ Error: Data file not found at {data_path}. Please check the path.")
        return None

# ==============================================================================
# Bayesian Change Point Analysis Functions
# ==============================================================================

def run_change_point_model(df, output_dir="./reports"):
    """
    Runs a Bayesian change point model on oil price data and returns the trace.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    price = df['Price'].values
    n = len(price)

    with pm.Model() as model:
        tau = pm.DiscreteUniform('tau', lower=0, upper=n - 1)
        mu_1 = pm.Normal('mu_1', mu=np.mean(price), sigma=10)
        mu_2 = pm.Normal('mu_2', mu=np.mean(price), sigma=10)
        sigma = pm.HalfNormal('sigma', sigma=10)

        mu = at.switch(at.ge(np.arange(n), tau), mu_2, mu_1)
        
        likelihood = pm.Normal('y', mu=mu, sigma=sigma, observed=price)

        trace = pm.sample(draws=2000, tune=1000, target_accept=0.95)

    az.plot_trace(trace, var_names=['mu_1', 'mu_2', 'sigma'])
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


def save_summary_to_csv(trace, change_date, output_dir="./reports"):
    """
    Saves a summary of the model results to a CSV file.
    """
    mu_1_summary = az.summary(trace, var_names=['mu_1'], hdi_prob=0.95)
    mu_2_summary = az.summary(trace, var_names=['mu_2'], hdi_prob=0.95)

    mu_1_mean = mu_1_summary['mean'].values[0]
    mu_1_hdi_low = mu_1_summary['hdi_3%'].values[0]
    mu_1_hdi_high = mu_1_summary['hdi_97%'].values[0]

    mu_2_mean = mu_2_summary['mean'].values[0]
    mu_2_hdi_low = mu_2_summary['hdi_3%'].values[0]
    mu_2_hdi_high = mu_2_summary['hdi_97%'].values[0]

    summary_data = {
        "Metric": ["Pre-Change Mean", "Post-Change Mean", "Change Point Date"],
        "Value": [mu_1_mean, mu_2_mean, change_date],
        "HDI 3%": [mu_1_hdi_low, mu_2_hdi_low, np.nan],
        "HDI 97%": [mu_1_hdi_high, mu_2_hdi_high, np.nan]
    }
    
    summary_df = pd.DataFrame(summary_data)
    
    csv_path = os.path.join(output_dir, "analysis_summary.csv")
    summary_df.to_csv(csv_path, index=False)
    print(f" Summary data saved to {csv_path}")


def main():
    """Main execution function."""
    print("🔍 Starting Bayesian Change Point Analysis...")

    data_path = "./data/BrentOilPrices.csv"
    data_df = load_brent_prices(data_path)

    if data_df is None:
        return

    print(f" Data loaded: {len(data_df)} records from {data_df['Date'].min().date()} to {data_df['Date'].max().date()}")

    trace, change_date, tau_idx = run_change_point_model(data_df)
    
    print("\n Bayesian Analysis Complete.")
    print(f"Most probable change point occurred at index: {tau_idx}")
    print(f"Corresponding date: {change_date.strftime('%Y-%m-%d')}")
    print("Check the 'reports/' folder for visualizations and 'analysis_summary.csv'.")

    save_summary_to_csv(trace, change_date)


# ==============================================================================
# Run the analysis
# ==============================================================================
if __name__ == "__main__":
    main()