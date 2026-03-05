import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_excel(r"C:\Users\Aleksa\Documents\Predvidjanje\data_preparation\healthcare_data.xlsx", sheet_name="Data")


general_features = df[['Name', 'Morningstar Sector', 'Morningstar Industry', 'Country', 'Market Cap (mil) (Daily)']]


moat_features = df[['Economic Moat', 'Moat Source - Efficient Scale', 'Moat Source - Switch Cost', 
                    'Moat Source - Cost Advantage', 'Moat Source - Network Effect', 'Moat Source - Intangible Assets']]

rating_features = df[['Morningstar Rating Overall']]

price_features = df[['Price To Fair Value']]

momentum_features = df[['Momentum Score %']]

returns_features = df[['Total Ret 3 Mo (Daily)', 'Total Ret 6 Mo (Daily)', 'Total Ret YTD (Daily)',
                       'Total Ret 1 Yr (Daily)', 'Total Ret Annlzd 3 Yr (Daily)', 'Total Ret Annlzd 5 Yr (Daily)']]


def revenue_features(df):
    
    df['Total Revenue 1 Year Growth-FY'] = pd.to_numeric(df['Total Revenue 1 Year Growth-FY'], errors='coerce')
    df['Total Revenue 3 Year Growth-FY'] = pd.to_numeric(df['Total Revenue 3 Year Growth-FY'], errors='coerce')
    df['Total Revenue 5 Year Growth-FY'] = pd.to_numeric(df['Total Revenue 5 Year Growth-FY'], errors='coerce')
    df['Total Revenue Value-FY'] = pd.to_numeric(df['Total Revenue Value-FY'], errors='coerce')

   
    df['Revenue_1Yr_Avg'] = df['Total Revenue 1 Year Growth-FY']
    df['Revenue_3Yr_Avg'] = df['Total Revenue 3 Year Growth-FY'] / 3
    df['Revenue_5Yr_Avg'] = df['Total Revenue 5 Year Growth-FY'] / 5
    
    df['Revenue_1Yr/3Yr'] = df['Revenue_1Yr_Avg'] / df['Revenue_3Yr_Avg']
    df['Revenue_1Yr/5Yr'] = df['Revenue_1Yr_Avg'] / df['Revenue_5Yr_Avg']
    
    df['Revenue_Value'] = df['Total Revenue Value-FY']
    
    return df[['Revenue_Value','Revenue_1Yr_Avg','Revenue_3Yr_Avg','Revenue_5Yr_Avg','Revenue_1Yr/3Yr','Revenue_1Yr/5Yr']]

def gross_margin_features(df):
    years = ['Gross Margin-FY_2020-12-31', 'Gross Margin-FY_2021-12-31',
             'Gross Margin-FY_2022-12-31', 'Gross Margin-FY_2023-12-31',
             'Gross Margin-FY_2024-12-31']
    
    for col in years:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
   
    df['GrossMargin_1Yr_Avg'] = df['Gross Margin-FY_2024-12-31']
    
    
    df['GrossMargin_3Yr_Avg'] = df[['Gross Margin-FY_2022-12-31', 
                                    'Gross Margin-FY_2023-12-31', 
                                    'Gross Margin-FY_2024-12-31']].mean(axis=1)
    
  
    df['GrossMargin_5Yr_Avg'] = df[years].mean(axis=1)
    
   
    df['GrossMargin_1Yr/3Yr'] = df['GrossMargin_1Yr_Avg'] / df['GrossMargin_3Yr_Avg']
    df['GrossMargin_1Yr/5Yr'] = df['GrossMargin_1Yr_Avg'] / df['GrossMargin_5Yr_Avg']
    
    return df[['GrossMargin_1Yr_Avg', 'GrossMargin_3Yr_Avg', 'GrossMargin_5Yr_Avg', 
               'GrossMargin_1Yr/3Yr', 'GrossMargin_1Yr/5Yr']]

def operating_margin_features(df):
    
    years = ['2020-12-31','2021-12-31','2022-12-31','2023-12-31','2024-12-31']
    for year in years:
        col_name = f'Operating Margin-FY_{year}'
        df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
    
    
    df['OperatingMargin_1Yr_Avg'] = df['Operating Margin-FY_2024-12-31']
    df['OperatingMargin_3Yr_Avg'] = df[['Operating Margin-FY_2022-12-31',
                                 'Operating Margin-FY_2023-12-31',
                                 'Operating Margin-FY_2024-12-31']].mean(axis=1)
    df['OperatingMargin_5Yr_Avg'] = df[['Operating Margin-FY_2020-12-31',
                                 'Operating Margin-FY_2021-12-31',
                                 'Operating Margin-FY_2022-12-31',
                                 'Operating Margin-FY_2023-12-31',
                                 'Operating Margin-FY_2024-12-31']].mean(axis=1)
    
    df['OperatingMargin_1Yr/3Yr'] = df['OperatingMargin_1Yr_Avg'] / df['OperatingMargin_3Yr_Avg']
    df['OperatingMargin_1Yr/5Yr'] = df['OperatingMargin_1Yr_Avg'] / df['OperatingMargin_5Yr_Avg']
    
    return df[['OperatingMargin_1Yr_Avg','OperatingMargin_3Yr_Avg','OperatingMargin_5Yr_Avg','OperatingMargin_1Yr/3Yr','OperatingMargin_1Yr/5Yr']]

def net_profit_margin_features(df):
    for year in range(2020, 2025):
        col = f'Net Profit Margin-FY_{year}-12-31'
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df['NetProfitMargin_1Yr_Avg'] = df['Net Profit Margin-FY_2024-12-31']
    df['NetProfitMargin_3Yr_Avg'] = df[['Net Profit Margin-FY_2022-12-31',
                                  'Net Profit Margin-FY_2023-12-31',
                                  'Net Profit Margin-FY_2024-12-31']].mean(axis=1)
    df['NetProfitMargin_5Yr_Avg'] = df[['Net Profit Margin-FY_2020-12-31',
                                  'Net Profit Margin-FY_2021-12-31',
                                  'Net Profit Margin-FY_2022-12-31',
                                  'Net Profit Margin-FY_2023-12-31',
                                  'Net Profit Margin-FY_2024-12-31']].mean(axis=1)
    
    df['NetProfitMargin_1Yr/3Yr'] = df['NetProfitMargin_1Yr_Avg'] / df['NetProfitMargin_3Yr_Avg']
    df['NetProfitMargin_1Yr/5Yr'] = df['NetProfitMargin_1Yr_Avg'] / df['NetProfitMargin_5Yr_Avg']
    
    return df[['NetProfitMargin_1Yr_Avg','NetProfitMargin_3Yr_Avg','NetProfitMargin_5Yr_Avg','NetProfitMargin_1Yr/3Yr','NetProfitMargin_1Yr/5Yr']]

