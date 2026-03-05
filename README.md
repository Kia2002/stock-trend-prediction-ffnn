# Stock Trend Prediction Using Feed-Forward Neural Networks and Financial Ratio Analysis

## Overview

This repository contains research focused on predicting stock price trends using machine learning models based on financial ratio analysis.

The project investigates whether fundamental financial indicators derived from company financial statements can be used to predict the future direction of stock prices.

The experiments focus on companies from the healthcare sector and combine approaches from:

- financial analysis
- machine learning
- neural networks
- decision modeling

The core modeling approach uses Feed-Forward Neural Networks (FFNN) trained on financial indicators and aggregated financial features.

---

## Dataset

The dataset contains financial indicators for publicly traded healthcare companies.

Indicators are derived from company financial statements and include multiple categories of financial ratios such as:

- liquidity ratios
- profitability ratios
- leverage ratios
- efficiency ratios
- valuation indicators
- cash-flow related metrics

Examples of indicators include:

- EBITDA margin
- Return on equity (ROE)
- earnings per share (EPS)
- debt to EBITDA ratio
- capital expenditures to revenue ratio
- price-based valuation metrics

---

## Data Preparation

Several preprocessing steps were applied before training the models.

### Handling Missing Values

Financial datasets frequently contain missing values.

To improve model reliability:

- missing values were replaced with column mean values
- columns with more than 50% missing values were removed

### Standardization

All numerical features were standardized before training in order to prevent variables with larger scales from dominating the learning process.

---

## Feature Engineering

Two different feature approaches were analyzed.

### Individual Financial Indicators

The first approach uses individual financial ratios directly as input features for the neural network.

This preserves detailed information about each financial indicator.

### Aggregated Financial Indicators

The second approach uses aggregated indicators constructed from groups of financial ratios.

Two aggregation methods were used:

- weighted linear aggregation
- logical aggregation based on interpolative Boolean algebra

This approach reduces dimensionality and creates composite indicators representing broader financial characteristics.

---

## Machine Learning Model

The primary model used in the experiments is a Feed-Forward Neural Network implemented using the MLPClassifier algorithm.

Configuration includes:

- Adam optimizer
- ReLU activation function
- L2 regularization
- early stopping to prevent overfitting
- up to 2000 training iterations

Multiple network architectures were tested with different numbers of hidden layers and neurons.

---

## Data Split

The dataset was divided into:

- Training set — 70%
- Validation set — 15%
- Test set — 15%

The validation set was used for model selection before evaluating final performance on the test set.

---

## Prediction Tasks

Three modeling approaches were explored.

### Return Prediction

Predicting the future return value of a stock.

### Trend Prediction

Predicting the direction of price movement as a classification problem.

Trend labels were defined using thresholds on stock returns.

### Trend Prediction with Aggregated Indicators

Using aggregated financial indicators as input features to examine whether aggregation improves prediction stability.

---

## Model Selection

A custom metric called Selection Score was used to select the best model architectures.

For regression tasks the score balances validation performance and overfitting risk.

For classification tasks the score combines precision and generalization ability between training and validation datasets.

---

## Experiments

Several experiments were conducted in order to evaluate the predictive capabilities of neural networks trained on financial indicators.

Different neural network architectures were tested by varying:

- number of hidden layers
- number of neurons per layer
- feature sets used as model inputs
- prediction horizons

The experiments compare the performance of models trained on:

- raw financial ratios
- aggregated financial indicators

This allows analysis of how feature dimensionality and information aggregation affect prediction performance.

---

## Key Research Questions

The project investigates several research questions:

- Can financial ratios derived from company financial statements predict future stock trends?
- Are feed-forward neural networks capable of detecting meaningful patterns in fundamental financial indicators?
- Does aggregation of financial ratios improve model stability and predictive performance?
- How does prediction performance change across different time horizons?

---

## Technologies

The project uses tools and concepts from the following areas:

- Machine Learning
- Neural Networks
- Financial Analysis
- Data Preprocessing
- Feature Engineering

Tools used in the implementation include:

- Python
- NumPy
- Pandas
- Scikit-learn
- Jupyter Notebooks
- Visual Studio Code

---

## Data Source

Financial data used in this project was collected from the Morningstar platform, which provides standardized financial information for publicly traded companies.

---

## Setup

To run the project locally:

1. Clone the repository

git clone https://github.com/Kia2002/stock-trend-prediction-ffnn.git

2. Navigate to the project folder

cd repository-name

3. Install required libraries

pip install numpy pandas scikit-learn jupyter

---

## Running Experiments

Experiments can be reproduced using the provided Jupyter notebooks.

1. Open the project folder in Visual Studio Code.
2. Open the notebook located in the `data_preparation` directory and run all cells to preprocess the dataset and generate the cleaned dataset used for modeling.
3. After data preparation is completed, open the notebooks corresponding to each model experiment.
4. Run the notebooks for:
   - Model 1
   - Model 2
   - Model 3
   - Model 2 vs Model 3
5. Each notebook contains the full pipeline including feature preparation, model training, and evaluation of results.

---

## Author

Aleksa Vlaški  
