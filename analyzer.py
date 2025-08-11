# analyzer.py

import pandas as pd
import re
import numpy_financial as npf

def clean_price(price_text):
    if not isinstance(price_text, str): return None
    price_text = price_text.replace('₹', '').strip()
    try:
        if 'Cr' in price_text: return float(price_text.replace('Cr', '').strip()) * 1_00_00_000
        elif 'Lac' in price_text: return float(price_text.replace('Lac', '').strip()) * 1_00_000
        else: return float(price_text)
    except (ValueError, TypeError): return None

def clean_area(area_text):
    if not isinstance(area_text, str): return None
    try:
        area = re.search(r'[\d,.]+', area_text)
        if area: return float(area.group(0).replace(',', ''))
    except (ValueError, TypeError): return None

def analyze_properties(df: pd.DataFrame):
    print("Starting Advanced Analysis...")
    
    df['price_inr'] = df['price_text'].apply(clean_price)
    df['area'] = df['area_sqft'].apply(clean_area)
    df.dropna(subset=['price_inr', 'area'], inplace=True)
    if df.empty: return df
    df['price_per_sqft'] = df['price_inr'] / df['area']
    
    # --- DETAILED FINANCIAL UNDERWRITING ---
    DOWN_PAYMENT_PERCENT = 0.25
    INTEREST_RATE_ANNUAL = 0.07
    LOAN_TERM_YEARS = 30
    RENT_PER_SQFT_MONTHLY = 35
    EXPENSE_RATE = 0.33

    gross_rent_monthly = df['area'] * RENT_PER_SQFT_MONTHLY
    gross_rent_annual = gross_rent_monthly * 12

    total_operating_expenses = gross_rent_annual * EXPENSE_RATE
    df['noi'] = gross_rent_annual - total_operating_expenses
    df['cap_rate'] = (df['noi'] / df['price_inr']) * 100

    total_cash_invested = df['price_inr'] * DOWN_PAYMENT_PERCENT
    loan_amount = df['price_inr'] - total_cash_invested
    
    monthly_payment = npf.pmt(rate=INTEREST_RATE_ANNUAL / 12, nper=LOAN_TERM_YEARS * 12, pv=-loan_amount)
    annual_debt_service = monthly_payment * 12

    pre_tax_cash_flow = df['noi'] - annual_debt_service
    df['cash_on_cash_return'] = (pre_tax_cash_flow / total_cash_invested) * 100
    
    # --- Advanced Investment Score ---
    cap_rate_score = (df['cap_rate'] / 8) * 10
    coc_return_score = (df['cash_on_cash_return'] / 12) * 10
    
    df['investment_score'] = (cap_rate_score * 0.4) + (coc_return_score * 0.6)
    
    df = df.sort_values(by='investment_score', ascending=False)
    
    print("Advanced analysis complete.")
    return df