def ebit_margin_features(df):
    for year in range(2020, 2025):
        col = f'Ebit Margin-FY_{year}-12-31'
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df['Ebit_1Yr_Avg'] = df['Ebit Margin-FY_2024-12-31']
    df['Ebit_3Yr_Avg'] = df[['Ebit Margin-FY_2022-12-31',
                             'Ebit Margin-FY_2023-12-31',
                             'Ebit Margin-FY_2024-12-31']].mean(axis=1)
    df['Ebit_5Yr_Avg'] = df[['Ebit Margin-FY_2020-12-31',
                             'Ebit Margin-FY_2021-12-31',
                             'Ebit Margin-FY_2022-12-31',
                             'Ebit Margin-FY_2023-12-31',
                             'Ebit Margin-FY_2024-12-31']].mean(axis=1)
    
    df['Ebit_1Yr/3Yr'] = df['Ebit_1Yr_Avg'] / df['Ebit_3Yr_Avg']
    df['Ebit_1Yr/5Yr'] = df['Ebit_1Yr_Avg'] / df['Ebit_5Yr_Avg']
    
    return df[['Ebit_1Yr_Avg','Ebit_3Yr_Avg','Ebit_5Yr_Avg','Ebit_1Yr/3Yr','Ebit_1Yr/5Yr']]

def ebitda_margin_features(df):
    for year in range(2020, 2025):
        col = f'Ebitda Margin-FY_{year}-12-31'
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df['Ebitda_1Yr_Avg'] = df['Ebitda Margin-FY_2024-12-31']
    df['Ebitda_3Yr_Avg'] = df[['Ebitda Margin-FY_2022-12-31',
                               'Ebitda Margin-FY_2023-12-31',
                               'Ebitda Margin-FY_2024-12-31']].mean(axis=1)
    df['Ebitda_5Yr_Avg'] = df[['Ebitda Margin-FY_2020-12-31',
                               'Ebitda Margin-FY_2021-12-31',
                               'Ebitda Margin-FY_2022-12-31',
                               'Ebitda Margin-FY_2023-12-31',
                               'Ebitda Margin-FY_2024-12-31']].mean(axis=1)
    
    df['Ebitda_1Yr/3Yr'] = df['Ebitda_1Yr_Avg'] / df['Ebitda_3Yr_Avg']
    df['Ebitda_1Yr/5Yr'] = df['Ebitda_1Yr_Avg'] / df['Ebitda_5Yr_Avg']
    
    return df[['Ebitda_1Yr_Avg','Ebitda_3Yr_Avg','Ebitda_5Yr_Avg','Ebitda_1Yr/3Yr','Ebitda_1Yr/5Yr']]

def roa_features(df):
    for year in range(2020, 2025):
        col = f'Return On Asset-FY_{year}-12-31'
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df['ROA_1Yr_Avg'] = df['Return On Asset-FY_2024-12-31']
    df['ROA_3Yr_Avg'] = df[['Return On Asset-FY_2022-12-31',
                            'Return On Asset-FY_2023-12-31',
                            'Return On Asset-FY_2024-12-31']].mean(axis=1)
    df['ROA_5Yr_Avg'] = df[['Return On Asset-FY_2020-12-31',
                            'Return On Asset-FY_2021-12-31',
                            'Return On Asset-FY_2022-12-31',
                            'Return On Asset-FY_2023-12-31',
                            'Return On Asset-FY_2024-12-31']].mean(axis=1)
    
    df['ROA_1Yr/3Yr'] = df['ROA_1Yr_Avg'] / df['ROA_3Yr_Avg']
    df['ROA_1Yr/5Yr'] = df['ROA_1Yr_Avg'] / df['ROA_5Yr_Avg']
    
    return df[['ROA_1Yr_Avg','ROA_3Yr_Avg','ROA_5Yr_Avg','ROA_1Yr/3Yr','ROA_1Yr/5Yr']]

def roe_features(df):
    for year in range(2020, 2025):
        col = f'Return On Equity-FY_{year}-12-31'
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df['ROE_1Yr_Avg'] = df['Return On Equity-FY_2024-12-31']
    df['ROE_3Yr_Avg'] = df[['Return On Equity-FY_2022-12-31',
                            'Return On Equity-FY_2023-12-31',
                            'Return On Equity-FY_2024-12-31']].mean(axis=1)
    df['ROE_5Yr_Avg'] = df[['Return On Equity-FY_2020-12-31',
                            'Return On Equity-FY_2021-12-31',
                            'Return On Equity-FY_2022-12-31',
                            'Return On Equity-FY_2023-12-31',
                            'Return On Equity-FY_2024-12-31']].mean(axis=1)
    
    df['ROE_1Yr/3Yr'] = df['ROE_1Yr_Avg'] / df['ROE_3Yr_Avg']
    df['ROE_1Yr/5Yr'] = df['ROE_1Yr_Avg'] / df['ROE_5Yr_Avg']
    
    return df[['ROE_1Yr_Avg','ROE_3Yr_Avg','ROE_5Yr_Avg','ROE_1Yr/3Yr','ROE_1Yr/5Yr']]

def roic_features(df):
    for year in range(2020, 2025):
        col = f'Return On Invested Capital-FY_{year}-12-31'
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df['ROIC_1Yr_Avg'] = df['Return On Invested Capital-FY_2024-12-31']
    df['ROIC_3Yr_Avg'] = df[['Return On Invested Capital-FY_2022-12-31',
                             'Return On Invested Capital-FY_2023-12-31',
                             'Return On Invested Capital-FY_2024-12-31']].mean(axis=1)
    df['ROIC_5Yr_Avg'] = df[['Return On Invested Capital-FY_2020-12-31',
                             'Return On Invested Capital-FY_2021-12-31',
                             'Return On Invested Capital-FY_2022-12-31',
                             'Return On Invested Capital-FY_2023-12-31',
                             'Return On Invested Capital-FY_2024-12-31']].mean(axis=1)
    
    df['ROIC_1Yr/3Yr'] = df['ROIC_1Yr_Avg'] / df['ROIC_3Yr_Avg']
    df['ROIC_1Yr/5Yr'] = df['ROIC_1Yr_Avg'] / df['ROIC_5Yr_Avg']
    
    return df[['ROIC_1Yr_Avg','ROIC_3Yr_Avg','ROIC_5Yr_Avg','ROIC_1Yr/3Yr','ROIC_1Yr/5Yr']]

def fcf_sales_features(df):
    for year in range(2020, 2025):
        col = f'Free Cash Flow To Sales Ratio-FY_{year}-12-31'
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 1Yr, 3Yr i 5Yr proseci
    df['FCF/Sales_1Yr_Avg'] = df['Free Cash Flow To Sales Ratio-FY_2024-12-31']
    df['FCF/Sales_3Yr_Avg'] = df[['Free Cash Flow To Sales Ratio-FY_2022-12-31',
                                   'Free Cash Flow To Sales Ratio-FY_2023-12-31',
                                   'Free Cash Flow To Sales Ratio-FY_2024-12-31']].mean(axis=1)
    df['FCF/Sales_5Yr_Avg'] = df[['Free Cash Flow To Sales Ratio-FY_2020-12-31',
                                   'Free Cash Flow To Sales Ratio-FY_2021-12-31',
                                   'Free Cash Flow To Sales Ratio-FY_2022-12-31',
                                   'Free Cash Flow To Sales Ratio-FY_2023-12-31',
                                   'Free Cash Flow To Sales Ratio-FY_2024-12-31']].mean(axis=1)
    
    df['FCF/Sales_1Yr/3Yr'] = df['FCF/Sales_1Yr_Avg'] / df['FCF/Sales_3Yr_Avg']
    df['FCF/Sales_1Yr/5Yr'] = df['FCF/Sales_1Yr_Avg'] / df['FCF/Sales_5Yr_Avg']
    
    return df[['FCF/Sales_1Yr_Avg','FCF/Sales_3Yr_Avg','FCF/Sales_5Yr_Avg','FCF/Sales_1Yr/3Yr','FCF/Sales_1Yr/5Yr']]

