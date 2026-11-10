import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date, timedelta

# ============================================================
# CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="NEXUS | Business Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DESIGN SYSTEM
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
  --bg: #0b1020;
  --panel: #121a2b;
  --panel-2: #172238;
  --border: rgba(148,163,184,.15);
  --muted: #91a0b8;
  --text: #edf3ff;
  --cyan: #4dd8d0;
  --blue: #729cff;
  --purple: #b59aff;
  --green: #51d6a5;
  --orange: #ffb86b;
  --red: #ff7185;
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: radial-gradient(ellipse at 15% 0%, #172746 0%, #0b1020 42%, #090e19 100%); color: var(--text); }
[data-testid="stHeader"] { background: rgba(11,16,32,0); }
[data-testid="stSidebar"] { background: #0c1424; border-right: 1px solid var(--border); }
[data-testid="stSidebar"] > div { padding-top: 1.2rem; }
.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1600px; }
h1,h2,h3,h4 { font-family: 'Manrope', sans-serif !important; color: var(--text) !important; letter-spacing: -.035em; }
p, label, span { color: inherit; }
.small-muted { color: var(--muted); font-size: .83rem; }
.brand { font-family: 'Manrope'; font-weight: 800; font-size: 1.28rem; letter-spacing: .12em; color: #f4f7ff; }
.brand-mark { color: var(--cyan); }
.sidebar-caption { color: #7586a3; text-transform: uppercase; letter-spacing: .15em; font-size: .68rem; font-weight: 700; margin: 1.3rem 0 .55rem; }
.page-eyebrow { color: var(--cyan); text-transform: uppercase; letter-spacing: .17em; font-size: .72rem; font-weight: 700; margin-bottom: .35rem; }
.page-title { font-family: 'Manrope'; font-size: 2rem; font-weight: 800; letter-spacing: -.055em; color: #f5f7ff; margin: 0; }
.page-subtitle { color: #9aa9c2; font-size: .94rem; margin-top: .3rem; margin-bottom: 1.35rem; }
.kpi-card { background: linear-gradient(145deg, rgba(26,39,62,.96), rgba(17,26,43,.96)); border: 1px solid var(--border); border-radius: 15px; padding: 17px 18px 15px; min-height: 120px; box-shadow: 0 10px 30px rgba(0,0,0,.12); }
.kpi-label { color: #9aabc5; font-size: .76rem; font-weight: 600; letter-spacing: .035em; }
.kpi-value { color: #f4f7ff; font-family: 'Manrope'; font-size: 1.72rem; font-weight: 800; margin-top: 7px; line-height: 1.2; }
.kpi-delta { font-size: .75rem; margin-top: 8px; color: #55d9a9; }
.kpi-delta.negative { color: #ff8293; }
.panel { background: rgba(18,26,43,.78); border: 1px solid var(--border); border-radius: 16px; padding: 16px 18px 8px; }
.panel-title { color: #eef3ff; font-family: 'Manrope'; font-size: 1rem; font-weight: 700; margin-bottom: 0; }
.panel-subtitle { color: #8fa0bb; font-size: .76rem; margin-top: 3px; margin-bottom: 8px; }
.section-label { color: #a9b8d0; font-family: 'Manrope'; font-weight: 700; font-size: .88rem; letter-spacing: .02em; margin: 1.05rem 0 .65rem; }
.insight-card { background: linear-gradient(135deg, rgba(30,49,75,.95), rgba(20,29,48,.95)); border: 1px solid rgba(77,216,208,.22); border-radius: 14px; padding: 15px 17px; min-height: 115px; }
.insight-tag { color: var(--cyan); font-size: .68rem; text-transform: uppercase; letter-spacing: .12em; font-weight: 700; }
.insight-text { color: #e4ecfa; font-size: .88rem; line-height: 1.5; margin-top: 7px; }
div[data-testid="stMetric"] { background: transparent; }
.stSelectbox label, .stDateInput label, .stMultiSelect label { color: #9aabc5 !important; font-size: .8rem !important; }
.stSelectbox > div > div, .stDateInput > div > div, .stMultiSelect > div > div { background: #121c30; border-color: var(--border); }
.stRadio label { color: #c8d4e8 !important; }
div[data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
hr { border-color: var(--border); }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DEMO DATA — replace this section with your GOLD-layer queries
# ============================================================
@st.cache_data
def load_demo_data():
    rng = np.random.default_rng(42)
    months = pd.date_range(end=pd.Timestamp.today().normalize().replace(day=1), periods=18, freq="MS")
    regions = ["North", "South", "East", "West", "Central"]
    teams = ["Enterprise", "Growth", "Strategic Accounts", "SMB", "Digital"]
    categories = ["Electronics", "Home & Living", "Industrial", "Office", "Accessories"]
    products = [
        ("Pro Laptop", "Electronics"), ("Smart Monitor", "Electronics"),
        ("Wireless Headset", "Accessories"), ("Ergo Chair", "Home & Living"),
        ("Standing Desk", "Home & Living"), ("Network Switch", "Industrial"),
        ("Cloud Gateway", "Industrial"), ("Office Suite", "Office"),
        ("Laser Printer", "Office"), ("Docking Station", "Accessories"),
        ("Tablet Pro", "Electronics"), ("Smart Sensor", "Industrial"),
    ]
    customers = [f"Customer {i:03d}" for i in range(1, 81)]
    customer_region = {c: rng.choice(regions) for c in customers}
    customer_segment = {c: rng.choice(["Platinum", "Gold", "Silver", "Bronze"], p=[.12,.23,.3,.35]) for c in customers}
    product_base = {p[0]: rng.uniform(900, 6500) for p in products}
    rows = []
    for m_idx, month in enumerate(months):
        for _ in range(int(rng.integers(100, 155))):
            customer = rng.choice(customers)
            product, category = products[int(rng.integers(0, len(products)))]
            units = int(rng.integers(1, 9))
            trend = 1 + m_idx * .018
            revenue = product_base[product] * units * trend * rng.uniform(.72, 1.28)
            rows.append({
                "date": month + pd.Timedelta(days=int(rng.integers(0, 25))),
                "month": month, "customer": customer, "region": customer_region[customer],
                "segment": customer_segment[customer], "product": product, "category": category,
                "team": rng.choice(teams), "quantity": units, "revenue": round(revenue, 2),
                "order_id": f"ORD-{len(rows)+1:06d}"
            })
    sales = pd.DataFrame(rows)
    cust = sales.groupby("customer").agg(
        revenue=("revenue","sum"), orders=("order_id","nunique"),
        last_order=("date","max"), first_order=("date","min"),
        region=("region","first"), segment=("segment","first")
    ).reset_index()
    today = pd.Timestamp.today().normalize()
    cust["inactivity_days"] = (today - cust["last_order"]).dt.days.clip(lower=0)
    cust["churn_score"] = np.clip(
        (cust["inactivity_days"] / 150) * .55 + rng.uniform(0, .42, len(cust)), 0, 1
    )
    cust["risk"] = pd.cut(cust["churn_score"], [-.01,.35,.68,1.01], labels=["Low","Medium","High"])
    cust["revenue_at_risk"] = cust["revenue"] * cust["churn_score"] * .35
    cust["recoverable_revenue"] = cust["revenue_at_risk"] * rng.uniform(.35,.72,len(cust))
    return sales, cust

sales_all, customers_all = load_demo_data()

# ============================================================
# HELPERS
# ============================================================
COLORS = ["#4dd8d0", "#729cff", "#b59aff", "#ffb86b", "#ff7185", "#79c7ff"]
RISK_COLORS = {"High":"#ff7185", "Medium":"#ffb86b", "Low":"#51d6a5"}
PLOT_TEMPLATE = "plotly_dark"

def money(x, compact=False):
    if compact:
        if abs(x) >= 1e7: return f"₹{x/1e7:.2f}Cr"
        if abs(x) >= 1e5: return f"₹{x/1e5:.2f}L"
        return f"₹{x:,.0f}"
    return f"₹{x:,.0f}"

def chart_layout(fig, height=330, showlegend=True):
    fig.update_layout(
        template=PLOT_TEMPLATE, height=height, paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans", color="#aebbd0", size=11),
        margin=dict(l=8,r=12,t=28,b=8), showlegend=showlegend,
        legend=dict(orientation="h", y=1.12, x=0, font=dict(size=10)),
        hoverlabel=dict(bgcolor="#172238", bordercolor="#33445f", font_color="#f4f7ff"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="rgba(148,163,184,.12)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,.10)", zeroline=False)
    return fig

def panel_header(title, subtitle=""):
    st.markdown(f'<div class="panel-title">{title}</div><div class="panel-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def kpi(label, value, delta=None, negative=False):
    delta_html = ""
    if delta is not None:
        cls = "negative" if negative else ""
        delta_html = f'<div class="kpi-delta {cls}">{delta}</div>'
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>{delta_html}</div>',
        unsafe_allow_html=True
    )

def page_header(eyebrow, title, subtitle):
    st.markdown(f'<div class="page-eyebrow">{eyebrow}</div><div class="page-title">{title}</div><div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def insight(tag, text):
    st.markdown(f'<div class="insight-card"><div class="insight-tag">{tag}</div><div class="insight-text">{text}</div></div>', unsafe_allow_html=True)

def make_filters(df):
    with st.sidebar:
        st.markdown('<div class="sidebar-caption">Workspace filters</div>', unsafe_allow_html=True)
        min_d, max_d = df["date"].min().date(), df["date"].max().date()
        date_range = st.date_input("Date range", value=(min_d, max_d), min_value=min_d, max_value=max_d)
        region = st.multiselect("Region", sorted(df["region"].unique()), default=sorted(df["region"].unique()))
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start, end = date_range
        else:
            start, end = min_d, max_d
    filtered = df[
        df["date"].dt.date.between(start, end) &
        df["region"].isin(region)
    ].copy()
    return filtered

def section_gap():
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================
with st.sidebar:
    st.markdown('<div class="brand"><span class="brand-mark">◈</span> NEXUS</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-muted">BUSINESS INTELLIGENCE SUITE</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="sidebar-caption">Analytics</div>', unsafe_allow_html=True)
    pages = {
        "Executive Overview": "01",
        "Customer Intelligence": "02",
        "Product Intelligence": "03",
        "Churn & Risk": "04",
        "Strategic Insights": "05",
    }
    selected_page = st.radio(
        "Navigate", list(pages.keys()), label_visibility="collapsed",
        format_func=lambda x: f"{pages[x]}   {x}"
    )
    st.markdown("---")
    st.markdown('<div class="sidebar-caption">Data environment</div>', unsafe_allow_html=True)
    st.markdown("🟢 &nbsp; Demo data connected", unsafe_allow_html=True)
    st.caption("Last refreshed: " + pd.Timestamp.now().strftime("%d %b %Y · %H:%M"))
    st.markdown("---")
    st.caption("NEXUS Analytics · v1.0")

filtered = make_filters(sales_all)
if filtered.empty:
    st.warning("No records match the selected filters. Expand the date range or region selection.")
    st.stop()

# Consistent aggregates
total_revenue = filtered["revenue"].sum()
total_orders = filtered["order_id"].nunique()
active_customers = filtered["customer"].nunique()
aov = total_revenue / max(total_orders, 1)
monthly = filtered.groupby("month", as_index=False).agg(revenue=("revenue","sum"), orders=("order_id","nunique"))
monthly["growth"] = monthly["revenue"].pct_change().fillna(0) * 100
prev_rev = monthly["revenue"].iloc[-2] if len(monthly) > 1 else total_revenue
growth = (monthly["revenue"].iloc[-1] / prev_rev - 1) * 100 if prev_rev else 0

# ============================================================
# PAGE 1 — EXECUTIVE REVENUE OVERVIEW
# ============================================================
if selected_page == "Executive Overview":
    page_header("01 / PERFORMANCE", "Executive Revenue Overview", "A real-time pulse check on revenue, demand and commercial execution.")
    cols = st.columns(5)
    with cols[0]: kpi("TOTAL REVENUE", money(total_revenue, True), "Across selected period")
    with cols[1]: kpi("REVENUE GROWTH", f"{growth:+.1f}%", "Latest month vs previous", growth < 0)
    with cols[2]: kpi("TOTAL ORDERS", f"{total_orders:,}", "Unique sales orders")
    with cols[3]: kpi("AVG. ORDER VALUE", money(aov, True), "Revenue per order")
    with cols[4]: kpi("ACTIVE CUSTOMERS", f"{active_customers:,}", "Customers with purchases")
    section_gap()
    left, right = st.columns([1.65, 1])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_header("Revenue trajectory", "Monthly revenue performance · GOLD.REVENUE_SUMMARY")
        fig = px.area(monthly, x="month", y="revenue")
        fig.update_traces(line=dict(color="#4dd8d0", width=3), fillcolor="rgba(77,216,208,.13)", hovertemplate="%{x|%b %Y}<br>₹%{y:,.0f}<extra></extra>")
        chart_layout(fig, 320, False)
        fig.update_yaxes(tickprefix="₹", tickformat="~s")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_header("Revenue vs orders", "Commercial volume and value")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=monthly["month"], y=monthly["orders"], name="Orders", marker_color="#729cff", opacity=.78), secondary_y=False)
        fig.add_trace(go.Scatter(x=monthly["month"], y=monthly["revenue"], name="Revenue", line=dict(color="#4dd8d0", width=3)), secondary_y=True)
        chart_layout(fig, 320)
        fig.update_yaxes(title_text="Orders", secondary_y=False, showgrid=False)
        fig.update_yaxes(title_text="Revenue", tickprefix="₹", tickformat="~s", secondary_y=True, gridcolor="rgba(148,163,184,.1)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    left, right = st.columns([1.05, 1])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_header("Revenue by region", "Geographic distribution · illustrative demo coordinates")
        reg = filtered.groupby("region", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
        coords = {"North":(28.6139,77.2090),"South":(13.0827,80.2707),"East":(22.5726,88.3639),"West":(19.0760,72.8777),"Central":(23.2599,77.4126)}
        reg["lat"] = reg["region"].map(lambda x: coords[x][0])
        reg["lon"] = reg["region"].map(lambda x: coords[x][1])
        fig = px.scatter_map(
            reg,
            lat="lat",
            lon="lon",
            size="revenue",
            color="revenue",
            hover_name="region",
            zoom=3.5,
            map_style="carto-darkmatter",
        )
        fig.update_layout(mapbox_style="carto-darkmatter")
        chart_layout(fig, 300, False)
        fig.update_layout(mapbox=dict(style="carto-darkmatter", center=dict(lat=21.5,lon=80.5), zoom=3.2), coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_header("Sales team leaderboard", "Revenue contribution by team")
        team = filtered.groupby("team", as_index=False)["revenue"].sum().sort_values("revenue")
        fig = px.bar(team, x="revenue", y="team", orientation="h", text="revenue")
        fig.update_traces(marker_color="#729cff", texttemplate="₹%{x:.2s}", textposition="outside", cliponaxis=False)
        chart_layout(fig, 300, False)
        fig.update_xaxes(tickprefix="₹", tickformat="~s")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Top revenue customers</div>', unsafe_allow_html=True)
    top = filtered.groupby("customer", as_index=False).agg(revenue=("revenue","sum"), orders=("order_id","nunique"), region=("region","first")).nlargest(8,"revenue")
    top["Revenue"] = top["revenue"].map(lambda x: money(x))
    top = top.rename(columns={"customer":"Customer","orders":"Orders","region":"Region"})[["Customer","Region","Orders","Revenue"]]
    st.dataframe(top, use_container_width=True, hide_index=True)

# ============================================================
# PAGE 2 — CUSTOMER INTELLIGENCE
# ============================================================
elif selected_page == "Customer Intelligence":
    page_header("02 / CUSTOMER VALUE", "Customer Intelligence", "Understand who your customers are, what they contribute and where loyalty is strongest.")
    c = customers_all[customers_all["customer"].isin(filtered["customer"].unique())].copy()
    cust_rev = filtered.groupby("customer", as_index=False).agg(revenue=("revenue","sum"), orders=("order_id","nunique"), region=("region","first"), segment=("segment","first"))
    cust_rev["clv"] = cust_rev["revenue"] / cust_rev["orders"].clip(lower=1) * 2.8
    repeat = (cust_rev["orders"] > 1).sum()
    new = (c["first_order"] >= filtered["date"].min()).sum()
    retention = repeat / max(len(cust_rev),1) * 100
    cols = st.columns(5)
    with cols[0]: kpi("TOTAL CUSTOMERS", f"{len(cust_rev):,}", "In selected period")
    with cols[1]: kpi("NEW CUSTOMERS", f"{new:,}", "First purchase in period")
    with cols[2]: kpi("REPEAT CUSTOMERS", f"{repeat:,}", "More than one order")
    with cols[3]: kpi("AVG. CUSTOMER LTV", money(cust_rev["clv"].mean() if len(cust_rev) else 0, True), "Demo lifetime-value proxy")
    with cols[4]: kpi("RETENTION RATE", f"{retention:.1f}%", "Repeat customers / total")
    section_gap()
    left,right = st.columns([.9,1.35])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_header("Customer segmentation", "Value tiers by customer count")
        seg = cust_rev.groupby("segment",as_index=False).size().rename(columns={"size":"customers"})
        fig = px.pie(seg, names="segment", values="customers", hole=.68, color="segment",
                     color_discrete_map={"Platinum":"#b59aff","Gold":"#ffb86b","Silver":"#a9bbd1","Bronze":"#c98568"})
        fig.update_traces(textposition="inside", textinfo="percent", marker=dict(line=dict(color="#121a2b",width=3)))
        chart_layout(fig, 310)
        fig.update_layout(showlegend=True, legend=dict(orientation="h",y=-.12,x=.05))
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_header("Top 20 customers", "Ranked by revenue contribution")
        top20 = cust_rev.nlargest(20,"revenue").sort_values("revenue")
        fig = px.bar(top20,x="revenue",y="customer",orientation="h",color="revenue",color_continuous_scale=["#315a78","#4dd8d0"])
        chart_layout(fig, 310, False)
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(tickprefix="₹",tickformat="~s")
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    left,right = st.columns(2)
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_header("Revenue contribution · Pareto", "Cumulative revenue share by customer")
        pareto = cust_rev.sort_values("revenue",ascending=False).reset_index(drop=True)
        pareto["rank"] = np.arange(1,len(pareto)+1)
        pareto["cumulative"] = pareto["revenue"].cumsum()/max(pareto["revenue"].sum(),1)*100
        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(x=pareto["rank"],y=pareto["revenue"],name="Revenue",marker_color="#729cff"),secondary_y=False)
        fig.add_trace(go.Scatter(x=pareto["rank"],y=pareto["cumulative"],name="Cumulative %",line=dict(color="#ffb86b",width=3)),secondary_y=True)
        chart_layout(fig,300)
        fig.update_yaxes(tickprefix="₹",tickformat="~s",secondary_y=False)
        fig.update_yaxes(ticksuffix="%",range=[0,105],secondary_y=True,showgrid=False)
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_header("New vs repeat customers", "Monthly customer mix")
        tmp = filtered.groupby(["month","customer"]).agg(orders=("order_id","nunique")).reset_index()
        tmp["type"] = np.where(tmp["orders"] > 1,"Repeat","New / one-time")
        mix = tmp.groupby(["month","type"]).size().reset_index(name="customers")
        fig = px.area(mix,x="month",y="customers",color="type",color_discrete_map={"Repeat":"#4dd8d0","New / one-time":"#729cff"})
        fig.update_traces(line=dict(width=2))
        chart_layout(fig,300)
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="panel">',unsafe_allow_html=True)
    panel_header("Customer geography","Revenue-weighted customer locations · illustrative demo coordinates")
    geo = cust_rev.groupby("region",as_index=False).agg(customers=("customer","count"),revenue=("revenue","sum"))
    coords = {"North":(28.6139,77.2090),"South":(13.0827,80.2707),"East":(22.5726,88.3639),"West":(19.0760,72.8777),"Central":(23.2599,77.4126)}
    geo["lat"] = geo["region"].map(lambda x:coords[x][0]); geo["lon"] = geo["region"].map(lambda x:coords[x][1])
    fig = px.scatter_mapbox(geo,lat="lat",lon="lon",size="customers",color="revenue",hover_name="region",hover_data=["customers"],
                            color_continuous_scale=["#315a78","#4dd8d0"],zoom=3.2,center={"lat":21.5,"lon":80.5},height=310)
    fig.update_layout(mapbox_style="carto-darkmatter")
    chart_layout(fig,310,False)
    fig.update_layout(mapbox=dict(style="carto-darkmatter",center=dict(lat=21.5,lon=80.5),zoom=3.2),coloraxis_showscale=False)
    st.plotly_chart(fig,use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ============================================================
# PAGE 3 — PRODUCT INTELLIGENCE
# ============================================================
elif selected_page == "Product Intelligence":
    page_header("03 / PRODUCT PERFORMANCE", "Product Intelligence", "Find the products and categories creating momentum — and the ones quietly losing it.")
    prod = filtered.groupby(["product","category"],as_index=False).agg(revenue=("revenue","sum"),quantity=("quantity","sum"),orders=("order_id","nunique"))
    prod["asp"] = prod["revenue"]/prod["quantity"].clip(lower=1)
    monthly_prod = filtered.groupby(["month","product"],as_index=False).agg(revenue=("revenue","sum"),quantity=("quantity","sum"))
    last_month = monthly_prod["month"].max()
    recent = monthly_prod[monthly_prod["month"]==last_month].groupby("product")["quantity"].sum()
    prev_month = monthly_prod["month"].drop_duplicates().sort_values().iloc[-2] if monthly_prod["month"].nunique()>1 else last_month
    previous = monthly_prod[monthly_prod["month"]==prev_month].groupby("product")["quantity"].sum()
    prod["momentum"] = prod["product"].map(recent).fillna(0)-prod["product"].map(previous).fillna(0)
    cols = st.columns(5)
    with cols[0]: kpi("PRODUCT REVENUE",money(prod["revenue"].sum(),True),"Selected period")
    with cols[1]: kpi("UNITS SOLD",f'{prod["quantity"].sum():,.0f}',"Total quantity")
    with cols[2]: kpi("AVERAGE SELLING PRICE",money(prod["asp"].mean(),True),"Revenue / units")
    with cols[3]: kpi("FAST MOVING",f'{(prod["momentum"]>0).sum():,}',"Products gaining volume")
    with cols[4]: kpi("SLOW MOVING",f'{(prod["momentum"]<=0).sum():,}',"Flat or declining volume",True)
    section_gap()
    left,right=st.columns([1.05,1.1])
    with left:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        panel_header("Top products by revenue","Revenue ranking")
        fig=px.bar(prod.nlargest(10,"revenue").sort_values("revenue"),x="revenue",y="product",orientation="h",color="revenue",color_continuous_scale=["#315a78","#4dd8d0"])
        chart_layout(fig,330,False); fig.update_layout(coloraxis_showscale=False); fig.update_xaxes(tickprefix="₹",tickformat="~s")
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        panel_header("Revenue by category","Portfolio mix")
        fig=px.treemap(prod,path=["category","product"],values="revenue",color="revenue",color_continuous_scale=["#243c5a","#4dd8d0"])
        fig.update_traces(hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:,.0f}<extra></extra>",textfont=dict(size=12))
        chart_layout(fig,330,False)
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    left,right=st.columns(2)
    with left:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        panel_header("Product growth trend","Monthly revenue by leading products")
        leaders=prod.nlargest(5,"revenue")["product"].tolist()
        trend=monthly_prod[monthly_prod["product"].isin(leaders)]
        fig=px.line(trend,x="month",y="revenue",color="product",color_discrete_sequence=COLORS,markers=True)
        chart_layout(fig,310)
        fig.update_yaxes(tickprefix="₹",tickformat="~s")
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        panel_header("Quantity sold analysis","Units sold by product")
        q=prod.nlargest(10,"quantity").sort_values("quantity")
        fig=px.bar(q,x="product",y="quantity",color="quantity",color_continuous_scale=["#315a78","#b59aff"])
        chart_layout(fig,310,False); fig.update_layout(coloraxis_showscale=False); fig.update_xaxes(tickangle=-28)
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="panel">',unsafe_allow_html=True)
    panel_header("Product contribution","Share of total revenue by product")
    contribution=prod.sort_values("revenue",ascending=False).copy()
    contribution["share"]=contribution["revenue"]/max(contribution["revenue"].sum(),1)*100
    fig=px.bar(contribution,x="product",y="share",color="category",text=contribution["share"].map(lambda x:f"{x:.1f}%"))
    fig.update_traces(textposition="outside")
    chart_layout(fig,300)
    fig.update_yaxes(ticksuffix="%"); fig.update_xaxes(tickangle=-25)
    st.plotly_chart(fig,use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ============================================================
# PAGE 4 — CHURN & RISK
# ============================================================
elif selected_page == "Churn & Risk":
    page_header("04 / PREDICTIVE RISK", "Churn & Risk Analytics", "Surface customer warning signals early and quantify the revenue that needs protecting.")
    c=customers_all[customers_all["customer"].isin(filtered["customer"].unique())].copy()
    high=c[c["risk"]=="High"]
    total_risk=high["revenue_at_risk"].sum()
    avg_score=c["churn_score"].mean()*100 if len(c) else 0
    churned=(c["inactivity_days"]>120).sum()
    cols=st.columns(5)
    with cols[0]: kpi("HIGH-RISK CUSTOMERS",f"{len(high):,}","Priority accounts",True)
    with cols[1]: kpi("REVENUE AT RISK",money(total_risk,True),"High-risk exposure",True)
    with cols[2]: kpi("AVG. CHURN SCORE",f"{avg_score:.1f}%","Modelled risk index",avg_score>50)
    with cols[3]: kpi("CHURNED CUSTOMERS",f"{churned:,}","Inactive > 120 days",True)
    with cols[4]: kpi("RECOVERABLE REVENUE",money(c["recoverable_revenue"].sum(),True),"Estimated opportunity")
    section_gap()
    left,right=st.columns([.85,1.35])
    with left:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        panel_header("Churn distribution","Customers by risk tier")
        dist=c.groupby("risk",observed=False).size().reset_index(name="customers")
        fig=px.pie(dist,names="risk",values="customers",hole=.7,color="risk",color_discrete_map=RISK_COLORS)
        fig.update_traces(textinfo="percent",marker=dict(line=dict(color="#121a2b",width=3)))
        chart_layout(fig,310)
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        panel_header("Top customers at risk","Prioritised by estimated revenue exposure")
        risk_top=c.nlargest(10,"revenue_at_risk").sort_values("revenue_at_risk")
        fig=px.bar(risk_top,x="revenue_at_risk",y="customer",orientation="h",color="risk",color_discrete_map=RISK_COLORS)
        chart_layout(fig,310)
        fig.update_xaxes(tickprefix="₹",tickformat="~s")
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    left,right=st.columns(2)
    with left:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        panel_header("Revenue decline trend","Monthly revenue trajectory")
        rev=filtered.groupby("month",as_index=False)["revenue"].sum()
        rev["change"]=rev["revenue"].pct_change()*100
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=rev["month"],y=rev["revenue"],mode="lines+markers",line=dict(color="#ffb86b",width=3),fill="tozeroy",fillcolor="rgba(255,184,107,.10)",name="Revenue"))
        chart_layout(fig,300,False); fig.update_yaxes(tickprefix="₹",tickformat="~s")
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        panel_header("Customer inactivity distribution","Days since last purchase")
        fig=px.histogram(c,x="inactivity_days",nbins=18,color_discrete_sequence=["#729cff"])
        chart_layout(fig,300,False); fig.update_xaxes(title="Days inactive"); fig.update_yaxes(title="Customers")
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="panel">',unsafe_allow_html=True)
    panel_header("Risk heatmap","Customer count by inactivity and revenue-risk score")
    c["inactivity_band"]=pd.cut(c["inactivity_days"],[0,30,60,90,120,180,10000],labels=["0–30","31–60","61–90","91–120","121–180","180+"])
    c["score_band"]=pd.cut(c["churn_score"],[0,.2,.4,.6,.8,1.01],labels=["0–20%","20–40%","40–60%","60–80%","80–100%"],include_lowest=True)
    heat=c.groupby(["inactivity_band","score_band"],observed=False).size().reset_index(name="customers")
    pivot=heat.pivot(index="score_band",columns="inactivity_band",values="customers").fillna(0)
    fig=px.imshow(pivot,text_auto=True,aspect="auto",color_continuous_scale=["#172238","#315a78","#ffb86b","#ff7185"])
    chart_layout(fig,300,False)
    st.plotly_chart(fig,use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-label">Priority intervention queue</div>',unsafe_allow_html=True)
    queue=c.nlargest(10,"revenue_at_risk")[["customer","region","inactivity_days","churn_score","revenue_at_risk","recoverable_revenue"]].copy()
    queue["churn_score"]=queue["churn_score"].map(lambda x:f"{x:.0%}")
    queue["revenue_at_risk"]=queue["revenue_at_risk"].map(money)
    queue["recoverable_revenue"]=queue["recoverable_revenue"].map(money)
    queue=queue.rename(columns={"customer":"Customer","region":"Region","inactivity_days":"Inactive days","churn_score":"Churn score","revenue_at_risk":"Revenue at risk","recoverable_revenue":"Recoverable"})
    st.dataframe(queue,use_container_width=True,hide_index=True)

# ============================================================
# PAGE 5 — STRATEGIC BUSINESS INSIGHTS
# ============================================================
else:
    page_header("05 / DECISION INTELLIGENCE", "Strategic Business Insights", "Translate commercial signals into strategic priorities for leadership.")
    c=customers_all[customers_all["customer"].isin(filtered["customer"].unique())].copy()
    cust=filtered.groupby("customer",as_index=False)["revenue"].sum().sort_values("revenue",ascending=False)
    prod=filtered.groupby("product",as_index=False)["revenue"].sum().sort_values("revenue",ascending=False)
    top_cust_pct=cust.head(max(1,int(np.ceil(len(cust)*.1))))["revenue"].sum()/max(total_revenue,1)*100
    top_prod_pct=prod.head(max(1,int(np.ceil(len(prod)*.2))))["revenue"].sum()/max(total_revenue,1)*100
    dependency=(top_cust_pct*.55+top_prod_pct*.45)
    critical=int((c["risk"]=="High").sum())
    cols=st.columns(5)
    with cols[0]: kpi("TOP CUSTOMER SHARE",f"{top_cust_pct:.1f}%","Top 10% of customers")
    with cols[1]: kpi("TOP PRODUCT SHARE",f"{top_prod_pct:.1f}%","Top 20% of products")
    with cols[2]: kpi("DEPENDENCY SCORE",f"{dependency:.1f}/100","Concentration indicator",dependency>65)
    with cols[3]: kpi("CRITICAL ALERTS",f"{critical:,}","High-risk customer accounts",critical>0)
    with cols[4]: kpi("AI INSIGHTS","04","Generated from demo rules")
    section_gap()
    left,right=st.columns(2)
    with left:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        panel_header("Customer revenue concentration","Pareto distribution")
        p=cust.reset_index(drop=True); p["rank"]=np.arange(1,len(p)+1); p["cum"]=p["revenue"].cumsum()/max(p["revenue"].sum(),1)*100
        fig=make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(x=p["rank"],y=p["revenue"],name="Revenue",marker_color="#729cff"),secondary_y=False)
        fig.add_trace(go.Scatter(x=p["rank"],y=p["cum"],name="Cumulative %",line=dict(color="#4dd8d0",width=3)),secondary_y=True)
        chart_layout(fig,310); fig.update_yaxes(tickprefix="₹",tickformat="~s",secondary_y=False); fig.update_yaxes(ticksuffix="%",range=[0,105],secondary_y=True,showgrid=False)
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        panel_header("Product revenue concentration","Pareto distribution")
        p2=prod.reset_index(drop=True); p2["rank"]=np.arange(1,len(p2)+1); p2["cum"]=p2["revenue"].cumsum()/max(p2["revenue"].sum(),1)*100
        fig=make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(x=p2["rank"],y=p2["revenue"],name="Revenue",marker_color="#b59aff"),secondary_y=False)
        fig.add_trace(go.Scatter(x=p2["rank"],y=p2["cum"],name="Cumulative %",line=dict(color="#ffb86b",width=3)),secondary_y=True)
        chart_layout(fig,310); fig.update_yaxes(tickprefix="₹",tickformat="~s",secondary_y=False); fig.update_yaxes(ticksuffix="%",range=[0,105],secondary_y=True,showgrid=False)
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    left,right=st.columns(2)
    with left:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        panel_header("Revenue risk analysis","Customer value, inactivity and risk exposure")
        scatter=c.copy()
        fig=px.scatter(scatter,x="inactivity_days",y="revenue",size="revenue_at_risk",color="risk",hover_name="customer",
                       color_discrete_map=RISK_COLORS,size_max=38,opacity=.82)
        chart_layout(fig,330)
        fig.update_xaxes(title="Days inactive"); fig.update_yaxes(title="Lifetime revenue",tickprefix="₹",tickformat="~s")
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        panel_header("Executive risk matrix","Revenue value vs churn probability")
        fig=px.scatter(c,x="churn_score",y="revenue",size="revenue_at_risk",color="risk",hover_name="customer",
                       color_discrete_map=RISK_COLORS,size_max=34,opacity=.82)
        chart_layout(fig,330)
        fig.update_xaxes(title="Churn probability",tickformat=".0%"); fig.update_yaxes(title="Customer revenue",tickprefix="₹",tickformat="~s")
        fig.add_vline(x=.68,line_dash="dash",line_color="#ff7185",opacity=.6)
        fig.add_hline(y=c["revenue"].median(),line_dash="dash",line_color="#ffb86b",opacity=.6)
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-label">AI recommendation brief</div>',unsafe_allow_html=True)
    top_customer=cust.iloc[0]["customer"] if len(cust) else "—"
    top_product=prod.iloc[0]["product"] if len(prod) else "—"
    risk_value=c["revenue_at_risk"].sum()
    insights=[
        ("01 · CUSTOMER CONCENTRATION",f"The top 10% of customers contribute {top_cust_pct:.1f}% of revenue. Protect strategic accounts with executive ownership and relationship plans."),
        ("02 · PRODUCT DEPENDENCY",f"{top_prod_pct:.1f}% of revenue comes from the top 20% of products. Build substitutes, bundles and cross-sell paths to reduce portfolio dependency."),
        ("03 · CHURN EXPOSURE",f"Estimated customer revenue exposure is {money(risk_value,True)}. Prioritise high-value accounts with inactivity above 60 days for proactive outreach."),
        ("04 · GROWTH OPPORTUNITY",f"{top_customer} is the leading customer and {top_product} is the leading product in the selected period. Use these as anchors for retention and expansion plays."),
    ]
    a,b=st.columns(2)
    with a: insight(*insights[0]); section_gap(); insight(*insights[2])
    with b: insight(*insights[1]); section_gap(); insight(*insights[3])
    st.caption("AI recommendation cards are rule-based demonstration outputs. Connect an LLM and governed business context to generate production-grade recommendations.")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    '<div style="display:flex;justify-content:space-between;color:#71819b;font-size:.72rem;">'
    '<span>◈ NEXUS BUSINESS INTELLIGENCE</span><span>Confidential · Internal analytics</span></div>',
    unsafe_allow_html=True
)
