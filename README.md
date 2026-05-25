# Stock Trend Prediction Using Feed-Forward Neural Networks

A machine learning research project investigating whether fundamental financial ratios derived from company financial statements can be used to predict the future direction of stock prices, with a focus on the healthcare sector.

## Overview

This project explores the application of Feed-Forward Neural Networks (FFNN) to the problem of stock trend prediction using financial ratio analysis. Two feature engineering approaches are compared: raw individual financial indicators versus aggregated composite indicators constructed using interpolative Boolean algebra. The study evaluates prediction performance across multiple time horizons and network architectures.

## Research Questions

- Can financial ratios derived from company financial statements reliably predict future stock price trends?
- Are feed-forward neural networks capable of extracting meaningful patterns from fundamental financial indicators?
- Does aggregating financial ratios into composite indicators improve model stability and predictive performance?
- How does prediction accuracy vary across different time horizons?

## Dataset

Financial data was collected from [Morningstar](https://www.morningstar.com/) for publicly traded healthcare sector companies. Indicators span multiple categories of financial ratios:

| Category | Example Indicators |
|---|---|
| Liquidity | Current ratio, quick ratio |
| Profitability | EBITDA margin, return on equity (ROE) |
| Leverage | Debt-to-EBITDA ratio |
| Efficiency | Asset turnover |
| Valuation | Price-based valuation metrics, EPS |
| Cash Flow | CapEx-to-revenue ratio |

### Preprocessing

- Missing values replaced with column means
- Columns with more than 50% missing values removed
- All features standardized before training

## Feature Engineering

Two distinct input representations are compared:

**Individual Financial Indicators** — Raw financial ratios used directly as model inputs, preserving full granularity.

**Aggregated Financial Indicators** — Composite indicators constructed from groups of financial ratios using:
- Weighted linear aggregation
- Logical aggregation based on interpolative Boolean algebra

Aggregation reduces input dimensionality and creates higher-level features that represent broader financial health dimensions.

## Model Architecture

The primary model is a Feed-Forward Neural Network implemented with scikit-learn's `MLPClassifier`.

| Parameter | Configuration |
|---|---|
| Optimizer | Adam |
| Activation | ReLU |
| Regularization | L2 |
| Early Stopping | Enabled |
| Max Iterations | 2000 |

Multiple architectures were evaluated by varying the number of hidden layers and neurons per layer.

## Data Split

| Split | Proportion |
|---|---|
| Training | 70% |
| Validation | 15% |
| Test | 15% |

The validation set was used for architecture selection; final performance is reported on the held-out test set.

## Prediction Tasks

Three prediction tasks are investigated:

1. **Return Prediction** — Regression task predicting the future return value of a stock.
2. **Trend Prediction** — Binary classification predicting price movement direction, with trend labels derived from return thresholds.
3. **Trend Prediction with Aggregated Indicators** — Same classification task using aggregated composite features as inputs.

## Model Selection

A custom **Selection Score** metric was used for architecture selection:

- **Regression tasks:** Balances validation performance against overfitting risk.
- **Classification tasks:** Combines precision with the generalization gap between training and validation accuracy.

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Primary language |
| NumPy | Numerical computation |
| Pandas | Data manipulation |
| Scikit-learn | ML model implementation |
| SciPy | Statistical functions |
| Matplotlib / Seaborn | Plotting and visualization |
| openpyxl | Reading and writing `.xlsx` data files |

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/Kia2002/stock-trend-prediction-ffnn.git
cd stock-trend-prediction-ffnn
pip install numpy pandas scikit-learn scipy matplotlib seaborn openpyxl
```

### Running Experiments

The pipeline is implemented as standalone Python scripts (not notebooks).

1. Open the project in your editor of choice (e.g., VS Code).
2. Each script defines a hardcoded `folder_putanja` (or input file path) pointing to its own directory on the original author's machine. Before running a script, update this path to the corresponding directory in your local clone.
3. Run `data_preparation/data_preparation.py` to preprocess the dataset.
4. After data preparation completes, run the experiment scripts in order:
   - `Model 1/model1.py` — Baseline model on individual indicators
   - `Model 2/model 2.py` — Model on aggregated indicators (linear aggregation)
   - `Model 3/model3.py` — Model on aggregated indicators (logical aggregation)
   - `Model 2 vs Model 3/model2_averages.py` and `model3_averages.py` — Comparative analysis of aggregation methods

Each script covers a stage of the pipeline: feature preparation, model training and evaluation, or results comparison, writing its output to `.xlsx` files in its own directory.

## Author

Aleksa Vlaški

## License

This project is intended for academic and portfolio purposes.