def fcf_growth_features(df):
    df['Free Cash Flow 1 Year Growth-FY'] = pd.to_numeric(df['Free Cash Flow 1 Year Growth-FY'], errors='coerce')
    df['Free Cash Flow 3 Year Growth-FY'] = pd.to_numeric(df['Free Cash Flow 3 Year Growth-FY'], errors='coerce')
    df['Free Cash Flow 5 Year Growth-FY'] = pd.to_numeric(df['Free Cash Flow 5 Year Growth-FY'], errors='coerce')

    df['FCF_Growth_1Yr_Avg'] = df['Free Cash Flow 1 Year Growth-FY']
    df['FCF_Growth_3Yr_Avg'] = df['Free Cash Flow 3 Year Growth-FY'] / 3
    df['FCF_Growth_5Yr_Avg'] = df['Free Cash Flow 5 Year Growth-FY'] / 5

    df['FCF_Growth_1Yr/3Yr'] = df['FCF_Growth_1Yr_Avg'] / df['FCF_Growth_3Yr_Avg']
    df['FCF_Growth_1Yr/5Yr'] = df['FCF_Growth_1Yr_Avg'] / df['FCF_Growth_5Yr_Avg']

    return df[['FCF_Growth_1Yr_Avg','FCF_Growth_3Yr_Avg','FCF_Growth_5Yr_Avg','FCF_Growth_1Yr/3Yr','FCF_Growth_1Yr/5Yr']]

def debt_equity_features(df):
    years = ['2020-12-31','2021-12-31','2022-12-31','2023-12-31','2024-12-31']
    for y in years:
        col = f'Total Debt To Equity Ratio-FY_{y}'
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df['Debt/Equity_1Yr_Avg'] = df['Total Debt To Equity Ratio-FY_2024-12-31']
    df['Debt/Equity_3Yr_Avg'] = df[['Total Debt To Equity Ratio-FY_2022-12-31',
                                   'Total Debt To Equity Ratio-FY_2023-12-31',
                                   'Total Debt To Equity Ratio-FY_2024-12-31']].mean(axis=1)
    df['Debt/Equity_5Yr_Avg'] = df[[f'Total Debt To Equity Ratio-FY_{y}' for y in years]].mean(axis=1)
    
    
    df['Debt/Equity_1Yr/3Yr'] = df['Debt/Equity_1Yr_Avg'] / df['Debt/Equity_3Yr_Avg']
    df['Debt/Equity_1Yr/5Yr'] = df['Debt/Equity_1Yr_Avg'] / df['Debt/Equity_5Yr_Avg']
    
    return df[['Debt/Equity_1Yr_Avg','Debt/Equity_3Yr_Avg','Debt/Equity_5Yr_Avg','Debt/Equity_1Yr/3Yr','Debt/Equity_1Yr/5Yr']]

def dividend_per_share_features(df):
    df['Dividend Per Share 1 Year Growth-FY'] = pd.to_numeric(df['Dividend Per Share 1 Year Growth-FY'], errors='coerce')
    df['Dividend Per Share 3 Year Growth-FY'] = pd.to_numeric(df['Dividend Per Share 3 Year Growth-FY'], errors='coerce')
    df['Dividend Per Share 5 Year Growth-FY'] = pd.to_numeric(df['Dividend Per Share 5 Year Growth-FY'], errors='coerce')
    
    df['DividendPerShare_1Yr_Avg'] = df['Dividend Per Share 1 Year Growth-FY']
    df['DividendPerShare_3Yr_Avg'] = df['Dividend Per Share 3 Year Growth-FY'] / 3
    df['DividendPerShare_5Yr_Avg'] = df['Dividend Per Share 5 Year Growth-FY'] / 5
    
    df['DividendPerShare_1Yr/3Yr'] = df['DividendPerShare_1Yr_Avg'] / df['DividendPerShare_3Yr_Avg']
    df['DividendPerShare_1Yr/5Yr'] = df['DividendPerShare_1Yr_Avg'] / df['DividendPerShare_5Yr_Avg']
    
    return df[['DividendPerShare_1Yr_Avg','DividendPerShare_3Yr_Avg','DividendPerShare_5Yr_Avg','DividendPerShare_1Yr/3Yr','DividendPerShare_1Yr/5Yr']]

financial_ratios = df[['Forward Dividend Yield', 
                       'Dividend Pay Out Ratio-TTM', 
                       'P/E Ratio (TTM) (Long)', 
                       'Price To Earnings Ratio 5 Year Average', 
                       'Forward Price To Earnings Ratio', 
                       'Price Earnings To Growth Ratio']]
def price_to_sales_features(df):
    df['Price To Sales Ratio'] = pd.to_numeric(
        df['Price To Sales Ratio'], errors='coerce'
    )
    df['Price To Sales Ratio 5 Year Average'] = pd.to_numeric(
        df['Price To Sales Ratio 5 Year Average'], errors='coerce'
    )

    df['PS/PS_5Yr'] = (
        df['Price To Sales Ratio'] /
        df['Price To Sales Ratio 5 Year Average']
    )

    return df[['Price To Sales Ratio',
               'Price To Sales Ratio 5 Year Average',
               'PS/PS_5Yr']]

def price_to_book_features(df):
    df['Price To Book Ratio'] = pd.to_numeric(
        df['Price To Book Ratio'], errors='coerce'
    )
    df['Price To Book Ratio 5 Year Average'] = pd.to_numeric(
        df['Price To Book Ratio 5 Year Average'], errors='coerce'
    )

    df['PB/PB_5Yr'] = (
        df['Price To Book Ratio'] /
        df['Price To Book Ratio 5 Year Average']
    )

    return df[['Price To Book Ratio',
               'Price To Book Ratio 5 Year Average',
               'PB/PB_5Yr']]

def price_to_cash_flow_features(df):
    df['Price To Cash Flow Ratio'] = pd.to_numeric(
        df['Price To Cash Flow Ratio'], errors='coerce'
    )
    df['Price To Cash Flow Ratio 5 Year Average'] = pd.to_numeric(
        df['Price To Cash Flow Ratio 5 Year Average'], errors='coerce'
    )

    df['PCF/PCF_5Yr'] = (
        df['Price To Cash Flow Ratio'] /
        df['Price To Cash Flow Ratio 5 Year Average']
    )

    return df[['Price To Cash Flow Ratio',
               'Price To Cash Flow Ratio 5 Year Average',
               'PCF/PCF_5Yr']]

def price_to_free_cash_flow_features(df):
    df['Price To Free Cash Flow Ratio'] = pd.to_numeric(
        df['Price To Free Cash Flow Ratio'], errors='coerce'
    )
    df['Price To Free Cash Flow Ratio 3 Year Average'] = pd.to_numeric(
        df['Price To Free Cash Flow Ratio 3 Year Average'], errors='coerce'
    )

    df['PFCF/PFCF_3Yr'] = (
        df['Price To Free Cash Flow Ratio'] /
        df['Price To Free Cash Flow Ratio 3 Year Average']
    )

    return df[['Price To Free Cash Flow Ratio',
               'Price To Free Cash Flow Ratio 3 Year Average',
               'PFCF/PFCF_3Yr']]
ev_features = df[['Enterprise Value To EBIT Ratio',
                  'Enterprise Value To EBITDA Ratio']]

