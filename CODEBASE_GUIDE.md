# 📚 Codebase Explanation Guide

> **For beginners who want to understand how this Streamlit dashboard works**

---

## 🤔 What is Streamlit?

**Streamlit** is a Python library that turns Python scripts into interactive web applications. Instead of learning HTML, CSS, and JavaScript, you write Python code and Streamlit automatically creates a beautiful web interface.

```python
import streamlit as st
st.title("Hello World!")  # This creates a webpage with a title!
```

**Key Streamlit concepts:**
- `st.` - Everything starts with this prefix
- The script runs **top to bottom** every time something changes
- Streamlit **automatically reruns** when you interact with widgets

---

## 📁 Project Structure

```
sales_dashboard/
├── app.py              # 🎯 Main dashboard (the UI)
├── data_loader.py      # 📊 Data processing functions
├── data/
│   └── train.csv       # 📁 Your sales data (9,800 rows)
├── requirements.txt    # 📦 Python packages needed
└── README.md           # 📖 Project overview
```

---

## 📊 Understanding `data_loader.py`

This file handles all data operations. It's separated from `app.py` to keep code organized.

### 1. Caching Data with `@st.cache_data`

```python
@st.cache_data
def load_data():
    df = pd.read_csv("data/train.csv")
    return df
```

**What this does:**
- `@st.cache_data` is a **decorator** (the `@` symbol)
- It tells Streamlit: "Remember this result, don't recalculate it"
- Without caching, the CSV would reload on every interaction (slow!)
- With caching, it loads once and stays in memory (fast!)

### 2. Date Parsing

```python
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')
```

**What this does:**
- Converts text like "25/12/2024" into actual date objects
- `format='%d/%m/%Y'` tells Python: day/month/year format
- Now we can do date math, filtering, and time-series charts

### 3. Calculating Shipping Days

```python
df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
```

**What this does:**
- Subtracts Order Date from Ship Date
- `.dt.days` extracts just the number of days
- Creates a new column we can analyze

### 4. Filter Function

```python
def filter_data(df, regions=None, segments=None, ...):
    filtered_df = df.copy()
    
    if regions and len(regions) > 0:
        filtered_df = filtered_df[filtered_df['Region'].isin(regions)]
    
    return filtered_df
```

**What this does:**
- Takes the full dataset and user-selected filters
- `.isin(regions)` checks if Region is in the selected list
- Returns only matching rows

### 5. KPI Calculations

```python
def get_kpi_metrics(df):
    total_sales = df['Sales'].sum()
    total_orders = df['Order ID'].nunique()  # nunique = number of unique
    avg_order_value = total_sales / total_orders
    return {...}
```

**What this does:**
- `.sum()` adds up all sales
- `.nunique()` counts unique order IDs (avoids counting duplicates)
- Returns a dictionary with all KPIs

---

## 🎨 Understanding `app.py` - The Main Dashboard

### 1. Page Configuration (Must be FIRST!)

```python
st.set_page_config(
    page_title="Sales Intelligence Dashboard",  # Browser tab title
    page_icon="📊",                              # Favicon emoji
    layout="wide",                               # Use full screen width
    initial_sidebar_state="expanded"             # Sidebar open by default
)
```

### 2. Custom CSS Styling

```python
st.markdown("""
<style>
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)
```

**What this does:**
- `st.markdown()` renders HTML/CSS
- `unsafe_allow_html=True` allows raw HTML (normally blocked for security)
- We use CSS to style the KPI cards with gradients

### 3. Sidebar Filters

```python
st.sidebar.markdown("## 🎛️ Dashboard Filters")

selected_regions = st.sidebar.multiselect(
    "Select Regions",           # Label shown to user
    options=all_regions,        # All possible choices
    default=all_regions         # What's selected initially
)
```

**What this does:**
- `st.sidebar.` puts elements in the left sidebar
- `multiselect` creates a dropdown where you can pick multiple options
- Returns a list of selected values

### 4. Date Input

```python
start_date = st.date_input(
    "From",                    # Label
    min_date,                  # Default value
    min_value=min_date,        # Earliest selectable date
    max_value=max_date         # Latest selectable date
)
```

**What this does:**
- Creates a calendar date picker
- Returns a Python date object

### 5. Displaying Metrics (KPIs)

```python
col1, col2, col3, col4 = st.columns(4)  # Create 4 equal columns

with col1:
    st.metric(
        label="💰 Total Revenue",
        value=f"${kpis['total_sales']:,.0f}"
    )
```

