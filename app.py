import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart City Cloud Billing",
    page_icon="🏙️",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Dark navy background */
.stApp {
    background-color: #0B1120;
    color: #E8EDF5;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1F2D45;
}
[data-testid="stSidebar"] * {
    color: #C9D6E8 !important;
}

/* Hide default header */
header { visibility: hidden; }

/* KPI cards */
.kpi-card {
    background: linear-gradient(135deg, #162036 0%, #1A2A48 100%);
    border: 1px solid #243554;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 8px;
}
.kpi-label {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #6B8BB5;
    margin-bottom: 6px;
}
.kpi-value {
    font-family: 'Space Mono', monospace;
    font-size: 26px;
    font-weight: 700;
    color: #5BC4FF;
    line-height: 1;
}
.kpi-sub {
    font-size: 12px;
    color: #4A6A99;
    margin-top: 4px;
}

/* Section headers */
.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #5BC4FF;
    border-left: 3px solid #5BC4FF;
    padding-left: 12px;
    margin: 32px 0 16px 0;
}

/* Chart containers */
.chart-box {
    background: #111827;
    border: 1px solid #1F2D45;
    border-radius: 12px;
    padding: 16px;
}

/* Optimization rows */
.opt-row {
    background: #131F33;
    border: 1px solid #1F2D45;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Streamlit elements */
[data-testid="stMetric"] { display: none; }
div[data-testid="column"] > div { gap: 0 !important; }

.stSelectbox > div > div {
    background-color: #131F33 !important;
    border-color: #243554 !important;
    color: #C9D6E8 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Color palette ─────────────────────────────────────────────────────────────
COLORS = ['#5BC4FF','#FF6B6B','#FFD166','#06D6A0','#A78BFA',
          '#F97316','#34D399','#60A5FA','#F472B6','#FBBF24','#4ADE80','#E879F9']
BG       = '#0B1120'
CARD_BG  = '#111827'
TEXT     = '#E8EDF5'
SUBTEXT  = '#6B8BB5'
ACCENT   = '#5BC4FF'

plt.rcParams.update({
    'figure.facecolor' : BG,
    'axes.facecolor'   : CARD_BG,
    'axes.edgecolor'   : '#1F2D45',
    'text.color'       : TEXT,
    'axes.labelcolor'  : SUBTEXT,
    'xtick.color'      : SUBTEXT,
    'ytick.color'      : SUBTEXT,
    'axes.spines.top'  : False,
    'axes.spines.right': False,
    'axes.spines.left' : False,
    'axes.spines.bottom': False,
    'grid.color'       : '#1F2D45',
    'grid.linewidth'   : 0.6,
    'font.family'      : 'DejaVu Sans',
})

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('cloud_billing_2024.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

MONTH_ORDER = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏙️ Smart City Cloud")
    st.markdown("**Cost Intelligence 2024**")
    st.markdown("---")

    all_services = sorted(df['Service_Type'].unique())
    selected_services = st.multiselect(
        "Filter Services", all_services, default=all_services,
    )

    all_depts = sorted(df['Department'].unique())
    selected_depts = st.multiselect(
        "Filter Departments", all_depts, default=all_depts,
    )

    st.markdown("---")
    st.markdown('<div style="font-size:11px;color:#4A6A99;">Dataset: cloud_billing_2024.csv<br>Records: 144 rows · 10 columns<br>Period: Jan–Dec 2024</div>', unsafe_allow_html=True)

# ── Filter ────────────────────────────────────────────────────────────────────
dff = df[df['Service_Type'].isin(selected_services) & df['Department'].isin(selected_depts)]

# ── Title ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 24px 0 8px 0;">
  <div style="font-family:'Space Mono',monospace;font-size:11px;letter-spacing:3px;color:#5BC4FF;text-transform:uppercase;margin-bottom:6px;">Smart City Cloud Intelligence</div>
  <div style="font-family:'DM Sans',sans-serif;font-size:32px;font-weight:700;color:#E8EDF5;line-height:1.1;">Cloud Billing Cost Analysis</div>
  <div style="font-size:14px;color:#4A6A99;margin-top:6px;">Annual overview · 2024 · us-east-1</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border:none;border-top:1px solid #1F2D45;margin:8px 0 24px 0'>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Tab bar */
button[data-baseweb="tab"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #6B8BB5 !important;
    background: transparent !important;
    border: none !important;
    padding: 10px 20px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #5BC4FF !important;
    border-bottom: 2px solid #5BC4FF !important;
}
[data-testid="stTabPanel"] { padding-top: 24px; }
/* Sliders */
[data-testid="stSlider"] > div > div > div > div { background: #5BC4FF !important; }
/* Number inputs */
[data-testid="stNumberInput"] input {
    background: #131F33 !important;
    border-color: #243554 !important;
    color: #E8EDF5 !important;
}
</style>
""", unsafe_allow_html=True)

tab_dashboard, tab_calculator = st.tabs(["📊  Dashboard", "🧮  Cost Calculator"])

with tab_dashboard:
    # ── KPI Row ──────────────────────────────────────────────────────────────────
    annual   = dff['Total_Cost_USD'].sum()
    monthly  = annual / 12
    by_month_all = dff.groupby('Month')['Total_Cost_USD'].sum().reindex(MONTH_ORDER)
    growth   = ((by_month_all.iloc[-1] - by_month_all.iloc[0]) / by_month_all.iloc[0] * 100) if by_month_all.iloc[0] else 0

    k1, k2, k3, k4 = st.columns(4)
    for col, label, value, sub in [
        (k1, "Annual Spend",      f"${annual:,.0f}",   "Total 2024"),
        (k2, "Monthly Average",   f"${monthly:,.0f}",  "Avg per month"),
        (k3, "Services Active",   str(dff['Service_Type'].nunique()), "Cloud services"),
        (k4, "YoY Growth",        f"{growth:.1f}%",    "Jan → Dec trend"),
    ]:
        col.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # CHART 1 + 2  —  Service pie  &  Monthly bar
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">Cost Distribution</div>', unsafe_allow_html=True)

    col_pie, col_bar = st.columns([1, 1])

    # Pie — by service
    by_service = dff.groupby('Service_Type')['Total_Cost_USD'].sum().sort_values(ascending=False)

    with col_pie:
        fig, ax = plt.subplots(figsize=(6, 5), facecolor=BG)
        wedges, _, pcts = ax.pie(
            by_service.values,
            autopct='%1.1f%%',
            startangle=140,
            colors=COLORS[:len(by_service)],
            wedgeprops={'linewidth': 1.8, 'edgecolor': BG},
            pctdistance=0.78,
            explode=[0.03] * len(by_service),
        )
        for p in pcts:
            p.set_fontsize(8); p.set_color('white'); p.set_fontweight('bold')
        ax.legend(
            wedges,
            [f"{s}  ${c:,.0f}" for s, c in by_service.items()],
            loc='center left', bbox_to_anchor=(-0.55, 0.5),
            fontsize=7.5, framealpha=0, labelcolor=TEXT,
        )
        ax.set_title('Spend by Service Type', color=TEXT, fontsize=12, fontweight='bold', pad=12)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # Bar — monthly trend
    with col_bar:
        by_month = dff.groupby('Month')['Total_Cost_USD'].sum().reindex(MONTH_ORDER)
        fig, ax = plt.subplots(figsize=(6, 5), facecolor=BG)
        bars = ax.bar(
            [m[:3] for m in MONTH_ORDER],
            by_month.values,
            color=ACCENT, alpha=0.85, edgecolor=BG, width=0.65,
        )
        for i, bar in enumerate(bars):
            bar.set_alpha(0.5 + 0.5 * (i / 12))
        ax.set_title('Monthly Cloud Spend', color=TEXT, fontsize=12, fontweight='bold', pad=12)
        ax.set_ylabel('Cost (USD)', fontsize=9)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:,.0f}'))
        ax.tick_params(axis='x', labelsize=8)
        ax.yaxis.grid(True); ax.set_axisbelow(True)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # ═══════════════════════════════════════════════════════════════════════════
    # CHART 3  —  Monthly trend line
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">Monthly Trend & MoM Change</div>', unsafe_allow_html=True)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), facecolor=BG, sharex=True,
                                     gridspec_kw={'height_ratios': [2, 1], 'hspace': 0.08})

    x = range(12)
    ax1.fill_between(x, by_month.values, alpha=0.12, color=ACCENT)
    ax1.plot(x, by_month.values, color=ACCENT, lw=2.5, marker='o',
             markersize=7, markerfacecolor='#FF6B6B', markeredgecolor=BG, markeredgewidth=2)
    for xi, v in enumerate(by_month.values):
        ax1.annotate(f'${v:,.0f}', (xi, v), xytext=(0, 10), textcoords='offset points',
                     ha='center', fontsize=7.5, color=ACCENT)
    ax1.set_title('Monthly Spend + MoM Change', color=TEXT, fontsize=12, fontweight='bold', pad=10)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:,.0f}'))
    ax1.yaxis.grid(True); ax1.set_axisbelow(True)

    changes = by_month.diff().fillna(0)
    bar_colors = ['#06D6A0' if v >= 0 else '#FF6B6B' for v in changes]
    ax2.bar(x, changes.values, color=bar_colors, edgecolor=BG, width=0.6)
    ax2.axhline(0, color='#243554', lw=1)
    ax2.set_xticks(x); ax2.set_xticklabels([m[:3] for m in MONTH_ORDER], fontsize=8)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:+,.0f}'))
    ax2.yaxis.grid(True); ax2.set_axisbelow(True)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    # ═══════════════════════════════════════════════════════════════════════════
    # CHART 4 + 5  —  Department & Stacked bar
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">Department Breakdown & Service Mix</div>', unsafe_allow_html=True)

    col_dept, col_stack = st.columns([1, 1.4])

    by_dept = dff.groupby('Department')['Total_Cost_USD'].sum().sort_values(ascending=False)

    with col_dept:
        fig, ax = plt.subplots(figsize=(5, 5), facecolor=BG)
        wedges, _, pcts = ax.pie(
            by_dept.values,
            autopct='%1.0f%%',
            startangle=90,
            colors=COLORS[:len(by_dept)],
            wedgeprops={'linewidth': 2, 'edgecolor': BG, 'width': 0.58},
            pctdistance=0.78,
        )
        for p in pcts:
            p.set_fontsize(8); p.set_fontweight('bold')
        ax.text(0, 0, f'${by_dept.sum():,.0f}\nTotal',
                ha='center', va='center', fontsize=9, fontweight='bold', color=ACCENT)
        ax.legend(wedges, by_dept.index, loc='center left',
                  bbox_to_anchor=(-0.45, 0.5), fontsize=8, framealpha=0, labelcolor=TEXT)
        ax.set_title('Spend by Department', color=TEXT, fontsize=12, fontweight='bold', pad=12)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    with col_stack:
        pivot = (dff.pivot_table(values='Total_Cost_USD', index='Month',
                                  columns='Service_Type', aggfunc='sum', fill_value=0)
                   .reindex(MONTH_ORDER))
        pivot.index = [m[:3] for m in MONTH_ORDER]

        fig, ax = plt.subplots(figsize=(7, 5), facecolor=BG)
        pivot.plot(kind='bar', stacked=True, ax=ax,
                   color=COLORS[:len(pivot.columns)], edgecolor=BG, linewidth=0.3, width=0.72)
        ax.set_title('Monthly Spend by Service', color=TEXT, fontsize=12, fontweight='bold', pad=12)
        ax.set_xlabel('')
        ax.set_ylabel('Cost (USD)', fontsize=9)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:,.0f}'))
        ax.tick_params(axis='x', rotation=0, labelsize=8)
        ax.legend(title='Service', bbox_to_anchor=(1.01, 1), loc='upper left',
                  fontsize=7.5, framealpha=0, labelcolor=TEXT, title_fontsize=8)
        ax.yaxis.grid(True); ax.set_axisbelow(True)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # ═══════════════════════════════════════════════════════════════════════════
    # CHART 6  —  Heat map
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">Cost Heat Map — Month × Service</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(13, 5), facecolor=BG)
    im = ax.imshow(pivot.values, cmap='Blues', aspect='auto', vmin=0)
    ax.set_xticks(range(len(pivot.columns))); ax.set_xticklabels(pivot.columns, rotation=30, ha='right', fontsize=9)
    ax.set_yticks(range(len(pivot.index)));   ax.set_yticklabels(pivot.index, fontsize=9)

    thresh = pivot.values.max() * 0.5
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            v = pivot.values[i, j]
            color = 'white' if v > thresh else '#8AAFD4'
            ax.text(j, i, f'${v:.0f}', ha='center', va='center', fontsize=7.5,
                    color=color, fontweight='bold')

    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.ax.yaxis.set_tick_params(color=SUBTEXT)
    cbar.outline.set_edgecolor('#1F2D45')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=SUBTEXT, fontsize=8)
    ax.set_title('Monthly Cost Heat Map', color=TEXT, fontsize=13, fontweight='bold', pad=14)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    # ═══════════════════════════════════════════════════════════════════════════
    # OPTIMIZATION SECTION
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">Optimization Recommendations</div>', unsafe_allow_html=True)

    saving_lo = annual * 0.20
    saving_hi = annual * 0.30

    col_recs, col_savings = st.columns([2, 1])

    with col_recs:
        recs = [
            ("🗃️", "Storage Lifecycle Policies",  "Archive sensor data >90 days",       "~20% savings"),
            ("🤖", "AI/ML Batch Inference",        "Schedule CCTV jobs vs real-time",    "~30% savings"),
            ("💻", "Compute Right-sizing",         "Downsize VMs with <30% CPU util",    "~25% savings"),
            ("🌐", "CDN for Network Egress",       "Cache portal content at edge nodes", "~35% savings"),
            ("🗄️", "Reserved DB Instances",       "1-yr reserved vs on-demand pricing", "~40% savings"),
        ]
        for icon, title, desc, saving in recs:
            st.markdown(f"""
            <div style="background:#111827;border:1px solid #1F2D45;border-radius:8px;
                        padding:12px 16px;margin-bottom:8px;display:flex;
                        justify-content:space-between;align-items:center;">
              <div>
                <span style="font-size:16px;margin-right:10px;">{icon}</span>
                <span style="font-weight:600;color:#E8EDF5;font-size:14px;">{title}</span>
                <div style="color:#4A6A99;font-size:12px;margin-top:3px;padding-left:26px;">{desc}</div>
              </div>
              <div style="font-family:'Space Mono',monospace;font-size:12px;color:#06D6A0;
                          background:#0D2218;border:1px solid #0D3D24;padding:4px 10px;border-radius:20px;
                          white-space:nowrap;">{saving}</div>
            </div>""", unsafe_allow_html=True)

    with col_savings:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0D2218,#111827);border:1px solid #0D3D24;
                    border-radius:12px;padding:28px 24px;text-align:center;margin-top:0;">
          <div style="font-family:'Space Mono',monospace;font-size:10px;letter-spacing:2px;
                      color:#06D6A0;text-transform:uppercase;margin-bottom:16px;">Estimated Savings</div>
          <div style="font-family:'Space Mono',monospace;font-size:22px;font-weight:700;color:#06D6A0;">
            ${saving_lo:,.0f}<br><span style="font-size:14px;color:#4A6A99;">to</span><br>${saving_hi:,.0f}
          </div>
          <div style="color:#4A6A99;font-size:11px;margin-top:10px;">per year (20–30%)</div>
          <hr style="border:none;border-top:1px solid #0D3D24;margin:16px 0;">
          <div style="font-family:'Space Mono',monospace;font-size:10px;letter-spacing:2px;
                      color:#5BC4FF;text-transform:uppercase;margin-bottom:8px;">Optimized Target</div>
          <div style="font-family:'Space Mono',monospace;font-size:18px;font-weight:700;color:#5BC4FF;">
            ${annual - saving_hi:,.0f}–${annual - saving_lo:,.0f}
          </div>
          <div style="color:#4A6A99;font-size:11px;margin-top:6px;">annual target</div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — COST CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════════
with tab_calculator:

    # ── Actual per-service annual averages from dataset (used as defaults) ────
    svc_actuals = df.groupby('Service_Type')['Total_Cost_USD'].sum().to_dict()

    st.markdown('<div class="section-header">Service Cost Estimator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#6B8BB5;font-size:13px;margin-bottom:20px;">'
        'Adjust monthly usage per service. Defaults are pre-filled from your 2024 actuals (÷ 12).'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Service definitions: (label, unit, price_per_unit, default_units) ────
    # Prices are back-calculated from actuals so defaults match exactly.
    SERVICE_DEFS = {
        "Compute":        ("VM vCPU-hours/mo",    0.048,   None),
        "Storage":        ("GB stored/mo",         0.023,   None),
        "Database":       ("DB instance-hours/mo", 0.17,    None),
        "AI/ML":          ("GPU-hours/mo",         2.50,    None),
        "Network":        ("GB egress/mo",         0.085,   None),
        "IoT":            ("Messages (thousands)", 0.0012,  None),
        "Security":       ("Resources monitored",  12.00,   None),
        "Monitoring":     ("Metrics-hours/mo",     0.10,    None),
        "Serverless":     ("Invocations (millions)",0.20,   None),
        "Container":      ("Pod-hours/mo",         0.045,   None),
    }

    # Fill default units from actuals
    for svc, (unit, price, _) in SERVICE_DEFS.items():
        actual_annual = svc_actuals.get(svc, 0)
        default_units = round((actual_annual / 12) / price) if price else 0
        SERVICE_DEFS[svc] = (unit, price, max(1, default_units))

    # ── Grid of sliders ───────────────────────────────────────────────────────
    svc_list  = list(SERVICE_DEFS.keys())
    calc_totals = {}

    for row_start in range(0, len(svc_list), 3):
        cols = st.columns(3)
        for ci, svc in enumerate(svc_list[row_start:row_start + 3]):
            unit, price, default_units = SERVICE_DEFS[svc]
            max_val = default_units * 3
            with cols[ci]:
                st.markdown(
                    f'<div style="font-family:\'Space Mono\',monospace;font-size:10px;'
                    f'letter-spacing:1.5px;text-transform:uppercase;color:#5BC4FF;'
                    f'margin-bottom:4px;">{svc}</div>',
                    unsafe_allow_html=True,
                )
                units = st.slider(
                    unit,
                    min_value=0,
                    max_value=max(max_val, 100),
                    value=default_units,
                    key=f"calc_{svc}",
                )
                monthly_cost = units * price
                calc_totals[svc] = monthly_cost
                st.markdown(
                    f'<div style="font-family:\'Space Mono\',monospace;font-size:11px;'
                    f'color:#06D6A0;margin-top:2px;margin-bottom:12px;">'
                    f'${monthly_cost:,.2f} / mo &nbsp;·&nbsp; '
                    f'<span style="color:#4A6A99">${monthly_cost*12:,.0f}/yr</span></div>',
                    unsafe_allow_html=True,
                )

    # ── Summary KPIs ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Estimated Budget Summary</div>', unsafe_allow_html=True)

    calc_monthly_total = sum(calc_totals.values())
    calc_annual_total  = calc_monthly_total * 12
    actual_annual_total = df['Total_Cost_USD'].sum()
    delta_vs_actual = calc_annual_total - actual_annual_total
    delta_pct       = (delta_vs_actual / actual_annual_total * 100) if actual_annual_total else 0

    ck1, ck2, ck3, ck4 = st.columns(4)
    for col, label, value, sub in [
        (ck1, "Est. Monthly Total",  f"${calc_monthly_total:,.0f}",  "All services combined"),
        (ck2, "Est. Annual Total",   f"${calc_annual_total:,.0f}",   "12 × monthly"),
        (ck3, "vs 2024 Actuals",     f"{'▲' if delta_vs_actual >= 0 else '▼'} ${abs(delta_vs_actual):,.0f}",
              f"{'Over' if delta_vs_actual >= 0 else 'Under'} by {abs(delta_pct):.1f}%"),
        (ck4, "Budget Efficiency",   f"{100 - abs(delta_pct):.1f}%",  "Alignment with actuals"),
    ]:
        val_color = '#FF6B6B' if (label == 'vs 2024 Actuals' and delta_vs_actual > 0) else \
                    '#06D6A0' if (label == 'vs 2024 Actuals' and delta_vs_actual <= 0) else '#5BC4FF'
        col.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value" style="color:{val_color};">{value}</div>
          <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

    # ── Side-by-side bar: Estimated vs Actual ─────────────────────────────────
    st.markdown('<div class="section-header">Estimated vs Actual — By Service</div>', unsafe_allow_html=True)

    est_annual  = {svc: v * 12 for svc, v in calc_totals.items()}
    act_annual  = {svc: svc_actuals.get(svc, 0) for svc in svc_list}

    fig, ax = plt.subplots(figsize=(13, 5), facecolor=BG)
    x_pos  = np.arange(len(svc_list))
    width  = 0.38

    bars_est = ax.bar(x_pos - width / 2,
                      [est_annual[s] for s in svc_list],
                      width, label='Estimated', color=ACCENT,   alpha=0.85, edgecolor=BG)
    bars_act = ax.bar(x_pos + width / 2,
                      [act_annual[s] for s in svc_list],
                      width, label='2024 Actual', color='#A78BFA', alpha=0.85, edgecolor=BG)

    for bar in bars_est:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, h + 20,
                    f'${h:,.0f}', ha='center', fontsize=6.5, color=ACCENT)
    for bar in bars_act:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, h + 20,
                    f'${h:,.0f}', ha='center', fontsize=6.5, color='#A78BFA')

    ax.set_xticks(x_pos)
    ax.set_xticklabels(svc_list, fontsize=9, rotation=20, ha='right')
    ax.set_ylabel('Annual Cost (USD)', fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:,.0f}'))
    ax.legend(framealpha=0, labelcolor=TEXT, fontsize=9)
    ax.yaxis.grid(True); ax.set_axisbelow(True)
    ax.set_title('Annual Cost: Estimated vs 2024 Actual', color=TEXT, fontsize=13, fontweight='bold', pad=14)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:48px;padding-top:16px;border-top:1px solid #1F2D45;
            text-align:center;font-size:11px;color:#2D4060;">
  Smart City Cloud Cost Intelligence · 2024 · Built with Streamlit + Pandas + Matplotlib
</div>
""", unsafe_allow_html=True)