def days_sales_ratio_features(df):
    dsr_2021 = [
        'Days in Sales Ratio-TTM_2021-03-31',
        'Days in Sales Ratio-TTM_2021-06-30',
        'Days in Sales Ratio-TTM_2021-09-30',
        'Days in Sales Ratio-TTM_2021-12-31'
    ]

    dsr_2022 = [
        'Days in Sales Ratio-TTM_2022-03-31',
        'Days in Sales Ratio-TTM_2022-06-30',
        'Days in Sales Ratio-TTM_2022-09-30',
        'Days in Sales Ratio-TTM_2022-12-31'
    ]

    dsr_2023 = [
        'Days in Sales Ratio-TTM_2023-03-31',
        'Days in Sales Ratio-TTM_2023-06-30',
        'Days in Sales Ratio-TTM_2023-09-30',
        'Days in Sales Ratio-TTM_2023-12-31'
    ]

    dsr_2024 = [
        'Days in Sales Ratio-TTM_2024-03-31',
        'Days in Sales Ratio-TTM_2024-06-30',
        'Days in Sales Ratio-TTM_2024-09-30',
        'Days in Sales Ratio-TTM_2024-12-31'
    ]

    dsr_2025 = [
        'Days in Sales Ratio-TTM_2025-03-31',
        'Days in Sales Ratio-TTM_2025-06-30',
        'Days in Sales Ratio-TTM_2025-09-30' 
    ]

    for cols in [dsr_2021, dsr_2022, dsr_2023, dsr_2024, dsr_2025]:
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

    df['DSR_2021_Avg'] = df[dsr_2021].mean(axis=1)
    df['DSR_2022_Avg'] = df[dsr_2022].mean(axis=1)
    df['DSR_2023_Avg'] = df[dsr_2023].mean(axis=1)
    df['DSR_2024_Avg'] = df[dsr_2024].mean(axis=1)
    df['DSR_2025_Avg'] = df[dsr_2025].mean(axis=1)

    
    df['Days_Sales_Ratio_1Yr_Avg'] = df['DSR_2025_Avg']
    df['Days_Sales_Ratio_3Yr_Avg'] = (
        df[['DSR_2023_Avg', 'DSR_2024_Avg', 'DSR_2025_Avg']].sum(axis=1) / 3
    )
    df['Days_Sales_Ratio_5Yr_Avg'] = (
        df[['DSR_2021_Avg', 'DSR_2022_Avg', 'DSR_2023_Avg',
            'DSR_2024_Avg', 'DSR_2025_Avg']].sum(axis=1) / 5
    )

    df['Days_Sales_Ratio_1Yr/3Yr'] = df['Days_Sales_Ratio_1Yr_Avg'] / df['Days_Sales_Ratio_3Yr_Avg']
    df['Days_Sales_Ratio_1Yr/5Yr'] = df['Days_Sales_Ratio_1Yr_Avg'] / df['Days_Sales_Ratio_5Yr_Avg']

    return df[['Days_Sales_Ratio_1Yr_Avg', 'Days_Sales_Ratio_3Yr_Avg', 'Days_Sales_Ratio_5Yr_Avg',
               'Days_Sales_Ratio_1Yr/3Yr', 'Days_Sales_Ratio_1Yr/5Yr']]
def debt_to_capital_features(df):

    dtc_2021 = [c for c in df.columns if 'Debt to Capital % (trailing) (Long)_2021' in c]
    dtc_2022 = [c for c in df.columns if 'Debt to Capital % (trailing) (Long)_2022' in c]
    dtc_2023 = [c for c in df.columns if 'Debt to Capital % (trailing) (Long)_2023' in c]
    dtc_2024 = [c for c in df.columns if 'Debt to Capital % (trailing) (Long)_2024' in c]
    dtc_2025 = [c for c in df.columns if 'Debt to Capital % (trailing) (Long)_2025' in c]

    for cols in [dtc_2021, dtc_2022, dtc_2023, dtc_2024, dtc_2025]:
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

    df['Debt_To_Capital_2021_Avg'] = df[dtc_2021].mean(axis=1)
    df['Debt_To_Capital_2022_Avg'] = df[dtc_2022].mean(axis=1)
    df['Debt_To_Capital_2023_Avg'] = df[dtc_2023].mean(axis=1)
    df['Debt_To_Capital_2024_Avg'] = df[dtc_2024].mean(axis=1)
    df['Debt_To_Capital_2025_Avg'] = df[dtc_2025].mean(axis=1)

    df['Debt_To_Capital_1Yr_Avg'] = df['Debt_To_Capital_2025_Avg']

    df['Debt_To_Capital_3Yr_Avg'] = (
        df[['Debt_To_Capital_2023_Avg', 'Debt_To_Capital_2024_Avg', 'Debt_To_Capital_2025_Avg']]
        .mean(axis=1)
    )

    df['Debt_To_Capital_5Yr_Avg'] = (
        df[['Debt_To_Capital_2021_Avg', 'Debt_To_Capital_2022_Avg', 'Debt_To_Capital_2023_Avg',
            'Debt_To_Capital_2024_Avg', 'Debt_To_Capital_2025_Avg']]
        .mean(axis=1)
    )

    df['Debt_To_Capital_1Yr/3Yr'] = df['Debt_To_Capital_1Yr_Avg'] / df['Debt_To_Capital_3Yr_Avg']
    df['Debt_To_Capital_1Yr/5Yr'] = df['Debt_To_Capital_1Yr_Avg'] / df['Debt_To_Capital_5Yr_Avg']

    return df[
        ['Debt_To_Capital_1Yr_Avg', 'Debt_To_Capital_3Yr_Avg', 'Debt_To_Capital_5Yr_Avg',
         'Debt_To_Capital_1Yr/3Yr', 'Debt_To_Capital_1Yr/5Yr']
    ]
def current_ratio_features(df):

    cr_2021 = [c for c in df.columns if 'Current Ratio-FQ_2021' in c]
    cr_2022 = [c for c in df.columns if 'Current Ratio-FQ_2022' in c]
    cr_2023 = [c for c in df.columns if 'Current Ratio-FQ_2023' in c]
    cr_2024 = [c for c in df.columns if 'Current Ratio-FQ_2024' in c]
    cr_2025 = [c for c in df.columns if 'Current Ratio-FQ_2025' in c]

    for cols in [cr_2021, cr_2022, cr_2023, cr_2024, cr_2025]:
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

    df['CurrentRatio_2021_Avg'] = df[cr_2021].mean(axis=1)
    df['CurrentRatio_2022_Avg'] = df[cr_2022].mean(axis=1)
    df['CurrentRatio_2023_Avg'] = df[cr_2023].mean(axis=1)
    df['CurrentRatio_2024_Avg'] = df[cr_2024].mean(axis=1)
    df['CurrentRatio_2025_Avg'] = df[cr_2025].mean(axis=1)

    df['CurrentRatio_1Yr_Avg'] = df['CurrentRatio_2025_Avg']

    df['CurrentRatio_3Yr_Avg'] = (
        df[['CurrentRatio_2023_Avg',
            'CurrentRatio_2024_Avg',
            'CurrentRatio_2025_Avg']]
        .mean(axis=1)
    )

    df['CurrentRatio_5Yr_Avg'] = (
        df[['CurrentRatio_2021_Avg',
            'CurrentRatio_2022_Avg',
            'CurrentRatio_2023_Avg',
            'CurrentRatio_2024_Avg',
            'CurrentRatio_2025_Avg']]
        .mean(axis=1)
    )

    df['CurrentRatio_1Yr/3Yr'] = df['CurrentRatio_1Yr_Avg'] / df['CurrentRatio_3Yr_Avg']
    df['CurrentRatio_1Yr/5Yr'] = df['CurrentRatio_1Yr_Avg'] / df['CurrentRatio_5Yr_Avg']

    return df[
        ['CurrentRatio_1Yr_Avg', 'CurrentRatio_3Yr_Avg', 'CurrentRatio_5Yr_Avg',
         'CurrentRatio_1Yr/3Yr', 'CurrentRatio_1Yr/5Yr']
    ]
