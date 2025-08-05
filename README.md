```
# 🛢️ Brent Oil Price Change Point Analysis  
*A 10 Academy - KAIM Week 10 Challenge Project*  
**By: Addisu Taye | Birhan Energies – Data Science Division**

---

## 📌 Project Overview  
This project detects structural breaks in Brent crude oil prices using **Bayesian Change Point Analysis** with PyMC3. It identifies when and how major geopolitical, economic, and OPEC-related events caused statistically significant shifts in oil prices between 1987 and 2023.

The analysis is supported by an interactive **dashboard (FastAPI + React)** and a **storytelling-style final report**, enabling stakeholders to explore, understand, and act on data-driven insights.

---

## 🎯 Business Objective
- Detect when structural breaks occurred in oil prices.
- Associate these changes with real-world events (e.g., wars, OPEC decisions, pandemics).
- Quantify the impact of events on price levels.
- Communicate findings through a professional report and interactive dashboard.

---

## 🧩 Key Components
- **Data Analysis** – Python, pandas, NumPy  
- **Bayesian Modeling** – PyMC3, ArviZ, MCMC  
- **Exploratory Analysis** – Matplotlib, Seaborn  
- **Dashboard Backend** – FastAPI  
- **Dashboard Frontend** – React, TypeScript, Tailwind CSS, Recharts  
- **Reporting** – python-docx, storytelling  

---

## 📂 Project Structure
```
brent-oil-analysis/
├── data/
│   ├── BrentOilPrices.csv              # Raw price data (mixed formats)
│   └── BrentOilPrices_clean.csv        # Cleaned & parsed data
├── events/
│   └── key_oil_events.csv              # 15+ curated events (OPEC, wars, crises)
├── reports/
│   ├── price_series.png                # Full price trend
│   ├── log_returns.png                 # Volatility clustering
│   ├── posterior_tau.png               # Posterior of change point (2005)
│   ├── trace_plot.png                  # MCMC convergence diagnostics
│   ├── posterior_tau_2020.png          # Posterior of change point (2020)
│   └── trace_plot_2020.png             # MCMC diagnostics for 2020 model
├── backend/
│   └── app.py                          # FastAPI backend
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/                 # Recharts, filters, timeline
│   │   ├── services/api.ts
│   │   └── App.tsx
│   └── package.json
├── src/
│   ├── load_data.py                    # Handles mixed date formats
│   ├── change_point_model.py           # Bayesian model with PyMC3
│   ├── visualize.py                    # Plotting functions
│   └── utils.py                        # Load events
├── analysis_summary.csv                # 2005 regime shift results
├── analysis_summary_2020.csv           # 2020 pandemic-era results
├── final_report.docx                   # Generated final report
├── interim_report.docx                 # Interim submission
├── requirements.txt
└── README.md                           # This file
```

---

## 🔍 Key Insights

### 🔴 Change Point 1: February 25, 2005 – Global Demand Surge
- Pre-Change Mean: $21.45  
- Post-Change Mean: $75.59  
- Impact: +252% price increase  
- Event: Rising demand from China and India  
- Confidence: **100% probability** (no HDI overlap)

### 🔴 Change Point 2: April 21, 2020 – OPEC+ Production Cut
- Pre-Change Mean: $22.10  
- Post-Change Mean: $28.45  
- Impact: +28.7% recovery  
- Event: Historic 10M bpd cut  
- Confidence: **99.3% probability**

---

## 📈 Analysis Plots
1. Brent Oil Price Series (1987–2023) – Major trends, volatility clusters, change points  
2. Log Returns – Volatility clustering (e.g., 2008, 2020)  
3. Posterior Distribution (2005) – Sharp peak at Feb 25, 2005  
4. MCMC Trace Plot (2005) – Good convergence (r_hat ≈ 1.0)  
5. Posterior Distribution (2020) – Post-OPEC+ agreement  
6. MCMC Trace Plot (2020) – Converged well  

---

## 🖥️ Interactive Dashboard
Built with **FastAPI** (backend) and **React** (frontend):

- View historical price trends with event markers  
- Filter by date and event  
- Visualize change point indicators  
- Fully interactive and responsive  

---

## 🔧 Run the Dashboard

```bash
# 1. Start FastAPI backend
cd backend  
pip install -r requirements.txt  
uvicorn app:app --reload  

# 2. Start React frontend
cd ../frontend  
npm install  
npm run dev  

# Open browser: http://localhost:5173
```

---

## 📊 Key Features
✅ Historical Trends with Annotations  
✅ Real-world Event Correlation (OPEC, war, pandemic)  
✅ Interactive Filtering  
✅ Fully Responsive UI  
✅ Key Indicators (price, volatility, change)  
✅ Probabilistic Interpretation  

---



---

## 📦 Requirements

```txt
pandas==2.0.3  
numpy==1.24.3  
matplotlib==3.7.2  
seaborn==0.12.2  
pymc3==3.11.5  
arviz==0.15.1  
fastapi==0.109.2  
uvicorn==0.27.1  
python-docx==1.1.2
```

```bash
pip install -r requirements.txt
```

---

## 🚀 Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/addisu-taye/brent-oil-analysis.git  
cd brent-oil-analysis  
```

### 2. Clean Raw Data
```bash
python -c "  
import re  
with open('BrentOilPrices.csv', 'r') as f:  
    content = f.read().replace('\n', '').replace('\r', '')  
pattern = r'(?:\"([A-Za-z]{3} \d{1,2}, \d{4})\"|(\d{1,2}-[A-Za-z]{3}-\d{2})),([0-9]+\.[0-9]+)'  
matches = re.findall(pattern, content)  
with open('data/BrentOilPrices_clean.csv', 'w') as f:  
    f.write('Date,Price\n')  
    for m in matches:  
        date = m[0] if m[0] else m[1]  
        f.write(f'{date},{m[2]}\n')  
print('✅ Data cleaned and saved to data/BrentOilPrices_clean.csv')  
"
```

### 3. Run Exploratory Analysis
```bash
python -m src.exploratory_analysis
```

### 4. Run Bayesian Model
```bash
python src/change_point_model.py
```

### 5. Generate Final Report
```bash
python generate_final_report.py
```

---

## 📎 Interim Submission
✅ `interim_report.docx` – Draft report  
✅ `events/key_oil_events.csv` – Cleaned dataset  
✅ GitHub: https://github.com/addisu-taye/brent-oil-analysis  

---

## 📚 References
- Bayesian Change Point Detection (PyMC)  
- MCMC Explained  
- Data Science Workflow Best Practices  

---

## 🙌 Acknowledgements
- **10 Academy Tutors**: Mahlet, Rediet, Kerod, Rehmet  
- **Birhan Energies** – For business context  
- **Open Source Community** – PyMC, ArviZ, FastAPI, React  

---

## 📬 Contact  
**Addisu Taye**  
📧 addtaye@gmail.com  
🔗 [GitHub](https://github.com/addisu-taye) | [LinkedIn](https://linkedin.com/in/addisut)

> "The goal is not just to detect change — but to anticipate it."  
> — *Birhan Energies Data Science Team*
```
