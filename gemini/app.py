import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Enterprise KPI Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    h1 {color: #1f77b4; font-weight: 700;}
    h2, h3 {color: #2c3e50;}
    .stMetric {
        background-color: white; 
        padding: 15px; 
        border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# MOCK DATA GENERATOR
# ==========================================
@st.cache_data
def load_mock_data():
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", periods=12, freq='ME')
    
    return {
        "revenue_trend": pd.DataFrame({"Date": dates, "Revenue": np.random.randint(50000, 150000, size=12), "Orders": np.random.randint(500, 1500, size=12)}),
        "region_data": pd.DataFrame({"Region": ["North America", "EMEA", "APAC", "LATAM"], "Revenue": [450000, 320000, 280000, 150000]}),
        "sales_teams": pd.DataFrame({"Team": ["Alpha", "Beta", "Gamma", "Delta"], "Revenue": [300000, 250000, 400000, 200000]}),
        "customers": pd.DataFrame({"Customer": [f"Cust_{i}" for i in range(1, 21)], "Revenue": np.random.randint(10000, 50000, size=20)}),
        "segments": pd.DataFrame({"Segment": ["Platinum", "Gold", "Silver", "Bronze"], "Users": [150, 400, 850, 1200]}),
        "products": pd.DataFrame({"Product": [f"Prod_{i}" for i in range(1, 11)], "Revenue": np.random.randint(20000, 80000, size=10), "Category": np.random.choice(["Electronics", "Software", "Services"], 10)}),
        "churn": pd.DataFrame({"Risk_Level": ["High", "Medium", "Low"], "Customers": [120, 340, 1500]})
    }

data = load_mock_data()

# ==========================================
# PAGE 1: EXECUTIVE REVENUE OVERVIEW
# ==========================================
def page_executive_overview():
    st.title("Page 1: Executive Revenue Overview")
    st.markdown("##### *Executive snapshot of overall business performance.*")
    
    # KPI Widgets
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Revenue", "$1.2M", "12.5%", help="GOLD.REVENUE_SUMMARY")
    col2.metric("Revenue Growth", "12.5%", "2.1%")
    col3.metric("Total Orders", "14,230", "5.4%")
    col4.metric("Avg Order Value", "$84.50", "-1.2%")
    col5.metric("Active Customers", "8,942", "8.9%")
    
    st.divider()
    
    # Charts Row 1
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Revenue Trend")
        fig1 = px.line(data["revenue_trend"], x="Date", y="Revenue", markers=True, template="plotly_white")
        fig1.update_traces(line_color="#1f77b4")
        st.plotly_chart(fig1, use_container_width=True)
        
    with col_chart2:
        st.subheader("Revenue vs Orders")
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=data["revenue_trend"]["Date"], y=data["revenue_trend"]["Revenue"], name="Revenue", marker_color="#3498db"))
        fig2.add_trace(go.Scatter(x=data["revenue_trend"]["Date"], y=data["revenue_trend"]["Orders"], name="Orders", yaxis="y2", line=dict(color="#e74c3c", width=3)))
        fig2.update_layout(yaxis2=dict(overlaying="y", side="right"), template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

    # Charts Row 2
    col_chart3, col_chart4, col_chart5 = st.columns([1, 1, 1])
    with col_chart3:
        st.subheader("Revenue by Region")
        fig3 = px.bar(data["region_data"], x="Region", y="Revenue", color="Region", template="plotly_white")
        st.plotly_chart(fig3, use_container_width=True)
    with col_chart4:
        st.subheader("Revenue by Sales Team")
        fig4 = px.bar(data["sales_teams"].sort_values("Revenue"), x="Revenue", y="Team", orientation='h', template="plotly_white")
        st.plotly_chart(fig4, use_container_width=True)
    with col_chart5:
        st.subheader("Top Revenue Customers")
        st.dataframe(data["customers"].head(5).style.background_gradient(cmap='Blues'), use_container_width=True, hide_index=True)

# ==========================================
# PAGE 2: CUSTOMER INTELLIGENCE
# ==========================================
def page_customer_intelligence():
    st.title("Page 2: Customer Intelligence")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Customers", "12,450", "4.3%")
    col2.metric("New Customers", "1,204", "15.2%")
    col3.metric("Repeat Customers", "8,540", "2.1%")
    col4.metric("Customer LTV", "$3,240", "8.4%")
    col5.metric("Retention Rate", "88.5%", "-0.5%")
    
    st.divider()
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Customer Segmentation")
        fig = px.pie(data["segments"], values="Users", names="Segment", hole=0.5, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("New vs Repeat Customers (Trend)")
        df_area = pd.DataFrame({"Date": data["revenue_trend"]["Date"], "New": np.random.randint(100, 300, 12), "Repeat": np.random.randint(500, 1000, 12)})
        fig2 = px.area(df_area, x="Date", y=["New", "Repeat"], template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# PAGE 3: PRODUCT INTELLIGENCE
# ==========================================
def page_product_intelligence():
    st.title("Page 3: Product Intelligence")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Product Revenue", "$985K", "10.1%")
    col2.metric("Total Units Sold", "45,200", "5.4%")
    col3.metric("Avg Selling Price", "$21.50", "1.2%")
    col4.metric("Fast Moving Products", "24", "3")
    col5.metric("Slow Moving Products", "8", "-2")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top Products by Revenue")
        fig = px.bar(data["products"].sort_values("Revenue", ascending=False).head(10), x="Revenue", y="Product", orientation='h', template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Revenue by Category")
        fig2 = px.treemap(data["products"], path=["Category", "Product"], values="Revenue", template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# PAGE 4: CHURN & RISK ANALYTICS
# ==========================================
def page_churn_risk():
    st.title("Page 4: Churn & Risk Analytics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("High-Risk Customers", "120", "-15", delta_color="inverse")
    col2.metric("Revenue At Risk", "$450K", "-$20K", delta_color="inverse")
    col3.metric("Avg Churn Score", "42/100", "-5%", delta_color="inverse")
    col4.metric("Churned Customers", "45", "-2", delta_color="inverse")
    col5.metric("Recoverable Revenue", "$120K", "$15K")
    
    st.divider()
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Churn Distribution")
        fig = px.pie(data["churn"], values="Customers", names="Risk_Level", hole=0.5, 
                     color="Risk_Level", color_discrete_map={"High":"#e74c3c", "Medium":"#f39c12", "Low":"#2ecc71"})
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Inactivity Distribution")
        inactivity_data = np.random.normal(30, 10, 1000)
        fig2 = px.histogram(x=inactivity_data, nbins=20, labels={'x':'Days Inactive'}, template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# PAGE 5: STRATEGIC BUSINESS INSIGHTS
# ==========================================
def page_strategic_insights():
    st.title("Page 5: Strategic Business Insights")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Top Customer Contrib %", "42%", "-2%")
    col2.metric("Top Product Contrib %", "65%", "4%")
    col3.metric("Revenue Dependency Score", "7.8/10", "0.2", delta_color="inverse")
    col4.metric("Critical Alerts", "3", "-1", delta_color="inverse")
    col5.metric("AI Gen Insights", "12 active", "2")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Executive Risk Matrix")
        df_risk = pd.DataFrame({"Account": [f"Acc_{i}" for i in range(50)], "Risk Score": np.random.rand(50)*100, "Value": np.random.rand(50)*100000})
        fig = px.scatter(df_risk, x="Risk Score", y="Value", size="Value", color="Risk Score", hover_name="Account", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("AI Recommendation Cards")
        st.info("💡 **Cross-sell Opportunity:** Clients in 'Gold' segment purchasing 'Software' have a 78% likelihood to buy 'Services'. Implement targeted email sequence.")
        st.warning("⚠️ **Churn Alert:** 15 accounts in the 'APAC' region show declining activity over the last 30 days. Engage customer success team.")
        st.success("📈 **Growth Signal:** 'Prod_7' has seen a 40% WoW organic growth. Consider increasing ad spend for this product category.")

# ==========================================
# NAVIGATION ROUTING
# ==========================================
sidebar_options = {
    "1. Executive Revenue Overview": page_executive_overview,
    "2. Customer Intelligence": page_customer_intelligence,
    "3. Product Intelligence": page_product_intelligence,
    "4. Churn & Risk Analytics": page_churn_risk,
    "5. Strategic Business Insights": page_strategic_insights
}

st.sidebar.title("📊 BI Navigation")
st.sidebar.markdown("---")
selection = st.sidebar.radio("Go to Page:", list(sidebar_options.keys()))
st.sidebar.markdown("---")
st.sidebar.caption("Data Source: GOLD Tier")

# Render selected page
sidebar_options[selection]()