def net_debt_to_ebitda_features(df):

    nd_2021 = [c for c in df.columns if 'Net Debt To Ebitda Ratio-TTM_2021' in c]
    nd_2022 = [c for c in df.columns if 'Net Debt To Ebitda Ratio-TTM_2022' in c]
    nd_2023 = [c for c in df.columns if 'Net Debt To Ebitda Ratio-TTM_2023' in c]
    nd_2024 = [c for c in df.columns if 'Net Debt To Ebitda Ratio-TTM_2024' in c]
    nd_2025 = [c for c in df.columns if 'Net Debt To Ebitda Ratio-TTM_2025' in c]

    for cols in [nd_2021, nd_2022, nd_2023, nd_2024, nd_2025]:
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

    df['NetDebtToEBITDA_2021_Avg'] = df[nd_2021].mean(axis=1)
    df['NetDebtToEBITDA_2022_Avg'] = df[nd_2022].mean(axis=1)
    df['NetDebtToEBITDA_2023_Avg'] = df[nd_2023].mean(axis=1)
    df['NetDebtToEBITDA_2024_Avg'] = df[nd_2024].mean(axis=1)
    df['NetDebtToEBITDA_2025_Avg'] = df[nd_2025].mean(axis=1)

    df['NetDebtToEBITDA_1Yr_Avg'] = df['NetDebtToEBITDA_2025_Avg']

    df['NetDebtToEBITDA_3Yr_Avg'] = (
        df[['NetDebtToEBITDA_2023_Avg',
            'NetDebtToEBITDA_2024_Avg',
            'NetDebtToEBITDA_2025_Avg']]
        .mean(axis=1)
    )

    df['NetDebtToEBITDA_5Yr_Avg'] = (
        df[['NetDebtToEBITDA_2021_Avg',
            'NetDebtToEBITDA_2022_Avg',
            'NetDebtToEBITDA_2023_Avg',
            'NetDebtToEBITDA_2024_Avg',
            'NetDebtToEBITDA_2025_Avg']]
        .mean(axis=1)
    )

    
    df['NetDebtToEBITDA_1Yr/3Yr'] = df['NetDebtToEBITDA_1Yr_Avg'] / df['NetDebtToEBITDA_3Yr_Avg']
    df['NetDebtToEBITDA_1Yr/5Yr'] = df['NetDebtToEBITDA_1Yr_Avg'] / df['NetDebtToEBITDA_5Yr_Avg']

    return df[
        ['NetDebtToEBITDA_1Yr_Avg',
         'NetDebtToEBITDA_3Yr_Avg',
         'NetDebtToEBITDA_5Yr_Avg',
         'NetDebtToEBITDA_1Yr/3Yr',
         'NetDebtToEBITDA_1Yr/5Yr']
    ]
def eps_features_continous(df):
    eps_2021 = [
        'Basic Eps From Continuing Operations Value-FQ_2021-03-31',
        'Basic Eps From Continuing Operations Value-FQ_2021-06-30',
        'Basic Eps From Continuing Operations Value-FQ_2021-09-30',
        'Basic Eps From Continuing Operations Value-FQ_2021-12-31'
    ]

    eps_2022 = [
        'Basic Eps From Continuing Operations Value-FQ_2022-03-31',
        'Basic Eps From Continuing Operations Value-FQ_2022-06-30',
        'Basic Eps From Continuing Operations Value-FQ_2022-09-30',
        'Basic Eps From Continuing Operations Value-FQ_2022-12-31'
    ]

    eps_2023 = [
        'Basic Eps From Continuing Operations Value-FQ_2023-03-31',
        'Basic Eps From Continuing Operations Value-FQ_2023-06-30',
        'Basic Eps From Continuing Operations Value-FQ_2023-09-30',
        'Basic Eps From Continuing Operations Value-FQ_2023-12-31'
    ]

    eps_2024 = [
        'Basic Eps From Continuing Operations Value-FQ_2024-03-31',
        'Basic Eps From Continuing Operations Value-FQ_2024-06-30',
        'Basic Eps From Continuing Operations Value-FQ_2024-09-30',
        'Basic Eps From Continuing Operations Value-FQ_2024-12-31'
    ]

    eps_2025 = [
        'Basic Eps From Continuing Operations Value-FQ_2025-03-31',
        'Basic Eps From Continuing Operations Value-FQ_2025-06-30',
        'Basic Eps From Continuing Operations Value-FQ_2025-09-30' 
    ]

    for cols in [eps_2021, eps_2022, eps_2023, eps_2024, eps_2025]:
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

    df['EPS_2021_Avg'] = df[eps_2021].mean(axis=1)
    df['EPS_2022_Avg'] = df[eps_2022].mean(axis=1)
    df['EPS_2023_Avg'] = df[eps_2023].mean(axis=1)
    df['EPS_2024_Avg'] = df[eps_2024].mean(axis=1)
    df['EPS_2025_Avg'] = df[eps_2025].mean(axis=1)

    
    df['EPS_1Yr_Avg_Cont.'] = df['EPS_2025_Avg']
    df['EPS_3Yr_Avg_Cont.'] = df[['EPS_2023_Avg', 'EPS_2024_Avg', 'EPS_2025_Avg']].mean(axis=1)
    df['EPS_5Yr_Avg_Cont.'] = df[['EPS_2021_Avg', 'EPS_2022_Avg', 'EPS_2023_Avg', 'EPS_2024_Avg', 'EPS_2025_Avg']].mean(axis=1)

    df['EPS_1Yr/3Yr_Cont.'] = df['EPS_1Yr_Avg_Cont.'] / df['EPS_3Yr_Avg_Cont.']
    df['EPS_1Yr/5Yr_Cont.'] = df['EPS_1Yr_Avg_Cont.'] / df['EPS_5Yr_Avg_Cont.']

    return df[['EPS_1Yr_Avg_Cont.','EPS_3Yr_Avg_Cont.','EPS_5Yr_Avg_Cont.','EPS_1Yr/3Yr_Cont.','EPS_1Yr/5Yr_Cont.']]

