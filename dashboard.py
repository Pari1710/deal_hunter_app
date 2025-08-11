# dashboard.py

import streamlit as st
import pandas as pd

def create_dashboard(df):
    st.set_page_config(layout="wide", page_title="Real Estate AI Analyzer")
    st.title("🏠 Real-Time Property Deal Hunter")

    if df.empty:
        st.warning("Welcome! Your database is currently empty.")
        st.info("The scraper is running in the background to find the first deals. Please refresh this page in a minute or two.")
        return

    st.markdown("This dashboard analyzes property listings to find the best investment opportunities.")
    st.sidebar.header("Filter Your Deals")
    
    min_price = int(df['price_inr'].min())
    max_price = int(df['price_inr'].max())
    price_range = st.sidebar.slider(
        "Price Range (in Crores)", 
        min_value=float(min_price / 1_00_00_000), max_value=float(max_price / 1_00_00_000),
        value=(float(min_price / 1_00_00_000), float(max_price / 1_00_00_000)), step=0.1
    )
    
    min_area = int(df['area'].min())
    max_area = int(df['area'].max())
    area_range = st.sidebar.slider(
        "Area (sq. ft.)", min_value=min_area, max_value=max_area, value=(min_area, max_area)
    )
    
    filtered_df = df[
        (df['price_inr'] >= price_range[0] * 1_00_00_000) & (df['price_inr'] <= price_range[1] * 1_00_00_000) &
        (df['area'] >= area_range[0]) & (df['area'] <= area_range[1])
    ]

    st.header(f"Showing {len(filtered_df)} Matching Deals (from all historical data)")

    if filtered_df.empty:
        st.warning("No properties in the database match your filter criteria.")
    else:
        display_columns = ['title', 'price_text', 'cap_rate', 'cash_on_cash_return', 'investment_score']
        st.dataframe(filtered_df[display_columns].style.format({
            'cap_rate': '{:.2f}%', 'cash_on_cash_return': '{:.2f}%', 'investment_score': '{:.2f}'
        }))