"""
Data Loader Module for Sales Intelligence Dashboard
Handles data loading, preprocessing, and caching for performance
"""
import pandas as pd
import streamlit as st
from datetime import datetime

@st.cache_data
def load_data():
    """Load and preprocess the sales data with caching for performance"""
    df = pd.read_csv("data/train.csv")
    
    # Parse date columns
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')
    
    # Calculate shipping delay in days
    df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
    
    # Extract year and month for time series analysis
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month
    df['Year-Month'] = df['Order Date'].dt.to_period('M').astype(str)
    
    return df

def filter_data(df, regions=None, segments=None, categories=None, 
                sub_categories=None, date_range=None):
    """Apply filters to the dataframe"""
    filtered_df = df.copy()
    
    if regions and len(regions) > 0:
        filtered_df = filtered_df[filtered_df['Region'].isin(regions)]
    
    if segments and len(segments) > 0:
        filtered_df = filtered_df[filtered_df['Segment'].isin(segments)]
    
    if categories and len(categories) > 0:
        filtered_df = filtered_df[filtered_df['Category'].isin(categories)]
    
    if sub_categories and len(sub_categories) > 0:
        filtered_df = filtered_df[filtered_df['Sub-Category'].isin(sub_categories)]
    
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['Order Date'] >= pd.Timestamp(start_date)) & 
            (filtered_df['Order Date'] <= pd.Timestamp(end_date))
        ]
    
    return filtered_df

def get_kpi_metrics(df):
    """Calculate key performance indicators"""
    total_sales = df['Sales'].sum()
    total_orders = df['Order ID'].nunique()
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    avg_shipping_days = df['Shipping Days'].mean()
    
    return {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'avg_shipping_days': avg_shipping_days
    }

def get_category_performance(df):
    """Get sales performance by category and sub-category"""
    category_sales = df.groupby('Category')['Sales'].sum().reset_index()
    category_sales = category_sales.sort_values('Sales', ascending=False)
    
    subcategory_sales = df.groupby(['Category', 'Sub-Category'])['Sales'].sum().reset_index()
    subcategory_sales = subcategory_sales.sort_values('Sales', ascending=False)
    
    return category_sales, subcategory_sales

def get_regional_performance(df):
    """Get sales performance by region"""
    regional_sales = df.groupby('Region')['Sales'].sum().reset_index()
    regional_sales = regional_sales.sort_values('Sales', ascending=False)
    return regional_sales

def get_time_series_data(df):
    """Get time series data for revenue trends"""
    time_series = df.groupby('Year-Month')['Sales'].sum().reset_index()
    time_series.columns = ['Period', 'Sales']
    return time_series

def get_shipping_analysis(df):
    """Analyze shipping delays by category"""
    shipping_by_category = df.groupby('Category')['Shipping Days'].mean().reset_index()
    shipping_by_category.columns = ['Category', 'Avg Shipping Days']
    return shipping_by_category

def identify_underperforming_segments(df):
    """Identify segments with lower revenue concentration"""
    segment_sales = df.groupby('Segment')['Sales'].sum()
    total_sales = segment_sales.sum()
    segment_share = (segment_sales / total_sales * 100).reset_index()
    segment_share.columns = ['Segment', 'Revenue Share %']
    
    # Identify segments below average (potential underperformers)
    avg_share = 100 / len(segment_share)
    segment_share['Status'] = segment_share['Revenue Share %'].apply(
        lambda x: '⚠️ Below Average' if x < avg_share else '✅ Above Average'
    )
    
    return segment_share