def basic_eps_features(df):
    eps_2021 = [
        'Basic Eps Value-FQ_2021-03-31',
        'Basic Eps Value-FQ_2021-06-30',
        'Basic Eps Value-FQ_2021-09-30',
        'Basic Eps Value-FQ_2021-12-31'
    ]
    eps_2022 = [
        'Basic Eps Value-FQ_2022-03-31',
        'Basic Eps Value-FQ_2022-06-30',
        'Basic Eps Value-FQ_2022-09-30',
        'Basic Eps Value-FQ_2022-12-31'
    ]
    eps_2023 = [
        'Basic Eps Value-FQ_2023-03-31',
        'Basic Eps Value-FQ_2023-06-30',
        'Basic Eps Value-FQ_2023-09-30',
        'Basic Eps Value-FQ_2023-12-31'
    ]
    eps_2024 = [
        'Basic Eps Value-FQ_2024-03-31',
        'Basic Eps Value-FQ_2024-06-30',
        'Basic Eps Value-FQ_2024-09-30',
        'Basic Eps Value-FQ_2024-12-31'
    ]
    eps_2025 = [
        'Basic Eps Value-FQ_2025-03-31',
        'Basic Eps Value-FQ_2025-06-30',
        'Basic Eps Value-FQ_2025-09-30'  
    ]
    
    
    for cols in [eps_2021, eps_2022, eps_2023, eps_2024, eps_2025]:
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
    
    
    df['EPS_2021_Avg'] = df[eps_2021].mean(axis=1)
    df['EPS_2022_Avg'] = df[eps_2022].mean(axis=1)
    df['EPS_2023_Avg'] = df[eps_2023].mean(axis=1)
    df['EPS_2024_Avg'] = df[eps_2024].mean(axis=1)
    df['EPS_2025_Avg'] = df[eps_2025].mean(axis=1)
    
    
    df['EPS_1Yr_Avg'] = df['EPS_2025_Avg']
    df['EPS_3Yr_Avg'] = df[['EPS_2023_Avg','EPS_2024_Avg','EPS_2025_Avg']].mean(axis=1)
    df['EPS_5Yr_Avg'] = df[['EPS_2021_Avg','EPS_2022_Avg','EPS_2023_Avg','EPS_2024_Avg','EPS_2025_Avg']].mean(axis=1)
    
   
    df['EPS_1Yr/3Yr'] = df['EPS_1Yr_Avg'] / df['EPS_3Yr_Avg']
    df['EPS_1Yr/5Yr'] = df['EPS_1Yr_Avg'] / df['EPS_5Yr_Avg']
    
    
    df.rename(columns={
        'EPS_1Yr_Avg': 'Basic_EPS_1Yr_Avg',
        'EPS_3Yr_Avg': 'Basic_EPS_3Yr_Avg',
        'EPS_5Yr_Avg': 'Basic_EPS_5Yr_Avg',
        'EPS_1Yr/3Yr': 'Basic_EPS_1Yr/3Yr',
        'EPS_1Yr/5Yr': 'Basic_EPS_1Yr/5Yr'
    }, inplace=True)
    
    return df[['Basic_EPS_1Yr_Avg','Basic_EPS_3Yr_Avg','Basic_EPS_5Yr_Avg',
               'Basic_EPS_1Yr/3Yr','Basic_EPS_1Yr/5Yr']]
def pb_ratio_features(df):
   
    pb_2021 = [c for c in df.columns if 'P/B Ratio (TTM) (Long)_2021' in c]
    pb_2022 = [c for c in df.columns if 'P/B Ratio (TTM) (Long)_2022' in c]
    pb_2023 = [c for c in df.columns if 'P/B Ratio (TTM) (Long)_2023' in c]
    pb_2024 = [c for c in df.columns if 'P/B Ratio (TTM) (Long)_2024' in c]
    pb_2025 = [c for c in df.columns if 'P/B Ratio (TTM) (Long)_2025' in c]

   
    for cols in [pb_2021, pb_2022, pb_2023, pb_2024, pb_2025]:
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

   
    df['PB_2021_Avg'] = df[pb_2021].mean(axis=1)
    df['PB_2022_Avg'] = df[pb_2022].mean(axis=1)
    df['PB_2023_Avg'] = df[pb_2023].mean(axis=1)
    df['PB_2024_Avg'] = df[pb_2024].mean(axis=1)
    df['PB_2025_Avg'] = df[pb_2025].mean(axis=1)

    df['P/B_1Yr_Avg'] = df['PB_2025_Avg']
    df['P/B_3Yr_Avg'] = df[['PB_2023_Avg', 'PB_2024_Avg', 'PB_2025_Avg']].mean(axis=1)
    df['P/B_5Yr_Avg'] = df[['PB_2021_Avg', 'PB_2022_Avg', 'PB_2023_Avg', 'PB_2024_Avg', 'PB_2025_Avg']].mean(axis=1)

 
    df['P/B_1Yr/3Yr'] = df['P/B_1Yr_Avg'] / df['P/B_3Yr_Avg']
    df['P/B_1Yr/5Yr'] = df['P/B_1Yr_Avg'] / df['P/B_5Yr_Avg']

    return df[['P/B_1Yr_Avg', 'P/B_3Yr_Avg', 'P/B_5Yr_Avg', 'P/B_1Yr/3Yr', 'P/B_1Yr/5Yr']]
def pe_ratio_features(df):
    pe_2021 = [c for c in df.columns if c.startswith('P/E Ratio (TTM) (Long)_2021')]
    pe_2022 = [c for c in df.columns if c.startswith('P/E Ratio (TTM) (Long)_2022')]
    pe_2023 = [c for c in df.columns if c.startswith('P/E Ratio (TTM) (Long)_2023')]
    pe_2024 = [c for c in df.columns if c.startswith('P/E Ratio (TTM) (Long)_2024')]
    pe_2025 = [c for c in df.columns if c.startswith('P/E Ratio (TTM) (Long)_2025')]

    for cols in [pe_2021, pe_2022, pe_2023, pe_2024, pe_2025]:
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

    df['PE_2021_Avg'] = df[pe_2021].mean(axis=1)
    df['PE_2022_Avg'] = df[pe_2022].mean(axis=1)
    df['PE_2023_Avg'] = df[pe_2023].mean(axis=1)
    df['PE_2024_Avg'] = df[pe_2024].mean(axis=1)
    df['PE_2025_Avg'] = df[pe_2025].mean(axis=1)

    df['P/E_1Yr_Avg'] = df['PE_2025_Avg']
    df['P/E_3Yr_Avg'] = df[['PE_2023_Avg', 'PE_2024_Avg', 'PE_2025_Avg']].mean(axis=1)
    df['P/E_5Yr_Avg'] = df[['PE_2021_Avg', 'PE_2022_Avg', 'PE_2023_Avg', 'PE_2024_Avg', 'PE_2025_Avg']].mean(axis=1)

    df['P/E_1Yr/3Yr'] = df['P/E_1Yr_Avg'] / df['P/E_3Yr_Avg']
    df['P/E_1Yr/5Yr'] = df['P/E_1Yr_Avg'] / df['P/E_5Yr_Avg']

    return df[['P/E_1Yr_Avg', 'P/E_3Yr_Avg', 'P/E_5Yr_Avg', 'P/E_1Yr/3Yr', 'P/E_1Yr/5Yr']]
