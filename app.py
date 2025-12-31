"""
Interactive Sales Intelligence Dashboard
A Streamlit app to analyze retail sales records, uncovering key revenue drivers and shipping delays.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from data_loader import (
    load_data, filter_data, get_kpi_metrics, 
    get_category_performance, get_regional_performance,
    get_time_series_data, get_shipping_analysis,
    identify_underperforming_segments
)

# Page Configuration
st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Metric cards styling */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    div[data-testid="metric-container"] label {
        color: rgba(255, 255, 255, 0.8) !important;
        font-size: 0.9rem !important;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: white !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    
    /* Header styling */
    .dashboard-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .dashboard-header h1 {
        color: #ffffff;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .dashboard-header p {
        color: #a0a0a0;
        font-size: 1.1rem;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1a 100%);
    }
    
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stDateInput label {
        color: #ffffff !important;
    }
    
    /* Chart container styling */
    .chart-container {
        background: #1a1a2e;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Load data
df = load_data()

# ===== SIDEBAR FILTERS =====
st.sidebar.markdown("## 🎛️ Dashboard Filters")
st.sidebar.markdown("---")

# Date Range Filter
st.sidebar.markdown("### 📅 Date Range")
min_date = df['Order Date'].min().date()
max_date = df['Order Date'].max().date()

col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("From", min_date, min_value=min_date, max_value=max_date)
with col2:
    end_date = st.date_input("To", max_date, min_value=min_date, max_value=max_date)

st.sidebar.markdown("---")

# Region Filter
st.sidebar.markdown("### 🌍 Region")
all_regions = df['Region'].unique().tolist()
selected_regions = st.sidebar.multiselect(
    "Select Regions",
    options=all_regions,
    default=all_regions
)

# Segment Filter
st.sidebar.markdown("### 👥 Customer Segment")
all_segments = df['Segment'].unique().tolist()
selected_segments = st.sidebar.multiselect(
    "Select Segments",
    options=all_segments,
    default=all_segments
)

st.sidebar.markdown("---")

# Category Filter
st.sidebar.markdown("### 📦 Category")
all_categories = df['Category'].unique().tolist()
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=all_categories,
    default=all_categories
)

# Sub-Category Filter
available_subcategories = df[df['Category'].isin(selected_categories)]['Sub-Category'].unique().tolist()
selected_subcategories = st.sidebar.multiselect(
    "Select Sub-Categories",
    options=available_subcategories,
    default=available_subcategories
)

# Apply filters
filtered_df = filter_data(
    df,
    regions=selected_regions,
    segments=selected_segments,
    categories=selected_categories,
    sub_categories=selected_subcategories,
    date_range=(start_date, end_date)
)

# ===== MAIN DASHBOARD =====
# Header
st.markdown("""
<div class="dashboard-header">
    <h1>
        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="url(#gradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 10px;">
            <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#667eea"/>
                    <stop offset="100%" style="stop-color:#764ba2"/>
                </linearGradient>
            </defs>
            <line x1="18" y1="20" x2="18" y2="10"></line>
            <line x1="12" y1="20" x2="12" y2="4"></line>
            <line x1="6" y1="20" x2="6" y2="14"></line>
        </svg>
        Sales Intelligence Dashboard
    </h1>
    <p>Analyzing ~10,000 retail sales records to uncover key revenue drivers and shipping insights</p>
