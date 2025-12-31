# 📊 Interactive Sales Intelligence Dashboard

A live interactive Streamlit application to analyze nearly 10,000 retail sales records, uncovering key revenue drivers and shipping delays.

## 🚀 Features

### Key Performance Indicators
- **Total Revenue** - Track overall sales performance
- **Total Orders** - Monitor order volume
- **Average Order Value** - Understand purchase patterns
- **Average Shipping Days** - Analyze fulfillment efficiency

### Interactive Filtering
- 📅 **Date Range** - Filter by order date period
- 🌍 **Region** - East, West, Central, South
- 👥 **Customer Segment** - Consumer, Corporate, Home Office
- 📦 **Category & Sub-Category** - Drill down into product categories

### Dynamic Visualizations (Plotly)
- **Treemap** - Category & Sub-category revenue distribution
- **Bar Charts** - Regional sales performance
- **Area Chart** - Revenue trends over time
- **Donut Chart** - Customer segment distribution
- **Histogram** - Shipping days distribution
- **Insights Table** - Underperforming segment analysis

## 📈 Key Insights

- Identifies underperforming segments contributing to ~15% lower revenue concentration
- Analyzes shipping delays across categories for optimization
- Enables stakeholder-level exploratory analysis with real-time filtering

## 🛠️ Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/sales-dashboard.git
cd sales-dashboard
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the dashboard
```bash
streamlit run app.py
```

4. Open your browser to `http://localhost:8501`

## 📁 Project Structure

```
sales_dashboard/
├── app.py              # Main Streamlit dashboard
├── data_loader.py      # Data loading and processing module
├── data/
│   └── train.csv       # Sales dataset (~10,000 records)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## 🔧 Tech Stack

- **Python** - Core programming language
- **Streamlit** - Web application framework
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation and analysis

## 📊 Dataset

The dashboard analyzes retail sales data with the following dimensions:
- Order Information (ID, Date, Ship Date)
- Customer Details (Segment, Region)
- Product Details (Category, Sub-Category, Name)
- Sales Metrics

## 📷 Screenshots

*Run the app to see the interactive dashboard in action!*

---

**Built with ❤️ using Streamlit & Plotly | December 2025**