**What this does:**
- `st.columns(4)` creates 4 side-by-side columns
- `with col1:` puts content in first column
- `st.metric()` displays a big number with a label
- `f"${value:,.0f}"` formats as currency with commas

### 6. Plotly Charts

```python
import plotly.express as px

fig_treemap = px.treemap(
    subcategory_sales,                    # Data
    path=['Category', 'Sub-Category'],    # Hierarchy levels
    values='Sales',                       # What determines box size
    color='Sales',                        # What determines color
    color_continuous_scale='Viridis'      # Color scheme
)

st.plotly_chart(fig_treemap, use_container_width=True)
```

**What this does:**
- `px.treemap()` creates an interactive hierarchy chart
- `st.plotly_chart()` displays it in Streamlit
- `use_container_width=True` makes it fill available space

### 7. Layout with Columns

```python
col1, col2 = st.columns(2)  # Two 50% columns

with col1:
    st.markdown("#### Left Chart")
    st.plotly_chart(chart1)

with col2:
    st.markdown("#### Right Chart")
    st.plotly_chart(chart2)
```

### 8. Displaying DataFrames

```python
st.dataframe(
    segment_performance,           # The pandas DataFrame
    use_container_width=True,      # Full width
    hide_index=True                # Don't show row numbers
)
```

---

## 🔄 How Streamlit Reruns Work

**This is the MOST IMPORTANT concept!**

```
User changes filter → Streamlit reruns ENTIRE script → New data displayed
```

Every time you:
- Select a region
- Change a date
- Click anything interactive

Streamlit runs `app.py` from top to bottom again. That's why:
1. `@st.cache_data` is crucial (avoids reloading CSV every time)
2. Filter variables are created fresh each run
3. Charts are regenerated with new filtered data

---

## 🛠️ How to Modify the Dashboard

### Add a New KPI

1. In `data_loader.py`, add to `get_kpi_metrics()`:
```python
def get_kpi_metrics(df):
    # ... existing code ...
    total_quantity = df['Quantity'].sum()  # NEW
    return {
        # ... existing returns ...
        'total_quantity': total_quantity    # NEW
    }
```

2. In `app.py`, add a new metric:
```python
with col5:  # Add a 5th column
    st.metric(label="📦 Total Quantity", value=f"{kpis['total_quantity']:,}")
```

### Add a New Filter

In `app.py`:
```python
# Add to sidebar
ship_modes = df['Ship Mode'].unique().tolist()
selected_ship_modes = st.sidebar.multiselect(
    "Ship Mode",
    options=ship_modes,
    default=ship_modes
)

# Add to filter_data() call
filtered_df = filter_data(df, ..., ship_modes=selected_ship_modes)
```

### Add a New Chart

```python
# Create the Plotly figure
fig_new = px.bar(
    data,
    x='Category',
    y='Profit',
    title='Profit by Category'
)

# Display it
st.plotly_chart(fig_new, use_container_width=True)
```

---

## 📚 Key Streamlit Functions Reference

| Function | What It Does |
|----------|--------------|
| `st.title("text")` | Big title |
| `st.header("text")` | Section header |
| `st.markdown("**bold**")` | Formatted text |
| `st.metric(label, value)` | KPI card |
| `st.columns(n)` | Create n columns |
| `st.sidebar.xyz()` | Put in sidebar |
| `st.selectbox()` | Single-choice dropdown |
| `st.multiselect()` | Multi-choice dropdown |
| `st.date_input()` | Date picker |
| `st.plotly_chart(fig)` | Display Plotly chart |
| `st.dataframe(df)` | Display table |
| `st.warning("text")` | Yellow warning box |
| `@st.cache_data` | Cache function results |

---

## 🚀 Running the App

```bash
# Navigate to project folder
cd c:\Users\PRIYANGSHU\Downloads\sales_dashboard

# Run with Streamlit
python -m streamlit run app.py

# Opens at http://localhost:8501
```

**Hot Reload:** Save any changes to `app.py` and the browser auto-refreshes!

---

## 💡 Tips for Interview

1. **Explain the flow:** "Data loads from CSV, gets cached, then filtered based on user selections"
2. **Show interactivity:** Change filters and point out how charts update
3. **Discuss insights:** "The segment analysis shows which segments underperform"
4. **Mention Plotly:** "Hover over charts to see detailed tooltips"

---

*Now you understand every part of this codebase! 🎉*