</div>
""", unsafe_allow_html=True)

# Data summary
st.markdown(f"**Showing:** {len(filtered_df):,} records out of {len(df):,} total")

# ===== KPI METRICS =====
st.markdown("### 📈 Key Performance Indicators")

kpis = get_kpi_metrics(filtered_df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Revenue",
        value=f"${kpis['total_sales']:,.0f}"
    )

with col2:
    st.metric(
        label="📦 Total Orders",
        value=f"{kpis['total_orders']:,}"
    )

with col3:
    st.metric(
        label="💵 Avg Order Value",
        value=f"${kpis['avg_order_value']:,.2f}"
    )

with col4:
    st.metric(
        label="⏱️ Avg Shipping Days",
        value=f"{kpis['avg_shipping_days']:.1f} days"
    )

st.markdown("---")

# ===== CHARTS ROW 1: Category Performance & Regional Analysis =====
st.markdown("### 🎯 Sales Performance Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Category & Sub-Category Revenue")
    category_sales, subcategory_sales = get_category_performance(filtered_df)
    
    # Treemap for hierarchical view
    fig_treemap = px.treemap(
        subcategory_sales,
        path=['Category', 'Sub-Category'],
        values='Sales',
        color='Sales',
        color_continuous_scale='Viridis',
        title=''
    )
    fig_treemap.update_layout(
        height=400,
        margin=dict(t=30, l=10, r=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig_treemap, use_container_width=True)

with col2:
    st.markdown("#### Regional Sales Distribution")
    regional_sales = get_regional_performance(filtered_df)
    
    fig_region = px.bar(
        regional_sales,
        x='Region',
        y='Sales',
        color='Sales',
        color_continuous_scale='Plasma',
        title=''
    )
    fig_region.update_layout(
        height=400,
        margin=dict(t=30, l=10, r=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    fig_region.update_traces(marker_line_width=0)
    st.plotly_chart(fig_region, use_container_width=True)

st.markdown("---")

# ===== CHARTS ROW 2: Time Series & Customer Segments =====
st.markdown("### 📊 Revenue Trends & Customer Insights")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("#### Revenue Over Time")
    time_series = get_time_series_data(filtered_df)
    
    fig_time = px.area(
        time_series,
        x='Period',
        y='Sales',
        title='',
        color_discrete_sequence=['#667eea']
    )
    fig_time.update_layout(
        height=350,
        margin=dict(t=30, l=10, r=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickangle=45),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    fig_time.update_traces(line=dict(width=2), fillcolor='rgba(102, 126, 234, 0.3)')
    st.plotly_chart(fig_time, use_container_width=True)

with col2:
    st.markdown("#### Segment Distribution")
    segment_data = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
    
    fig_segment = px.pie(
        segment_data,
        values='Sales',
        names='Segment',
        color_discrete_sequence=px.colors.sequential.Plasma_r,
        hole=0.4
    )
    fig_segment.update_layout(
        height=350,
        margin=dict(t=30, l=10, r=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        legend=dict(orientation='h', yanchor='bottom', y=-0.2)
    )
    st.plotly_chart(fig_segment, use_container_width=True)

st.markdown("---")

# ===== CHARTS ROW 3: Shipping Analysis =====
st.markdown("### ⏱️ Shipping Delay Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Shipping Days Distribution")
    fig_shipping_hist = px.histogram(
        filtered_df,
        x='Shipping Days',
        nbins=20,
        color_discrete_sequence=['#764ba2'],
        title=''
    )
    fig_shipping_hist.update_layout(
        height=350,
        margin=dict(t=30, l=10, r=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Number of Orders')
    )
    st.plotly_chart(fig_shipping_hist, use_container_width=True)

with col2:
    st.markdown("#### Avg Shipping Days by Category")
    shipping_analysis = get_shipping_analysis(filtered_df)
    
    fig_shipping_cat = px.bar(
        shipping_analysis,
        x='Category',
        y='Avg Shipping Days',
        color='Avg Shipping Days',
        color_continuous_scale='RdYlGn_r',
        title=''
    )
    fig_shipping_cat.update_layout(
        height=350,
        margin=dict(t=30, l=10, r=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig_shipping_cat, use_container_width=True)

st.markdown("---")

# ===== INSIGHTS SECTION =====
st.markdown("### 💡 Key Insights & Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Segment Performance Analysis")
    segment_performance = identify_underperforming_segments(filtered_df)
    st.dataframe(
        segment_performance.style.format({'Revenue Share %': '{:.1f}%'}),
        use_container_width=True,
        hide_index=True
    )
    
    # Calculate underperformance
    below_avg = segment_performance[segment_performance['Status'].str.contains('Below')]
    if not below_avg.empty:
        total_below = below_avg['Revenue Share %'].sum()
        st.warning(f"⚠️ Segments with below-average revenue concentration contribute only **{total_below:.1f}%** of total revenue. Consider targeted marketing strategies.")

with col2:
    st.markdown("#### Top 10 Products by Revenue")
    top_products = filtered_df.groupby('Product Name')['Sales'].sum().nlargest(10).reset_index()
    top_products.columns = ['Product', 'Revenue']
    top_products['Revenue'] = top_products['Revenue'].apply(lambda x: f"${x:,.0f}")
    st.dataframe(top_products, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>📊 Interactive Sales Intelligence Dashboard | Built with Streamlit & Plotly</p>
    <p>Analyzing {records:,} retail sales records</p>
</div>
""".format(records=len(df)), unsafe_allow_html=True)