def forward_div_yield_features(df):
    fdy_2021 = [c for c in df.columns if c.startswith('Forward Dividend Yield_2021')]
    fdy_2022 = [c for c in df.columns if c.startswith('Forward Dividend Yield_2022')]
    fdy_2023 = [c for c in df.columns if c.startswith('Forward Dividend Yield_2023')]
    fdy_2024 = [c for c in df.columns if c.startswith('Forward Dividend Yield_2024')]
    fdy_2025 = [c for c in df.columns if c.startswith('Forward Dividend Yield_2025')]

    for cols in [fdy_2021, fdy_2022, fdy_2023, fdy_2024, fdy_2025]:
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

    df['FDY_2021_Avg'] = df[fdy_2021].mean(axis=1)
    df['FDY_2022_Avg'] = df[fdy_2022].mean(axis=1)
    df['FDY_2023_Avg'] = df[fdy_2023].mean(axis=1)
    df['FDY_2024_Avg'] = df[fdy_2024].mean(axis=1)
    df['FDY_2025_Avg'] = df[fdy_2025].mean(axis=1)

    df['Forward_Div_Yield_1Yr_Avg'] = df['FDY_2025_Avg']
    df['Forward_Div_Yield_3Yr_Avg'] = df[['FDY_2023_Avg', 'FDY_2024_Avg', 'FDY_2025_Avg']].mean(axis=1)
    df['Forward_Div_Yield_5Yr_Avg'] = df[['FDY_2021_Avg', 'FDY_2022_Avg', 'FDY_2023_Avg', 'FDY_2024_Avg', 'FDY_2025_Avg']].mean(axis=1)

    
    df['Forward_Div_Yield_1Yr/3Yr'] = df['Forward_Div_Yield_1Yr_Avg'] / df['Forward_Div_Yield_3Yr_Avg']
    df['Forward_Div_Yield_1Yr/5Yr'] = df['Forward_Div_Yield_1Yr_Avg'] / df['Forward_Div_Yield_5Yr_Avg']

    return df[['Forward_Div_Yield_1Yr_Avg', 'Forward_Div_Yield_3Yr_Avg', 'Forward_Div_Yield_5Yr_Avg', 'Forward_Div_Yield_1Yr/3Yr', 'Forward_Div_Yield_1Yr/5Yr']]

def capex_to_sales_features(df):
    capex_2021 = [
        'Capital Expenditure To Sales Ratio-TTM_2021-03-31',
        'Capital Expenditure To Sales Ratio-TTM_2021-06-30',
        'Capital Expenditure To Sales Ratio-TTM_2021-09-30',
        'Capital Expenditure To Sales Ratio-TTM_2021-12-31'
    ]
    capex_2022 = [
        'Capital Expenditure To Sales Ratio-TTM_2022-03-31',
        'Capital Expenditure To Sales Ratio-TTM_2022-06-30',
        'Capital Expenditure To Sales Ratio-TTM_2022-09-30',
        'Capital Expenditure To Sales Ratio-TTM_2022-12-31'
    ]
    capex_2023 = [
        'Capital Expenditure To Sales Ratio-TTM_2023-03-31',
        'Capital Expenditure To Sales Ratio-TTM_2023-06-30',
        'Capital Expenditure To Sales Ratio-TTM_2023-09-30',
        'Capital Expenditure To Sales Ratio-TTM_2023-12-31'
    ]
    capex_2024 = [
        'Capital Expenditure To Sales Ratio-TTM_2024-03-31',
        'Capital Expenditure To Sales Ratio-TTM_2024-06-30',
        'Capital Expenditure To Sales Ratio-TTM_2024-09-30',
        'Capital Expenditure To Sales Ratio-TTM_2024-12-31'
    ]
    capex_2025 = [
        'Capital Expenditure To Sales Ratio-TTM_2025-03-31',
        'Capital Expenditure To Sales Ratio-TTM_2025-06-30',
        'Capital Expenditure To Sales Ratio-TTM_2025-09-30'  
    ]

    
    for cols in [capex_2021, capex_2022, capex_2023, capex_2024, capex_2025]:
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

    df['CapEx_2021_Avg'] = df[capex_2021].mean(axis=1)
    df['CapEx_2022_Avg'] = df[capex_2022].mean(axis=1)
    df['CapEx_2023_Avg'] = df[capex_2023].mean(axis=1)
    df['CapEx_2024_Avg'] = df[capex_2024].mean(axis=1)
    df['CapEx_2025_Avg'] = df[capex_2025].mean(axis=1)

    df['CapEx_1Yr_Avg'] = df['CapEx_2025_Avg']
    df['CapEx_3Yr_Avg'] = df[['CapEx_2023_Avg', 'CapEx_2024_Avg', 'CapEx_2025_Avg']].mean(axis=1)
    df['CapEx_5Yr_Avg'] = df[['CapEx_2021_Avg', 'CapEx_2022_Avg', 'CapEx_2023_Avg',
                               'CapEx_2024_Avg', 'CapEx_2025_Avg']].mean(axis=1)

    
    df['CapEx_1Yr/3Yr'] = df['CapEx_1Yr_Avg'] / df['CapEx_3Yr_Avg']
    df['CapEx_1Yr/5Yr'] = df['CapEx_1Yr_Avg'] / df['CapEx_5Yr_Avg']

    return df[['CapEx_1Yr_Avg', 'CapEx_3Yr_Avg', 'CapEx_5Yr_Avg',
               'CapEx_1Yr/3Yr', 'CapEx_1Yr/5Yr']]
def net_debt_issuance_features(df):
    debt_2021 = [
        'Issuance Of Repayments For Debt Net Value-FQ_2021-03-31',
        'Issuance Of Repayments For Debt Net Value-FQ_2021-06-30',
        'Issuance Of Repayments For Debt Net Value-FQ_2021-09-30',
        'Issuance Of Repayments For Debt Net Value-FQ_2021-12-31'
    ]
    debt_2022 = [
        'Issuance Of Repayments For Debt Net Value-FQ_2022-03-31',
        'Issuance Of Repayments For Debt Net Value-FQ_2022-06-30',
        'Issuance Of Repayments For Debt Net Value-FQ_2022-09-30',
        'Issuance Of Repayments For Debt Net Value-FQ_2022-12-31'
    ]
    debt_2023 = [
        'Issuance Of Repayments For Debt Net Value-FQ_2023-03-31',
        'Issuance Of Repayments For Debt Net Value-FQ_2023-06-30',
        'Issuance Of Repayments For Debt Net Value-FQ_2023-09-30',
        'Issuance Of Repayments For Debt Net Value-FQ_2023-12-31'
    ]
    debt_2024 = [
        'Issuance Of Repayments For Debt Net Value-FQ_2024-03-31',
        'Issuance Of Repayments For Debt Net Value-FQ_2024-06-30',
        'Issuance Of Repayments For Debt Net Value-FQ_2024-09-30',
        'Issuance Of Repayments For Debt Net Value-FQ_2024-12-31'
    ]
    debt_2025 = [
        'Issuance Of Repayments For Debt Net Value-FQ_2025-03-31',
        'Issuance Of Repayments For Debt Net Value-FQ_2025-06-30',
        'Issuance Of Repayments For Debt Net Value-FQ_2025-09-30'  
    ]

   
    for cols in [debt_2021, debt_2022, debt_2023, debt_2024, debt_2025]:
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

    df['DebtNet_2021_Avg'] = df[debt_2021].mean(axis=1)
    df['DebtNet_2022_Avg'] = df[debt_2022].mean(axis=1)
    df['DebtNet_2023_Avg'] = df[debt_2023].mean(axis=1)
    df['DebtNet_2024_Avg'] = df[debt_2024].mean(axis=1)
    df['DebtNet_2025_Avg'] = df[debt_2025].mean(axis=1)

    df['Issuance_Repayments_Debt_Net_1Yr_Avg'] = df['DebtNet_2025_Avg']
    df['Issuance_Repayments_Debt_Net_3Yr_Avg'] = df[['DebtNet_2023_Avg', 'DebtNet_2024_Avg', 'DebtNet_2025_Avg']].mean(axis=1)
    df['Issuance_Repayments_Debt_Net_5Yr_Avg'] = df[['DebtNet_2021_Avg', 'DebtNet_2022_Avg', 'DebtNet_2023_Avg',
                                'DebtNet_2024_Avg', 'DebtNet_2025_Avg']].mean(axis=1)

    
    df['Issuance_Repayments_Debt_Net_1Yr/3Yr'] = df['Issuance_Repayments_Debt_Net_1Yr_Avg'] / df['Issuance_Repayments_Debt_Net_3Yr_Avg']
    df['Issuance_Repayments_Debt_Net_1Yr/5Yr'] = df['Issuance_Repayments_Debt_Net_1Yr_Avg'] / df['Issuance_Repayments_Debt_Net_5Yr_Avg']

    return df[['Issuance_Repayments_Debt_Net_1Yr_Avg', 'Issuance_Repayments_Debt_Net_3Yr_Avg', 'Issuance_Repayments_Debt_Net_5Yr_Avg',
               'Issuance_Repayments_Debt_Net_1Yr/3Yr', 'Issuance_Repayments_Debt_Net_1Yr/5Yr']]



