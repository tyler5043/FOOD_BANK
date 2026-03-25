import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CalFoodConnect",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Outfit:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0c2340;
}
section[data-testid="stSidebar"] * { color: white !important; }
section[data-testid="stSidebar"] .stRadio label {
    font-size: 1rem !important;
    padding: 8px 0;
}

/* Main background */
.main { background: #eef2f7; }

/* Hero banner */
.hero {
    background: linear-gradient(130deg, #0c2340 0%, #134d7a 55%, #0d8a76 100%);
    border-radius: 16px;
    padding: 52px 56px;
    color: white;
    margin-bottom: 28px;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    margin-bottom: 10px;
    line-height: 1.2;
}
.hero p { font-size: 1.05rem; opacity: .85; }

/* Metric cards */
.metric-card {
    background: white;
    border-radius: 14px;
    padding: 24px 22px;
    box-shadow: 0 4px 24px rgba(12,35,64,.09);
    border-left: 5px solid #0d8a76;
    margin-bottom: 16px;
}
.metric-card .icon { font-size: 1.6rem; margin-bottom: 6px; }
.metric-card .label {
    font-size: .72rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: .07em; color: #64748b; margin-bottom: 4px;
}
.metric-card .value {
    font-family: 'Playfair Display', serif;
    font-size: 2.1rem; color: #0c2340;
}

/* Tag pills */
.tag-ok   { background:#dcfce7; color:#166534; padding:3px 10px; border-radius:99px; font-size:.75rem; font-weight:700; }
.tag-low  { background:#fef9c3; color:#854d0e; padding:3px 10px; border-radius:99px; font-size:.75rem; font-weight:700; }
.tag-crit { background:#fee2e2; color:#991b1b; padding:3px 10px; border-radius:99px; font-size:.75rem; font-weight:700; }

/* Section headers */
.sec-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem; color: #0c2340; margin-bottom: 4px;
}
.sec-sub { color: #64748b; font-size: .9rem; margin-bottom: 20px; }

/* Bank cards */
.bank-card {
    background: white;
    border-radius: 14px;
    padding: 20px 22px;
    box-shadow: 0 4px 20px rgba(12,35,64,.08);
    border-left: 5px solid #0d8a76;
    margin-bottom: 14px;
}
.bank-card .bname { font-weight: 700; font-size: 1rem; color: #0c2340; }
.bank-card .bmeta { font-size: .82rem; color: #64748b; margin-top: 4px; }

/* Check-in result box */
.ci-box {
    background: #dcfce7;
    border-radius: 12px;
    padding: 20px 24px;
    border-left: 5px solid #22c55e;
    margin-top: 16px;
}
.ci-box p { color: #166534; font-weight: 600; font-size: 1rem; }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    rows = [
        ("SF Food Bank",       "Rice",          320, 14, 45,  "OK"),
        ("SF Food Bank",       "Canned Beans",  180,  5, 30,  "Low"),
        ("SF Food Bank",       "Pasta",         240, 21, 25,  "OK"),
        ("SF Food Bank",       "Bread",          60,  3, 40,  "Critical"),
        ("SF Food Bank",       "Cooking Oil",    90, 18, 15,  "OK"),
        ("SF Food Bank",       "Canned Corn",   110,  6, 20,  "Low"),
        ("SF Food Bank",       "Baby Formula",   40,  4, 10,  "Critical"),
        ("LA Regional Bank",   "Rice",          500, 20, 80,  "OK"),
        ("LA Regional Bank",   "Canned Tuna",   200,  7, 35,  "Low"),
        ("LA Regional Bank",   "Pasta",         310, 15, 50,  "OK"),
        ("LA Regional Bank",   "Bread",          80,  2, 60,  "Critical"),
        ("LA Regional Bank",   "Milk (UHT)",    150,  9, 40,  "Low"),
        ("LA Regional Bank",   "Cereal",        220, 25, 30,  "OK"),
        ("LA Regional Bank",   "Peanut Butter",  95, 11, 20,  "OK"),
        ("Sacramento Harvest", "Rice",          180, 30, 30,  "OK"),
        ("Sacramento Harvest", "Canned Soup",   140,  6, 25,  "Low"),
        ("Sacramento Harvest", "Pasta",         160, 22, 20,  "OK"),
        ("Sacramento Harvest", "Bread",          45,  4, 35,  "Critical"),
        ("Sacramento Harvest", "Eggs",           70,  3, 28,  "Critical"),
        ("Sacramento Harvest", "Oatmeal",       120, 18, 15,  "OK"),
        ("San Diego Share",    "Canned Beans",  230, 12, 40,  "OK"),
        ("San Diego Share",    "Rice",          280, 16, 55,  "OK"),
        ("San Diego Share",    "Bread",          55,  5, 45,  "Low"),
        ("San Diego Share",    "Baby Formula",   30,  3,  8,  "Critical"),
        ("San Diego Share",    "Pasta",         190, 20, 25,  "OK"),
        ("San Diego Share",    "Canned Corn",   100,  7, 18,  "Low"),
        ("Oakland Community",  "Rice",          210, 11, 38,  "OK"),
        ("Oakland Community",  "Canned Tuna",   130,  6, 22,  "Low"),
        ("Oakland Community",  "Bread",          35,  2, 30,  "Critical"),
        ("Oakland Community",  "Cereal",        180, 19, 25,  "OK"),
        ("Oakland Community",  "Peanut Butter",  75, 14, 18,  "OK"),
        ("Oakland Community",  "Cooking Oil",    60,  8, 12,  "Low"),
        ("Fresno Food Net",    "Rice",          400, 25, 65,  "OK"),
        ("Fresno Food Net",    "Pasta",         270, 17, 35,  "OK"),
        ("Fresno Food Net",    "Bread",          90,  4, 50,  "Critical"),
        ("Fresno Food Net",    "Canned Beans",  160, 10, 28,  "OK"),
        ("Fresno Food Net",    "Milk (UHT)",    110,  6, 32,  "Low"),
        ("Fresno Food Net",    "Oatmeal",        95, 22, 14,  "OK"),
        ("San Jose Pantry",    "Rice",          290, 13, 48,  "OK"),
        ("San Jose Pantry",    "Canned Soup",   170,  5, 30,  "Low"),
        ("San Jose Pantry",    "Bread",          50,  3, 38,  "Critical"),
        ("San Jose Pantry",    "Baby Formula",   25,  4,  7,  "Critical"),
        ("San Jose Pantry",    "Pasta",         210, 19, 28,  "OK"),
        ("San Jose Pantry",    "Cereal",        140, 16, 20,  "OK"),
        ("Bakersfield Aid",    "Rice",          350, 18, 58,  "OK"),
        ("Bakersfield Aid",    "Canned Tuna",   155,  7, 26,  "Low"),
        ("Bakersfield Aid",    "Bread",          65,  5, 42,  "Low"),
        ("Bakersfield Aid",    "Pasta",         195, 20, 30,  "OK"),
        ("Bakersfield Aid",    "Cooking Oil",    80, 12, 16,  "OK"),
        ("Bakersfield Aid",    "Canned Corn",   120,  6, 22,  "Low"),
    ]
    df = pd.DataFrame(rows, columns=[
        "bank_name", "item_name", "quantity",
        "days_left", "avg_daily_demand", "supply_status"
    ])
    return df

df = load_data()

# ── Sidebar nav ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🥗 CalFoodConnect")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🏠 Home", "🏪 Food Banks", "📦 Inventory",
         "✅ Check In", "🔍 Network Search", "📈 Predictions"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        "<small style='opacity:.5'>Made for California food banks · 2026</small>",
        unsafe_allow_html=True,
    )

# ── Helper: status badge HTML ─────────────────────────────────────────────────
def status_badge(s):
    s = str(s)
    sl = s.lower()
    if "ok"   in sl: return f'<span class="tag-ok">OK</span>'
    if "low"  in sl: return f'<span class="tag-low">LOW</span>'
    if "crit" in sl: return f'<span class="tag-crit">CRITICAL</span>'
    return s

def days_badge(d):
    d = int(d)
    if d <= 3: return f'<span class="tag-crit">{d}d</span>'
    if d <= 7: return f'<span class="tag-low">{d}d</span>'
    return f'<span class="tag-ok">{d}d</span>'

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────────────────────────────────────
if page == "🏠 Home":

    st.markdown("""
    <div class="hero">
      <h1>Connecting California<br>Food Banks</h1>
      <p>Reducing waste · Ending hunger · Powered by community data</p>
    </div>
    """, unsafe_allow_html=True)

    # Metric cards
    expiring = df[df["days_left"] <= 7]
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="icon">🏪</div>
            <div class="label">Total Banks</div>
            <div class="value">{df['bank_name'].nunique()}</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="icon">⚠️</div>
            <div class="label">Expiring Soon</div>
            <div class="value">{len(expiring)}</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="icon">📦</div>
            <div class="label">Total Items</div>
            <div class="value">{df['quantity'].sum():,}</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        st.markdown(f"""<div class="metric-card">
            <div class="icon">🤝</div>
            <div class="label">Daily Demand</div>
            <div class="value">{df['avg_daily_demand'].sum():,}</div>
        </div>""", unsafe_allow_html=True)

    # Expiring alerts
    st.markdown("---")
    st.markdown(f'<p class="sec-title">⚠️ Expiring This Week <span style="background:#f5a623;color:#0c2340;font-size:.75rem;font-weight:700;padding:3px 12px;border-radius:99px;margin-left:10px">{len(expiring)} items</span></p>', unsafe_allow_html=True)

    alert_df = expiring.sort_values("days_left")[["bank_name","item_name","quantity","days_left"]].head(15).copy()
    alert_df.columns = ["Food Bank", "Item", "Quantity", "Days Left"]
    st.dataframe(
        alert_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Days Left": st.column_config.NumberColumn(format="%d days"),
            "Quantity":  st.column_config.NumberColumn(format="%d"),
        }
    )

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: FOOD BANKS
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🏪 Food Banks":

    st.markdown('<p class="sec-title">Food Banks</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">All registered partner organizations</p>', unsafe_allow_html=True)

    banks = df["bank_name"].unique()
    cols = st.columns(2)

    for i, bank in enumerate(banks):
        subset   = df[df["bank_name"] == bank]
        total    = subset["quantity"].sum()
        critical = len(subset[subset["supply_status"] == "Critical"])
        low      = len(subset[subset["supply_status"] == "Low"])
        warn     = f" · ⚠️ {critical} critical" if critical else ""
        warn    += f" · 🟡 {low} low" if low else ""

        with cols[i % 2]:
            st.markdown(f"""<div class="bank-card">
                <div class="bname">🏪 {bank}</div>
                <div class="bmeta">{len(subset)} items · {total:,} units{warn}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p class="sec-title">Per-Bank Summary</p>', unsafe_allow_html=True)

    summary = df.groupby("bank_name").agg(
        Items=("item_name","count"),
        Total_Quantity=("quantity","sum"),
        Daily_Demand=("avg_daily_demand","sum"),
        Critical_Items=("supply_status", lambda x: (x=="Critical").sum()),
    ).reset_index().rename(columns={"bank_name":"Food Bank","Total_Quantity":"Total Qty","Daily_Demand":"Daily Demand","Critical_Items":"Critical ⚠️"})

    st.dataframe(summary, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: INVENTORY
# ─────────────────────────────────────────────────────────────────────────────
elif page == "📦 Inventory":

    st.markdown('<p class="sec-title">Inventory Explorer</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        bank_filter = st.selectbox("Filter by Food Bank", ["All"] + list(df["bank_name"].unique()))
    with col2:
        item_filter = st.text_input("Filter by Item", placeholder="e.g. Rice, Bread…")
    with col3:
        status_filter = st.selectbox("Status", ["All", "OK", "Low", "Critical"])

    filtered = df.copy()
    if bank_filter != "All":
        filtered = filtered[filtered["bank_name"] == bank_filter]
    if item_filter:
        filtered = filtered[filtered["item_name"].str.contains(item_filter, case=False)]
    if status_filter != "All":
        filtered = filtered[filtered["supply_status"] == status_filter]

    st.markdown(f"**{len(filtered)} rows**", unsafe_allow_html=True)

    display = filtered[["bank_name","item_name","quantity","days_left","avg_daily_demand","supply_status"]].copy()
    display.columns = ["Food Bank","Item","Quantity","Days Left","Daily Demand","Status"]

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Quantity":     st.column_config.NumberColumn(format="%d"),
            "Days Left":    st.column_config.NumberColumn(format="%d days"),
            "Daily Demand": st.column_config.NumberColumn(format="%d/day"),
            "Status": st.column_config.TextColumn(),
        }
    )

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: CHECK-IN
# ─────────────────────────────────────────────────────────────────────────────
elif page == "✅ Check In":

    st.markdown('<p class="sec-title">Family Check-In</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">Record families visiting today</p>', unsafe_allow_html=True)

    # Session state counters
    if "fam_count" not in st.session_state: st.session_state.fam_count = 0
    if "ppl_count" not in st.session_state: st.session_state.ppl_count = 0
    if "log"       not in st.session_state: st.session_state.log       = []

    col_form, col_stats = st.columns([1.2, 1])

    with col_form:
        with st.form("checkin_form"):
            bank = st.selectbox("Food Bank", df["bank_name"].unique())
            size = st.number_input("Family Size", min_value=1, max_value=12, value=2)
            submitted = st.form_submit_button("✅ Check In Family", use_container_width=True)

        if submitted:
            st.session_state.fam_count += 1
            st.session_state.ppl_count += size
            st.session_state.log.append({"Bank": bank, "Family Size": int(size)})
            st.success(f"✔ Family of {size} checked in at {bank}!")

    with col_stats:
        st.markdown(f"""<div class="metric-card">
            <div class="icon">👨‍👩‍👧</div>
            <div class="label">Families Today</div>
            <div class="value">{st.session_state.fam_count}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="metric-card">
            <div class="icon">🤝</div>
            <div class="label">People Today</div>
            <div class="value">{st.session_state.ppl_count}</div>
        </div>""", unsafe_allow_html=True)

    if st.session_state.log:
        st.markdown("---")
        st.markdown("**Today's Check-In Log**")
        st.dataframe(
            pd.DataFrame(st.session_state.log),
            use_container_width=True,
            hide_index=True,
        )
        if st.button("🗑 Reset Today's Count"):
            st.session_state.fam_count = 0
            st.session_state.ppl_count = 0
            st.session_state.log = []
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: NETWORK SEARCH
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🔍 Network Search":

    st.markdown('<p class="sec-title">Network Search</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">Find any item across all food banks</p>', unsafe_allow_html=True)

    query = st.text_input("Search for an item", placeholder="e.g. Rice, Baby Formula, Bread…")

    if query:
        results = df[
            df["item_name"].str.contains(query, case=False) |
            df["bank_name"].str.contains(query, case=False)
        ][["bank_name","item_name","quantity","days_left","supply_status"]].copy()
        results.columns = ["Food Bank","Item","Quantity","Days Left","Status"]

        if results.empty:
            st.warning(f'No results found for "{query}"')
        else:
            st.success(f"Found **{len(results)}** result(s) for **{query}**")
            st.dataframe(
                results,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Quantity":  st.column_config.NumberColumn(format="%d"),
                    "Days Left": st.column_config.NumberColumn(format="%d days"),
                }
            )
    else:
        st.info("Type an item name above to search across all food banks.")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: PREDICTIONS
# ─────────────────────────────────────────────────────────────────────────────
elif page == "📈 Predictions":

    st.markdown('<p class="sec-title">Predictions & Analytics</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">Supply vs demand, expiry risk, and item distribution</p>', unsafe_allow_html=True)

    # ── Chart 1: Supply vs Weekly Demand per bank ──
    grouped = df.groupby("bank_name").agg(
        Supply=("quantity","sum"),
        Weekly_Demand=("avg_daily_demand", lambda x: x.sum() * 7),
    ).reset_index()

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name="Supply (units)", x=grouped["bank_name"], y=grouped["Supply"],   marker_color="#0d8a76"))
    fig1.add_trace(go.Bar(name="Weekly Demand",  x=grouped["bank_name"], y=grouped["Weekly_Demand"], marker_color="#f5a623"))
    fig1.update_layout(
        barmode="group", title="Supply vs Weekly Demand by Food Bank",
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Outfit, sans-serif", color="#0c2340"),
        legend=dict(orientation="h", y=-0.22),
        margin=dict(t=50, b=80, l=60, r=20),
        xaxis=dict(tickangle=-20),
    )
    st.plotly_chart(fig1, use_container_width=True)

    col_a, col_b = st.columns(2)

    # ── Chart 2: Status breakdown pie ──
    with col_a:
        status_counts = df["supply_status"].value_counts().reset_index()
        status_counts.columns = ["Status","Count"]
        colors = {"OK":"#0d8a76","Low":"#f5a623","Critical":"#e84040"}
        fig2 = px.pie(
            status_counts, names="Status", values="Count",
            color="Status", color_discrete_map=colors,
            title="Inventory Status Breakdown",
            hole=0.45,
        )
        fig2.update_layout(font=dict(family="Outfit, sans-serif", color="#0c2340"), paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    # ── Chart 3: Days left distribution ──
    with col_b:
        fig3 = px.histogram(
            df, x="days_left", nbins=15,
            title="Days Until Expiry — Distribution",
            color_discrete_sequence=["#134d7a"],
            labels={"days_left":"Days Left"},
        )
        fig3.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Outfit, sans-serif", color="#0c2340"),
            bargap=0.08,
        )
        st.plotly_chart(fig3, use_container_width=True)

    # ── Chart 4: Top items by quantity ──
    top_items = df.groupby("item_name")["quantity"].sum().sort_values(ascending=True).tail(10)
    fig4 = go.Figure(go.Bar(
        x=top_items.values, y=top_items.index,
        orientation="h", marker_color="#0d8a76",
    ))
    fig4.update_layout(
        title="Top 10 Items by Total Quantity",
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Outfit, sans-serif", color="#0c2340"),
        margin=dict(l=140, r=20, t=50, b=40),
    )
    st.plotly_chart(fig4, use_container_width=True)