net_issuance_data = net_debt_issuance_features(df)
capex_data=capex_to_sales_features(df)
fdy_data = forward_div_yield_features(df)
pe_data_=pe_ratio_features(df)
pb_trend_data = pb_ratio_features(df)
basic_eps_data = basic_eps_features(df)
eps_data_continous = eps_features_continous(df)
net_debt_ebitda_data = net_debt_to_ebitda_features(df)
current_ratio_data = current_ratio_features(df)
debt_to_capital_data = debt_to_capital_features(df)
dsr_data = days_sales_ratio_features(df)
pfcf_data = price_to_free_cash_flow_features(df)
pcf_data = price_to_cash_flow_features(df)
pb_valuation_data = price_to_book_features(df)

ps_data = price_to_sales_features(df)
dividend_ps_data = dividend_per_share_features(df)
debt_equity_data = debt_equity_features(df)
cash_return = df[['Cash Return']]

fcf_growth_data = fcf_growth_features(df)
fcf_sales_data = fcf_sales_features(df)
roa_data = roa_features(df)
roe_data = roe_features(df)
roic_data = roic_features(df)
net_profit_data = net_profit_margin_features(df)
ebit_data = ebit_margin_features(df)
ebitda_data = ebitda_margin_features(df)
revenue_data = revenue_features(df)
gross_margin_data = gross_margin_features(df)
operating_margin_data = operating_margin_features(df)

input_features = pd.concat([general_features, moat_features, rating_features, 
                            price_features, momentum_features, returns_features, 
                            revenue_data, gross_margin_data, operating_margin_data, net_profit_data, ebit_data, ebitda_data, 
                            roa_data, roe_data, roic_data, fcf_sales_data, fcf_growth_data, 
                            cash_return, debt_equity_data, dividend_ps_data, financial_ratios,ps_data, pb_valuation_data,
                            pcf_data, pfcf_data, ev_features, dsr_data, debt_to_capital_data, current_ratio_data,
                            net_debt_ebitda_data, eps_data_continous, basic_eps_data, pb_trend_data, pe_data_,
                              fdy_data, capex_data, net_issuance_data], axis=1)


pd.set_option('display.max_columns', None)


experimental_df = pd.concat([
    rating_features, price_features, momentum_features, returns_features,
    revenue_data, gross_margin_data, operating_margin_data, net_profit_data,
    ebit_data, ebitda_data, roa_data, roe_data, roic_data, fcf_sales_data, fcf_growth_data,
    cash_return, debt_equity_data, dividend_ps_data, financial_ratios, ps_data, pb_valuation_data,
    pcf_data, pfcf_data, ev_features, dsr_data, debt_to_capital_data, current_ratio_data,
    net_debt_ebitda_data, eps_data_continous, basic_eps_data, pb_trend_data, pe_data_,
    fdy_data, capex_data, net_issuance_data
], axis=1)

experimental_df.replace(['-', '—', '', 'N/A', 'na', 'NaN'], np.nan, inplace=True)
input_features.replace(['-', '—', '', 'N/A', 'na', 'NaN'], np.nan, inplace=True)

experimental_df = experimental_df.apply(pd.to_numeric, errors='coerce')

experimental_df = experimental_df.loc[:, ~experimental_df.columns.duplicated()]
experimental_df = experimental_df.dropna(axis=1, how='all')
threshold = 0.5

columns_before = set(experimental_df.columns)

experimental_df = experimental_df.loc[:, experimental_df.isna().mean() < threshold]

columns_after = set(experimental_df.columns)

dropped_columns = columns_before - columns_after

if dropped_columns:
    print(f"Izbačeno je {len(dropped_columns)} kolona:")
    print(list(dropped_columns))
else:
    print("Nijedna kolona nije izbačena.")


missing_counts = experimental_df.isna().sum()
missing_counts1 = input_features.isna().sum()
first_row = pd.DataFrame([missing_counts], columns=experimental_df.columns)
first_row1 = pd.DataFrame([missing_counts1], columns=input_features.columns)
experimental_df = pd.concat([first_row, experimental_df]).reset_index(drop=True)
input_features = pd.concat([first_row1, input_features]).reset_index(drop=True)
corr_matrix = experimental_df.iloc[1:].corr(method="spearman")


threshold = 0.5

corr_matrix_abs = corr_matrix.abs()

upper = corr_matrix_abs.where(np.triu(np.ones(corr_matrix_abs.shape), k=1).astype(bool))

high_corr_df = upper.stack().reset_index()
high_corr_df.columns = ['Column 1', 'Column 2', 'Correlation']

high_corr_df = high_corr_df[high_corr_df['Correlation'] > threshold].sort_values(by='Correlation', ascending=False).reset_index(drop=True)

print(f"Broj prejako korelisanih parova (> {threshold}): {len(high_corr_df)}")
print(high_corr_df)  

experimental_df.to_excel('experimental_numerical_data.xlsx', index=False)
high_corr_df.to_excel('entry_colums_correlation_over_0.5.xlsx', index=False)
input_features.to_excel('input_data.xlsx', index=False)


target_columns = [
    'Total Ret 3 Mo (Daily)', 'Total Ret 6 Mo (Daily)', 'Total Ret YTD (Daily)',
    'Total Ret 1 Yr (Daily)', 'Total Ret Annlzd 3 Yr (Daily)', 'Total Ret Annlzd 5 Yr (Daily)'
]

returns_corr_matrix = experimental_df.iloc[1:][target_columns].corr(method="spearman")

returns_corr_matrix.to_excel('correlation_matrix_outputs.xlsx')
all_columns = experimental_df.columns.tolist()
input_columns = [col for col in experimental_df.columns if col not in target_columns]

full_corr_matrix = experimental_df.iloc[1:].corr(method="spearman")

with pd.ExcelWriter('correlation_inputs_outputs.xlsx') as writer:
    for target in target_columns:
        abs_correlation = full_corr_matrix[target].loc[input_columns].abs()
        
        analysis_df = abs_correlation.to_frame(name='Absolute_Spearman_Correlation')
        analysis_df = analysis_df.sort_values(by='Absolute_Spearman_Correlation', ascending=False)
        
        sheet_name = target.replace('Total Ret ', '').replace(' (Daily)', '')
        analysis_df.to_excel(writer, sheet_name=sheet_name)