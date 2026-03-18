import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import json

st.set_page_config(
    page_title="Muyuan Foods (002714 CH) — Investment Dashboard",
    page_icon="🐷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS — Dark TradingView Theme ──
st.markdown("""
<style>
    /* ─── Global dark background ─── */
    .stApp, .main, [data-testid="stAppViewContainer"] { background-color: #0a0e17 !important; }
    .main .block-container { padding-top: 1rem; max-width: 1400px; }
    html, body, .stApp { color: #d1d4dc; }

    /* ─── Sidebar ─── */
    div[data-testid="stSidebar"] { background: #131722 !important; border-right: 1px solid #2a2e39 !important; }
    div[data-testid="stSidebar"] * { color: #d1d4dc !important; }
    div[data-testid="stSidebar"] .stSelectbox label { color: #d1d4dc !important; }
    div[data-testid="stSidebar"] hr { border-color: #2a2e39 !important; }

    /* ─── Headers ─── */
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    p, span, label, .stMarkdown { color: #d1d4dc; }

    /* ─── Horizontal rules ─── */
    hr { border-color: #2a2e39 !important; }

    /* ─── Metric cards (Signal Dashboard) ─── */
    .metric-card {
        background: linear-gradient(135deg, #1e222d 0%, #2a2e39 100%);
        padding: 1.2rem; border-radius: 8px; color: #d1d4dc; text-align: center;
        border: 1px solid #363a45;
    }
    .metric-card h3 { margin: 0; font-size: 0.85rem; opacity: 0.7; font-weight: 400; color: #787b86 !important; }
    .metric-card h1 { margin: 0.3rem 0 0 0; font-size: 1.8rem; font-weight: 700; color: #ffffff !important; }

    /* ─── Signal badges ─── */
    .signal-buy { background: rgba(38,166,154,0.2); color: #26a69a; padding: 6px 16px; border-radius: 20px; font-weight: 700; display: inline-block; border: 1px solid #26a69a40; }
    .signal-accumulate { background: rgba(38,166,154,0.12); color: #26a69a; padding: 6px 16px; border-radius: 20px; font-weight: 700; display: inline-block; border: 1px solid #26a69a30; }
    .signal-hold { background: rgba(255,152,0,0.15); color: #ff9800; padding: 6px 16px; border-radius: 20px; font-weight: 700; display: inline-block; border: 1px solid #ff980030; }
    .signal-reduce { background: rgba(239,83,80,0.15); color: #ef5350; padding: 6px 16px; border-radius: 20px; font-weight: 700; display: inline-block; border: 1px solid #ef535030; }

    /* ─── Info boxes ─── */
    .info-box {
        background: #1e222d; border-left: 4px solid #2962ff; padding: 12px 16px;
        border-radius: 0 8px 8px 0; margin: 8px 0; font-size: 0.9rem; color: #d1d4dc;
        border: 1px solid #2a2e39; border-left: 4px solid #2962ff;
    }
    .info-box strong { color: #ffffff; }

    /* ─── Streamlit native metrics ─── */
    [data-testid="stMetric"] { background: #1e222d; border: 1px solid #2a2e39; border-radius: 8px; padding: 12px 16px; }
    [data-testid="stMetricLabel"] { color: #787b86 !important; }
    [data-testid="stMetricLabel"] p { color: #787b86 !important; }
    [data-testid="stMetricValue"] { color: #ffffff !important; }

    /* ─── Dataframes / Tables ─── */
    [data-testid="stDataFrame"] { border: 1px solid #2a2e39; border-radius: 8px; overflow: hidden; }

    /* ─── Number inputs, text inputs ─── */
    .stNumberInput > div > div > input { background-color: #1e222d !important; color: #d1d4dc !important; border-color: #2a2e39 !important; }
    .stTextInput > div > div > input { background-color: #1e222d !important; color: #d1d4dc !important; border-color: #2a2e39 !important; }
    .stNumberInput label, .stTextInput label { color: #787b86 !important; }

    /* ─── Radio buttons ─── */
    .stRadio > label { color: #787b86 !important; }
    .stRadio [data-testid="stMarkdownContainer"] p { color: #d1d4dc !important; }

    /* ─── Expanders ─── */
    .streamlit-expanderHeader { background-color: #1e222d !important; color: #d1d4dc !important; border: 1px solid #2a2e39 !important; border-radius: 8px !important; }
    .streamlit-expanderContent { background-color: #131722 !important; border: 1px solid #2a2e39 !important; color: #d1d4dc !important; }
    details { background-color: #1e222d !important; border: 1px solid #2a2e39 !important; border-radius: 8px !important; }
    details summary { color: #d1d4dc !important; }
    details div { background-color: #131722 !important; }
    details p, details span { color: #d1d4dc !important; }

    /* ─── Tabs ─── */
    .stTabs [data-baseweb="tab-list"] { background-color: #131722; border-bottom: 1px solid #2a2e39; }
    .stTabs [data-baseweb="tab"] { color: #787b86; }

    /* ─── Plotly chart containers ─── */
    .js-plotly-plot .plotly { background: transparent !important; }

    /* ─── Captions ─── */
    .stCaption, [data-testid="stCaptionContainer"] { color: #4a4e59 !important; }
    [data-testid="stCaptionContainer"] p { color: #4a4e59 !important; }

    /* ─── Markdown tables ─── */
    table { border-collapse: collapse; width: 100%; }
    th { background-color: #1e222d !important; color: #787b86 !important; border-bottom: 1px solid #2a2e39 !important; padding: 8px 12px !important; }
    td { background-color: #131722 !important; color: #d1d4dc !important; border-bottom: 1px solid #2a2e39 !important; padding: 8px 12px !important; }
    tr:hover td { background-color: #1e222d !important; }

    /* ─── Scrollbar ─── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0a0e17; }
    ::-webkit-scrollbar-thumb { background: #2a2e39; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #363a45; }

    /* ─── Toast / alerts ─── */
    .stAlert { background-color: #1e222d !important; border: 1px solid #2a2e39 !important; color: #d1d4dc !important; }
</style>
""", unsafe_allow_html=True)

# ── Dark Plotly template ──
DARK_LAYOUT = dict(
    paper_bgcolor='#0a0e17',
    plot_bgcolor='#131722',
    font=dict(color='#787b86', family='Inter, sans-serif', size=12),
    title_font=dict(color='#d1d4dc', size=14),
    xaxis=dict(gridcolor='rgba(42,46,57,0.19)', zerolinecolor='#2a2e39', tickfont=dict(color='#787b86'), title_font=dict(color='#787b86')),
    yaxis=dict(gridcolor='rgba(42,46,57,0.19)', zerolinecolor='#2a2e39', tickfont=dict(color='#787b86'), title_font=dict(color='#787b86')),
)

DARK_LEGEND = dict(font=dict(color='#d1d4dc'), bgcolor='rgba(0,0,0,0)', orientation="h", y=-0.15)


def signal_badge(signal: str) -> str:
    cls = signal.lower().replace(" ", "-")
    if cls in ("buy", "accumulate", "bullish", "oversold"):
        return f'<span class="signal-buy">{signal}</span>'
    elif cls in ("hold", "watch", "neutral"):
        return f'<span class="signal-hold">{signal}</span>'
    else:
        return f'<span class="signal-reduce">{signal}</span>'


def metric_card(title: str, value: str) -> str:
    return f'<div class="metric-card"><h3>{title}</h3><h1>{value}</h1></div>'


# ── Sidebar ──
with st.sidebar:
    st.markdown("## Muyuan Foods")
    st.markdown("**002714.SZ / 2714.HK**")
    st.markdown("---")
    page = st.radio(
        "Navigation",
        ["Signal Dashboard", "Market Charts", "P&L Drivers", "Broker Estimates", "Sensitivity", "Hog Cycle History", "Key Risks"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("##### Quick Reference")
    st.markdown("""
    - **5.0x** = Govt reserve trigger
    - **5.5x** = Current ratio
    - **7.0x** = Industry breakeven
    - **RMB 0.1/kg GP** = ~RMB 0.9bn NPAT
    """)
    st.markdown("---")
    st.caption("Data sources: BofA, UBS, GS, MS research reports (Mar 2026)")


# ════════════════════════════════════════════════════════════════
# PAGE 1: SIGNAL DASHBOARD
# ════════════════════════════════════════════════════════════════
if page == "Signal Dashboard":
    st.markdown("# Signal Dashboard")
    st.markdown("Real-time cycle indicators for entry/exit timing on Muyuan Foods.")

    # ── Top-level input metrics ──
    st.markdown("### Current Market Data")
    st.markdown("*Update these values to refresh all signals automatically.*")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        hog_price = st.number_input("Hog Spot Price (RMB/kg)", value=10.2, step=0.1, format="%.1f")
    with col2:
        corn_price = st.number_input("Corn Price (RMB/kg)", value=2.34, step=0.01, format="%.2f")
    with col3:
        soymeal_price = st.number_input("Soybean Meal (RMB/kg)", value=3.44, step=0.01, format="%.2f")
    with col4:
        sow_herd = st.number_input("Sow Herd (mn head)", value=39.6, step=0.1, format="%.1f")

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        sow_mom = st.number_input("Sow MoM Chg (%)", value=-1.0, step=0.1, format="%.1f")
    with col6:
        industry_profit = st.number_input("Industry Profit/Head (RMB)", value=-134, step=10)
    with col7:
        futures_near = st.number_input("Hog Futures Near (RMB/kg)", value=11.0, step=0.1, format="%.1f")
    with col8:
        futures_far = st.number_input("Hog Futures Far (RMB/kg)", value=13.5, step=0.1, format="%.1f")

    # ── Computed ratios ──
    hog_corn_ratio = hog_price / corn_price if corn_price > 0 else 0
    feed_price = corn_price * 0.65 + soymeal_price * 0.20 + 0.5  # rough blended feed
    hog_feed_ratio = hog_price / feed_price if feed_price > 0 else 0

    st.markdown("---")

    # ── Key metric cards ──
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card("Hog-to-Corn Ratio", f"{hog_corn_ratio:.1f}x"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("Hog-to-Feed Ratio", f"{hog_feed_ratio:.1f}x"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("Sow Herd", f"{sow_herd:.1f}mn"), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card("Futures Spread", f"{futures_far - futures_near:+.1f}"), unsafe_allow_html=True)

    st.markdown("")

    # ── Signal table ──
    st.markdown("### Cycle Position Signals")

    def get_hog_corn_signal(ratio):
        if ratio <= 5.0:
            return "BUY", "Below 5x: Govt reserve trigger = price floor. Asymmetric long setup."
        elif ratio <= 5.5:
            return "ACCUMULATE", "Near red line (5x). Watch for govt intervention signals."
        elif ratio <= 7.0:
            return "HOLD", "Loss-making zone. Sow culling likely accelerating."
        else:
            return "REDUCE", "Above breakeven. Farmers profitable, herd expanding."

    def get_industry_profit_signal(profit):
        if profit < -200:
            return "BUY", "Deep loss. Aggressive culling = supply crunch in 6-12 months."
        elif profit < 0:
            return "ACCUMULATE", "Industry loss-making. Sow liquidation underway."
        elif profit < 300:
            return "HOLD", "Modest profit. Stable herd dynamics."
        else:
            return "REDUCE", "High profit. Farmers restocking — supply wave ahead."

    def get_sow_signal(mom_pct):
        if mom_pct < -2.0:
            return "BUY", "Rapid destocking (>2% MoM). Strong contrarian buy signal."
        elif mom_pct < 0:
            return "ACCUMULATE", "Moderate destocking. Supply tightening ahead."
        elif mom_pct < 1.0:
            return "HOLD", "Stable herd. Neutral signal."
        else:
            return "REDUCE", "Herd expanding. Future oversupply risk."

    def get_price_signal(price):
        if price < 12:
            return "OVERSOLD", "Below industry cost. Unsustainable — price floor forming."
        elif price < 14:
            return "WATCH", "Near cost levels. Margin squeeze across industry."
        elif price < 17:
            return "NEUTRAL", "Mid-cycle range. Normal profitability."
        else:
            return "OVERBOUGHT", "Above cycle avg. Caution — supply response likely."

    signals = [
        ("Hog-to-Corn Ratio", f"{hog_corn_ratio:.1f}x", *get_hog_corn_signal(hog_corn_ratio)),
        ("Hog Spot Price", f"RMB {hog_price:.1f}/kg", *get_price_signal(hog_price)),
        ("Industry Profit/Head", f"RMB {industry_profit:+,}/head", *get_industry_profit_signal(industry_profit)),
        ("Sow Herd MoM Change", f"{sow_mom:+.1f}%", *get_sow_signal(sow_mom)),
    ]

    for indicator, value, signal, commentary in signals:
        col_a, col_b, col_c, col_d = st.columns([2, 1.2, 1, 4])
        with col_a:
            st.markdown(f"**{indicator}**")
        with col_b:
            st.markdown(f"`{value}`")
        with col_c:
            st.markdown(signal_badge(signal), unsafe_allow_html=True)
        with col_d:
            st.caption(commentary)

    st.markdown("---")

    # ── NDRC Mechanism gauge ──
    st.markdown("### Hog-to-Corn Ratio — NDRC Policy Zones")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=hog_corn_ratio,
        number={"suffix": "x", "font": {"size": 48, "color": "#ffffff"}},
        gauge={
            "axis": {"range": [3, 14], "tickwidth": 2, "tickcolor": "#363a45",
                     "tickvals": [3, 5, 5.5, 7, 9, 12, 14],
                     "ticktext": ["3x", "5x\nReserve", "5.5x\nNow", "7x\nBE", "9x", "12x\nRelease", "14x"],
                     "tickfont": {"color": "#787b86"}},
            "bar": {"color": "#f0b90b", "thickness": 0.3},
            "bgcolor": "#1e222d",
            "steps": [
                {"range": [3, 5], "color": "rgba(38,166,154,0.25)"},
                {"range": [5, 7], "color": "rgba(255,152,0,0.2)"},
                {"range": [7, 9], "color": "rgba(120,123,134,0.15)"},
                {"range": [9, 12], "color": "rgba(255,152,0,0.2)"},
                {"range": [12, 14], "color": "rgba(239,83,80,0.25)"},
            ],
            "threshold": {
                "line": {"color": "#ef5350", "width": 4},
                "thickness": 0.8,
                "value": 5.0,
            },
        },
    ))
    fig.update_layout(**DARK_LAYOUT)
    fig.update_layout(height=300, margin=dict(t=20, b=20, l=40, r=40))
    fig.add_annotation(x=0.15, y=0.15, text="Govt buys reserves<br>(Price floor)", showarrow=False, font=dict(size=10, color="#26a69a"))
    fig.add_annotation(x=0.85, y=0.15, text="Govt sells reserves<br>(Price cap)", showarrow=False, font=dict(size=10, color="#ef5350"))
    st.plotly_chart(fig, use_container_width=True)

    # ── Futures curve ──
    st.markdown("### Forward Curve Signal")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        spread = futures_far - futures_near
        if spread > 0:
            st.markdown(f'<div class="info-box"><strong>Contango: +RMB {spread:.1f}/kg</strong><br>Market pricing in price recovery. Bullish forward view.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="info-box"><strong>Backwardation: RMB {spread:.1f}/kg</strong><br>Market pricing near-term tightness. Watch for spot squeeze.</div>', unsafe_allow_html=True)
    with col_f2:
        fig_curve = go.Figure()
        fig_curve.add_trace(go.Bar(
            x=["Spot", "Near Futures", "Far Futures"],
            y=[hog_price, futures_near, futures_far],
            marker_color=["#ef5350", "#ff9800", "#26a69a"],
            text=[f"RMB {hog_price:.1f}", f"RMB {futures_near:.1f}", f"RMB {futures_far:.1f}"],
            textposition="outside",
            textfont=dict(color="#d1d4dc"),
        ))
        fig_curve.update_layout(height=250, yaxis_title="RMB/kg", showlegend=False, **DARK_LAYOUT)
        st.plotly_chart(fig_curve, use_container_width=True)


# ════════════════════════════════════════════════════════════════
# PAGE 2: MARKET CHARTS (TradingView-style)
# ════════════════════════════════════════════════════════════════
elif page == "Market Charts":
    st.markdown("# Market Charts")
    st.markdown("Interactive TradingView-style charts for cycle tracking. Data sourced from broker reports & Wind.")

    # ── KPI Strip ──
    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    with kpi1:
        st.metric("Hog Price", "¥10.2/kg", "-4.3 vs Mar-25")
    with kpi2:
        st.metric("Hog-Corn Ratio", "5.5x", "-1.5 vs BE", delta_color="inverse")
    with kpi3:
        st.metric("Sow Herd", "39.3mn", "-1.2mn YoY", delta_color="inverse")
    with kpi4:
        st.metric("Industry P/Head", "¥-134", "Loss since Jul-25", delta_color="inverse")
    with kpi5:
        st.metric("Muyuan Cost", "¥12.1/kg", "-1.9 vs 2024", delta_color="off")
    with kpi6:
        st.metric("Share Price", "¥49.74", "18 Mar 2026", delta_color="off")

    st.markdown("---")

    # ── Hero Chart: Hog-to-Corn Ratio vs Share Price ──
    st.markdown("### Hog-to-Corn Price Ratio vs Share Price")
    period = st.radio("Period", ["1Y", "3Y", "5Y", "ALL"], index=3, horizontal=True, key="hero_period")

    hero_html = """
    <div id="hero-chart" style="width:100%%;height:440px;background:#131722;border-radius:8px;overflow:hidden;"></div>
    <script src="https://unpkg.com/lightweight-charts@4.2.2/dist/lightweight-charts.standalone.production.js"></script>
    <script>
    const hogPrice = %s;
    const cornPrice = %s;
    const sharePriceRaw = %s;

    const el = document.getElementById('hero-chart');
    const chart = LightweightCharts.createChart(el, {
      width: el.clientWidth, height: 440,
      layout: { background: { type: 'solid', color: '#131722' }, textColor: '#787b86', fontFamily: "'Inter', sans-serif", fontSize: 11 },
      grid: { vertLines: { color: '#2a2e3918' }, horzLines: { color: '#2a2e3930' } },
      crosshair: { mode: LightweightCharts.CrosshairMode.Normal },
      leftPriceScale: { visible: true, borderColor: '#2a2e39', scaleMargins: { top: 0.08, bottom: 0.08 } },
      rightPriceScale: { visible: true, borderColor: '#2a2e39', scaleMargins: { top: 0.08, bottom: 0.08 } },
      timeScale: { borderColor: '#2a2e39', timeVisible: false, rightOffset: 3, barSpacing: 6 },
    });

    // Ratio
    const ratioSeries = chart.addLineSeries({ color: '#f0b90b', lineWidth: 2, priceScaleId: 'left', title: 'Ratio', lastValueVisible: true, priceLineVisible: false, crosshairMarkerRadius: 4 });
    const ratioData = Object.keys(hogPrice).sort().map(d => ({ time: d + '-01', value: +(hogPrice[d] / cornPrice[d]).toFixed(2) }));
    ratioSeries.setData(ratioData);
    ratioSeries.createPriceLine({ price: 5.0, color: '#ef5350', lineWidth: 1, lineStyle: LightweightCharts.LineStyle.Dashed, axisLabelVisible: true, title: '5.0x NDRC' });
    ratioSeries.createPriceLine({ price: 7.0, color: '#ff9800', lineWidth: 1, lineStyle: LightweightCharts.LineStyle.Dashed, axisLabelVisible: true, title: '7.0x BE' });

    // Share price
    const shareSeries = chart.addAreaSeries({ topColor: 'rgba(41,98,255,0.18)', bottomColor: 'rgba(41,98,255,0.02)', lineColor: '#2962ff', lineWidth: 2, priceScaleId: 'right', title: 'Price', lastValueVisible: true, priceLineVisible: false, crosshairMarkerRadius: 4 });
    const shareData = sharePriceRaw.map(d => ({ time: d[0] + '-01', value: d[1] }));
    shareSeries.setData(shareData);

    %s
    new ResizeObserver(entries => { chart.applyOptions({ width: entries[0].contentRect.width }); }).observe(el);
    </script>
    """

    hog_price_data = {"2015-01":13.2,"2015-03":11.6,"2015-06":13.5,"2015-09":16.8,"2015-12":16.5,"2016-01":17.2,"2016-03":18.5,"2016-06":20.5,"2016-09":17.8,"2016-12":16.3,"2017-01":17.0,"2017-03":15.0,"2017-06":13.5,"2017-09":14.0,"2017-12":14.5,"2018-01":15.4,"2018-03":11.5,"2018-06":11.0,"2018-09":13.2,"2018-12":13.0,"2019-01":12.0,"2019-03":12.5,"2019-06":16.5,"2019-09":27.0,"2019-12":33.0,"2020-01":36.0,"2020-03":35.5,"2020-06":33.0,"2020-09":35.0,"2020-12":33.0,"2021-01":36.0,"2021-03":28.0,"2021-06":18.0,"2021-09":12.5,"2021-12":16.0,"2022-01":14.5,"2022-03":12.5,"2022-06":15.5,"2022-09":23.0,"2022-12":18.0,"2023-01":15.5,"2023-03":14.5,"2023-06":14.0,"2023-09":15.8,"2023-12":13.5,"2024-01":14.0,"2024-03":14.8,"2024-06":17.5,"2024-09":18.0,"2024-12":15.0,"2025-01":16.0,"2025-03":14.5,"2025-06":14.0,"2025-07":13.5,"2025-09":12.5,"2025-12":11.5,"2026-01":11.0,"2026-02":10.8,"2026-03":10.2}
    corn_price_data = {"2015-01":2.20,"2015-03":2.18,"2015-06":2.15,"2015-09":2.00,"2015-12":1.85,"2016-01":1.82,"2016-03":1.85,"2016-06":1.88,"2016-09":1.65,"2016-12":1.55,"2017-01":1.55,"2017-03":1.60,"2017-06":1.65,"2017-09":1.60,"2017-12":1.68,"2018-01":1.72,"2018-03":1.72,"2018-06":1.72,"2018-09":1.80,"2018-12":1.80,"2019-01":1.78,"2019-03":1.80,"2019-06":1.88,"2019-09":1.85,"2019-12":1.82,"2020-01":1.82,"2020-03":1.90,"2020-06":2.05,"2020-09":2.30,"2020-12":2.60,"2021-01":2.70,"2021-03":2.75,"2021-06":2.72,"2021-09":2.55,"2021-12":2.60,"2022-01":2.65,"2022-03":2.80,"2022-06":2.85,"2022-09":2.80,"2022-12":2.85,"2023-01":2.80,"2023-03":2.72,"2023-06":2.60,"2023-09":2.58,"2023-12":2.40,"2024-01":2.35,"2024-03":2.30,"2024-06":2.30,"2024-09":2.22,"2024-12":2.25,"2025-01":2.28,"2025-03":2.30,"2025-06":2.32,"2025-07":2.31,"2025-09":2.30,"2025-12":2.32,"2026-01":2.32,"2026-02":2.32,"2026-03":2.34}
    share_price_raw = [["2018-01",13.92],["2018-02",11.37],["2018-03",10.57],["2018-04",11.15],["2018-05",12.30],["2018-06",10.38],["2018-07",11.23],["2018-08",9.65],["2018-09",10.46],["2018-10",9.62],["2018-11",11.35],["2018-12",12.08],["2019-01",14.52],["2019-02",18.82],["2019-03",26.60],["2019-04",26.93],["2019-05",26.62],["2019-06",24.70],["2019-07",32.18],["2019-08",33.78],["2019-09",29.62],["2019-10",41.39],["2019-11",36.47],["2019-12",37.31],["2020-01",34.33],["2020-02",48.95],["2020-03",51.30],["2020-04",53.65],["2020-05",50.40],["2020-06",58.63],["2020-07",65.34],["2020-08",62.54],["2020-09",52.81],["2020-10",50.65],["2020-11",55.00],["2020-12",55.07],["2021-01",63.50],["2021-02",81.36],["2021-03",71.45],["2021-04",80.79],["2021-05",63.63],["2021-06",60.82],["2021-07",42.27],["2021-08",42.31],["2021-09",51.90],["2021-10",57.11],["2021-11",52.40],["2021-12",53.36],["2022-01",54.59],["2022-02",57.08],["2022-03",56.86],["2022-04",52.23],["2022-05",51.18],["2022-06",55.27],["2022-07",59.60],["2022-08",58.62],["2022-09",54.52],["2022-10",46.78],["2022-11",48.07],["2022-12",48.75],["2023-01",49.94],["2023-02",49.54],["2023-03",49.00],["2023-04",47.87],["2023-05",40.05],["2023-06",42.15],["2023-07",44.45],["2023-08",40.58],["2023-09",37.89],["2023-10",37.76],["2023-11",39.08],["2023-12",41.18],["2024-01",35.25],["2024-02",38.49],["2024-03",43.15],["2024-04",43.62],["2024-05",47.15],["2024-06",43.60],["2024-07",43.72],["2024-08",38.56],["2024-09",46.31],["2024-10",43.64],["2024-11",40.73],["2024-12",38.44],["2025-01",37.21],["2025-02",36.29],["2025-03",38.73],["2025-04",39.67],["2025-05",40.44],["2025-06",42.01],["2025-07",46.36],["2025-08",54.96],["2025-09",53.00],["2025-10",50.30],["2025-11",50.75],["2025-12",50.58],["2026-01",46.00],["2026-02",46.90],["2026-03",49.74]]

    # Period filter logic
    if period == "1Y":
        range_js = "chart.timeScale().setVisibleRange({ from: '2025-03-01', to: '2026-03-18' });"
    elif period == "3Y":
        range_js = "chart.timeScale().setVisibleRange({ from: '2023-03-01', to: '2026-03-18' });"
    elif period == "5Y":
        range_js = "chart.timeScale().setVisibleRange({ from: '2021-03-01', to: '2026-03-18' });"
    else:
        range_js = "chart.timeScale().fitContent();"

    components.html(
        hero_html % (json.dumps(hog_price_data), json.dumps(corn_price_data), json.dumps(share_price_raw), range_js),
        height=460, scrolling=False
    )

    # Legend
    st.markdown("""
    <div style="display:flex;gap:24px;font-size:0.8rem;color:#888;margin-top:-8px;margin-bottom:16px;">
        <span><span style="color:#f0b90b;">●</span> Hog-to-Corn Ratio (LHS)</span>
        <span><span style="color:#2962ff;">●</span> Share Price (RHS)</span>
        <span style="color:#ef5350;">— — 5.0x NDRC trigger</span>
        <span style="color:#ff9800;">— — 7.0x breakeven</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── NDRC Mechanism ──
    st.markdown("### NDRC Hog-to-Corn Ratio Alert Mechanism")
    ndrc_html = """
    <div style="font-family:'Inter',system-ui,sans-serif;background:#131722;border-radius:8px;padding:16px 20px;">
      <div style="display:flex;gap:0;height:44px;border-radius:6px;overflow:hidden;margin-bottom:10px;">
        <div style="flex:1;background:rgba(239,83,80,0.56);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:500;color:#fff;text-align:center;line-height:1.1;border-radius:6px 0 0 6px;">&lt;5x<br>1st Alarm<br>Reserve Buy</div>
        <div style="flex:1;background:rgba(239,83,80,0.37);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:500;color:#fff;text-align:center;line-height:1.1;">5–6x 3wk<br>2nd Alarm<br>Reserve Buy</div>
        <div style="flex:1;background:rgba(255,152,0,0.25);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:500;color:#fff;text-align:center;line-height:1.1;">5–6x<br>3rd Alarm<br>Downside</div>
        <div style="flex:3;background:rgba(38,166,154,0.15);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:500;color:#fff;text-align:center;line-height:1.1;">6–9x Normal · 7.0 Breakeven</div>
        <div style="flex:1;background:rgba(255,152,0,0.25);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:500;color:#fff;text-align:center;line-height:1.1;">9–10x<br>3rd Alarm</div>
        <div style="flex:1;background:rgba(255,152,0,0.37);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:500;color:#fff;text-align:center;line-height:1.1;">10–12x<br>2nd Alarm</div>
        <div style="flex:1;background:rgba(239,83,80,0.56);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:500;color:#fff;text-align:center;line-height:1.1;border-radius:0 6px 6px 0;">&gt;12x<br>1st Alarm<br>Reserve Sell</div>
      </div>
      <div style="position:relative;width:100%%;height:4px;background:#2a2e39;border-radius:2px;margin-top:16px;">
        <div style="position:absolute;left:36.7%%;top:-20px;transform:translateX(-50%%);text-align:center;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;color:#f0b90b;">▼ 5.5x NOW</div>
          <div style="width:2px;height:20px;background:#f0b90b;margin:2px auto 0;"></div>
        </div>
      </div>
    </div>
    """
    components.html(ndrc_html, height=120, scrolling=False)

    st.markdown("---")

    # ── Secondary Charts Grid ──
    chart_template = """
    <div id="%s" style="width:100%%;height:300px;background:#131722;border-radius:8px;overflow:hidden;"></div>
    <script src="https://unpkg.com/lightweight-charts@4.2.2/dist/lightweight-charts.standalone.production.js"></script>
    <script>
    (function() {
      const el = document.getElementById('%s');
      const chart = LightweightCharts.createChart(el, {
        width: el.clientWidth, height: 300,
        layout: { background: { type: 'solid', color: '#131722' }, textColor: '#787b86', fontFamily: "'Inter', sans-serif", fontSize: 11 },
        grid: { vertLines: { color: '#2a2e3920' }, horzLines: { color: '#2a2e3940' } },
        crosshair: { mode: LightweightCharts.CrosshairMode.Normal },
        rightPriceScale: { borderColor: '#2a2e39', scaleMargins: { top: 0.1, bottom: 0.1 } },
        timeScale: { borderColor: '#2a2e39', timeVisible: false, rightOffset: 2, barSpacing: 8 },
      });
      %s
      chart.timeScale().fitContent();
      new ResizeObserver(entries => { chart.applyOptions({ width: entries[0].contentRect.width }); }).observe(el);
    })();
    </script>
    """

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Hog Price (Rmb/kg)")
        hog_js = """
        const data = %s;
        const series = chart.addLineSeries({ color: '#26a69a', lineWidth: 2, priceLineVisible: false, crosshairMarkerRadius: 3 });
        series.setData(Object.keys(data).sort().map(k => ({ time: k + '-01', value: data[k] })));
        """ % json.dumps(hog_price_data)
        components.html(chart_template % ("chart-hog", "chart-hog", hog_js), height=320, scrolling=False)

    with col_b:
        st.markdown("#### Corn Price (Rmb/kg)")
        corn_js = """
        const data = %s;
        const series = chart.addLineSeries({ color: '#ef5350', lineWidth: 2, priceLineVisible: false, crosshairMarkerRadius: 3 });
        series.setData(Object.keys(data).sort().map(k => ({ time: k + '-01', value: data[k] })));
        """ % json.dumps(corn_price_data)
        components.html(chart_template % ("chart-corn", "chart-corn", corn_js), height=320, scrolling=False)

    col_c, col_d = st.columns(2)

    sow_herd_data = {"2019-01":28.0,"2019-06":25.0,"2019-12":20.5,"2020-06":25.0,"2020-12":31.0,"2021-06":45.0,"2021-12":43.0,"2022-03":42.5,"2022-06":43.0,"2022-09":43.5,"2022-12":43.0,"2023-03":43.0,"2023-06":41.5,"2023-09":42.0,"2023-12":40.8,"2024-03":39.8,"2024-06":40.4,"2024-09":41.0,"2024-12":40.5,"2025-03":40.2,"2025-06":40.4,"2025-09":39.8,"2025-12":39.6,"2026-01":39.3}
    breeding_profit_data = {"2015-06":-200,"2015-12":200,"2016-06":800,"2016-12":400,"2017-06":100,"2017-12":-50,"2018-01":100,"2018-06":-200,"2018-12":-100,"2019-06":500,"2019-09":2200,"2019-12":3200,"2020-03":3000,"2020-06":2800,"2020-09":2500,"2020-12":2200,"2021-03":1800,"2021-06":200,"2021-09":-700,"2021-12":-200,"2022-03":-400,"2022-06":100,"2022-09":1200,"2022-12":400,"2023-03":100,"2023-06":-100,"2023-09":150,"2023-12":-200,"2024-03":-100,"2024-06":500,"2024-09":600,"2024-12":100,"2025-03":200,"2025-06":100,"2025-07":-50,"2025-09":-100,"2025-12":-200,"2026-01":-134,"2026-03":-300}

    with col_c:
        st.markdown("#### Sow Herd (mn head)")
        sow_js = """
        const data = %s;
        const series = chart.addLineSeries({ color: '#ab47bc', lineWidth: 2, priceLineVisible: false, crosshairMarkerRadius: 3 });
        series.setData(Object.keys(data).sort().map(k => ({ time: k + '-01', value: data[k] })));
        """ % json.dumps(sow_herd_data)
        components.html(chart_template % ("chart-sow", "chart-sow", sow_js), height=320, scrolling=False)

    with col_d:
        st.markdown("#### Industry Breeding Profit (Rmb/head)")
        profit_js = """
        const data = %s;
        const series = chart.addHistogramSeries({ priceLineVisible: false, base: 0 });
        series.setData(Object.keys(data).sort().map(k => ({ time: k + '-01', value: data[k], color: data[k] >= 0 ? '#26a69a' : '#ef5350' })));
        series.createPriceLine({ price: 0, color: '#787b8640', lineWidth: 1, lineStyle: LightweightCharts.LineStyle.Solid, axisLabelVisible: false });
        """ % json.dumps(breeding_profit_data)
        components.html(chart_template % ("chart-profit", "chart-profit", profit_js), height=320, scrolling=False)

    # ── Full-width: Unit Cost vs ASP ──
    st.markdown("#### Muyuan Unit Cost vs ASP (Rmb/kg — Annual)")
    unit_cost_data = {"2018":11.40,"2019":12.90,"2020":15.50,"2021":15.30,"2022":15.70,"2023":14.90,"2024":14.00,"2025":12.10,"2026":10.80,"2027":10.60}
    asp_data = {"2018":11.6,"2019":19.1,"2020":30.5,"2021":16.6,"2022":18.0,"2023":14.5,"2024":16.3,"2025":13.5,"2026":12.2,"2027":13.2}

    cost_asp_html = """
    <div id="chart-cost-asp" style="width:100%%;height:300px;background:#131722;border-radius:8px;overflow:hidden;"></div>
    <script src="https://unpkg.com/lightweight-charts@4.2.2/dist/lightweight-charts.standalone.production.js"></script>
    <script>
    (function() {
      const el = document.getElementById('chart-cost-asp');
      const chart = LightweightCharts.createChart(el, {
        width: el.clientWidth, height: 300,
        layout: { background: { type: 'solid', color: '#131722' }, textColor: '#787b86', fontFamily: "'Inter', sans-serif", fontSize: 11 },
        grid: { vertLines: { color: '#2a2e3920' }, horzLines: { color: '#2a2e3940' } },
        crosshair: { mode: LightweightCharts.CrosshairMode.Normal },
        rightPriceScale: { borderColor: '#2a2e39', scaleMargins: { top: 0.12, bottom: 0.12 } },
        timeScale: { borderColor: '#2a2e39', timeVisible: false, barSpacing: 40 },
      });

      const unitCost = %s;
      const asp = %s;

      function yearToSeries(dict) {
        return Object.keys(dict).sort().map(k => ({ time: parseInt(k) + '-07-01', value: dict[k] }));
      }

      const aspSer = chart.addLineSeries({ color: '#2962ff', lineWidth: 2, priceLineVisible: false, crosshairMarkerRadius: 4, title: 'ASP' });
      aspSer.setData(yearToSeries(asp));

      const costSer = chart.addLineSeries({ color: '#ef5350', lineWidth: 2, priceLineVisible: false, crosshairMarkerRadius: 4, lineStyle: LightweightCharts.LineStyle.Dashed, title: 'Unit Cost' });
      costSer.setData(yearToSeries(unitCost));

      chart.timeScale().fitContent();
      new ResizeObserver(entries => { chart.applyOptions({ width: entries[0].contentRect.width }); }).observe(el);
    })();
    </script>
    """
    components.html(cost_asp_html % (json.dumps(unit_cost_data), json.dumps(asp_data)), height=320, scrolling=False)

    st.markdown("""
    <div style="display:flex;gap:24px;font-size:0.8rem;color:#888;margin-top:-8px;">
        <span><span style="color:#2962ff;">●</span> ASP</span>
        <span><span style="color:#ef5350;">●</span> Unit Cost</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Gross Profit Sensitivity ──
    st.markdown("### Gross Profit Sensitivity")
    st.markdown("""
    <div style="background:#1e222d;border-radius:8px;padding:16px 20px;border:1px solid #2a2e39;font-size:0.9rem;">
        <p style="color:#d1d4dc;margin-bottom:12px;">
            Every <span style="color:#f0b90b;font-weight:700;font-family:monospace;">Rmb 0.1/kg</span> change in gross profit per kg =
            <span style="color:#f0b90b;font-weight:700;font-family:monospace;">~Rmb 0.9bn</span> NPAT impact
            <span style="color:#4a4e59;"> | </span>
            <span style="color:#f0b90b;font-weight:700;font-family:monospace;">~6%</span> of 2026E NPAT
            <span style="color:#4a4e59;"> | </span>
            <span style="color:#f0b90b;font-weight:700;font-family:monospace;">~4%</span> of 2027E NPAT
        </p>
        <div style="display:flex;gap:12px;flex-wrap:wrap;">
            <div style="background:#131722;border:1px solid #2a2e39;border-radius:4px;padding:8px 14px;font-size:0.82rem;">
                <span style="color:#787b86;">If ASP +Rmb1/kg →</span>
                <span style="color:#26a69a;font-family:monospace;font-weight:600;"> +Rmb 9.0bn NPAT</span>
            </div>
            <div style="background:#131722;border:1px solid #2a2e39;border-radius:4px;padding:8px 14px;font-size:0.82rem;">
                <span style="color:#787b86;">If cost -Rmb0.5/kg →</span>
                <span style="color:#26a69a;font-family:monospace;font-weight:600;"> +Rmb 4.5bn NPAT</span>
            </div>
            <div style="background:#131722;border:1px solid #2a2e39;border-radius:4px;padding:8px 14px;font-size:0.82rem;">
                <span style="color:#787b86;">GS 2H26 Rmb14-16 →</span>
                <span style="color:#26a69a;font-family:monospace;font-weight:600;"> +Rmb 2.7-5.4bn vs spot</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Broker Consensus ──
    st.markdown("### Broker Consensus")
    broker_df = pd.DataFrame({
        "House": ["BofA Securities", "Goldman Sachs", "Morgan Stanley", "UBS"],
        "Rating": ["BUY", "BUY", "OW", "BUY"],
        "A-Share TP": ["57.00", "67.00", "58.00", "60.50"],
        "Upside": ["+14.6%", "+34.7%", "+16.6%", "+21.6%"],
        "2025E EPS": [2.82, 2.86, 2.81, 3.03],
        "2026E EPS": [2.50, 5.50, 2.75, 3.69],
        "2027E EPS": [3.65, 7.52, 4.75, 5.95],
    })
    st.dataframe(broker_df, use_container_width=True, hide_index=True)
    st.caption("Consensus Avg TP: 60.63 | Avg Upside: +21.9% | Avg 2027E EPS: 5.47 | Base price: 49.74")

    st.markdown("---")

    # ── Catalyst Timeline ──
    st.markdown("### Catalyst Timeline")
    timeline_html = """
    <div style="font-family:'Inter',system-ui,sans-serif;background:#131722;border-radius:8px;padding:20px 20px 16px;">
      <div style="position:relative;display:flex;align-items:flex-start;overflow-x:auto;padding-bottom:8px;">
        <div style="position:absolute;top:20px;left:0;right:0;height:2px;background:#2a2e39;"></div>
        <div style="flex:1;min-width:120px;position:relative;text-align:center;padding-top:34px;">
          <div style="position:absolute;top:14px;left:50%%;transform:translateX(-50%%);width:12px;height:12px;border-radius:50%%;background:#4a4e59;border:2px solid #131722;z-index:1;"></div>
          <div style="font-family:monospace;font-size:11px;font-weight:600;color:#4a4e59;margin-bottom:3px;">Jul 2025</div>
          <div style="font-size:11px;color:#787b86;line-height:1.3;">Industry loss-making begins</div>
        </div>
        <div style="flex:1;min-width:120px;position:relative;text-align:center;padding-top:34px;">
          <div style="position:absolute;top:14px;left:50%%;transform:translateX(-50%%);width:12px;height:12px;border-radius:50%%;background:#4a4e59;border:2px solid #131722;z-index:1;"></div>
          <div style="font-family:monospace;font-size:11px;font-weight:600;color:#4a4e59;margin-bottom:3px;">Sep 2025</div>
          <div style="font-size:11px;color:#787b86;line-height:1.3;">Sow herd decline starts</div>
        </div>
        <div style="flex:1;min-width:140px;position:relative;text-align:center;padding-top:34px;">
          <div style="position:absolute;top:14px;left:50%%;transform:translateX(-50%%);width:12px;height:12px;border-radius:50%%;background:#f0b90b;box-shadow:0 0 8px #f0b90b;border:2px solid #131722;z-index:1;"></div>
          <div style="font-family:monospace;font-size:11px;font-weight:700;color:#f0b90b;margin-bottom:3px;">Mar 2026</div>
          <div style="font-size:11px;color:#787b86;line-height:1.3;">Govt sow target discussion (36.5mn) · <strong style="color:#f0b90b;">NOW</strong></div>
        </div>
        <div style="flex:1;min-width:120px;position:relative;text-align:center;padding-top:34px;">
          <div style="position:absolute;top:14px;left:50%%;transform:translateX(-50%%);width:12px;height:12px;border-radius:50%%;background:#2962ff;border:2px solid #131722;z-index:1;"></div>
          <div style="font-family:monospace;font-size:11px;font-weight:600;color:#2962ff;margin-bottom:3px;">2H26 / 3Q26</div>
          <div style="font-size:11px;color:#787b86;line-height:1.3;">Expected inflection point</div>
        </div>
        <div style="flex:1;min-width:120px;position:relative;text-align:center;padding-top:34px;">
          <div style="position:absolute;top:14px;left:50%%;transform:translateX(-50%%);width:12px;height:12px;border-radius:50%%;background:#2962ff;border:2px solid #131722;z-index:1;"></div>
          <div style="font-family:monospace;font-size:11px;font-weight:600;color:#2962ff;margin-bottom:3px;">2H26</div>
          <div style="font-size:11px;color:#787b86;line-height:1.3;">GS expects -6%% hog output decline</div>
        </div>
        <div style="flex:1;min-width:120px;position:relative;text-align:center;padding-top:34px;">
          <div style="position:absolute;top:14px;left:50%%;transform:translateX(-50%%);width:12px;height:12px;border-radius:50%%;background:#2962ff;border:2px solid #131722;z-index:1;"></div>
          <div style="font-family:monospace;font-size:11px;font-weight:600;color:#2962ff;margin-bottom:3px;">2H26</div>
          <div style="font-size:11px;color:#787b86;line-height:1.3;">Price recovery to Rmb 14-16/kg</div>
        </div>
      </div>
    </div>
    """
    components.html(timeline_html, height=120, scrolling=False)


# ════════════════════════════════════════════════════════════════
# PAGE 3: P&L DRIVERS
# ════════════════════════════════════════════════════════════════
elif page == "P&L Drivers":
    st.markdown("# Muyuan P&L Drivers")
    st.markdown("Key revenue and cost drivers extracted from broker research.")

    # Revenue drivers
    st.markdown("### Revenue Drivers")
    years = ["2022A", "2023A", "2024A", "2025E", "2026E", "2027E"]

    rev_data = {
        "Metric": [
            "Finished Hog ASP (RMB/kg)", "Total Hog Sales (mn head)",
            "Finished Hog Vol (mn head)", "Piglet Vol (mn head)",
            "Slaughtering Vol (mn head)", "Revenue (RMB bn)"
        ],
        "2022A": [18.0, 61.2, 55.3, 5.6, None, 124.8],
        "2023A": [14.5, 63.8, 62.3, 1.4, None, 110.9],
        "2024A": [16.3, 71.6, 65.5, 5.7, 12.6, 137.9],
        "2025E": [13.5, 91.4, 78.0, 13.5, 27.6, 140.0],
        "2026E": [13.3, 90.0, 80.0, 11.5, 35.1, 135.0],
        "2027E": [14.2, 90.0, 80.0, 11.9, 40.4, 148.0],
    }
    df_rev = pd.DataFrame(rev_data)
    st.dataframe(df_rev, use_container_width=True, hide_index=True)

    # ASP vs Cost chart
    col1, col2 = st.columns(2)
    with col1:
        fig_asp = go.Figure()
        asp_vals = [18.0, 14.5, 16.3, 13.5, 13.3, 14.2]
        cogs_vals = [14.7, 14.1, 13.2, 11.4, 11.3, 11.5]
        fig_asp.add_trace(go.Scatter(x=years, y=asp_vals, mode='lines+markers', name='ASP',
                                      line=dict(color='#2962ff', width=3), marker=dict(size=8)))
        fig_asp.add_trace(go.Scatter(x=years, y=cogs_vals, mode='lines+markers', name='Unit COGS',
                                      line=dict(color='#ef5350', width=3), marker=dict(size=8)))
        fig_asp.add_trace(go.Bar(x=years, y=[a - c for a, c in zip(asp_vals, cogs_vals)], name='GP/kg',
                                  marker_color='rgba(38,166,154,0.4)', opacity=0.8))
        fig_asp.update_layout(title="ASP vs Unit COGS (RMB/kg)", height=380,
                               legend=DARK_LEGEND, **DARK_LAYOUT)
        st.plotly_chart(fig_asp, use_container_width=True)

    with col2:
        fig_vol = go.Figure()
        fig_vol.add_trace(go.Bar(x=years, y=[55.3, 62.3, 65.5, 78.0, 80.0, 80.0],
                                  name='Finished Hog', marker_color='#2962ff'))
        fig_vol.add_trace(go.Bar(x=years, y=[5.6, 1.4, 5.7, 13.5, 11.5, 11.9],
                                  name='Piglet', marker_color='#ab47bc'))
        fig_vol.update_layout(title="Hog Sales Volume (mn head)", barmode='stack', height=380,
                               legend=DARK_LEGEND, **DARK_LAYOUT)
        st.plotly_chart(fig_vol, use_container_width=True)

    # Cost drivers
    st.markdown("### Cost Drivers")
    st.markdown("""
    <div class="info-box">
    <strong>Feed = ~60% of production cost.</strong> Muyuan's key edge: soymeal at 7.3% of feed vs industry 10-17%.
    Smart feeding system adjusts formulation in real-time. >80% of China's soybean is imported.
    </div>
    """, unsafe_allow_html=True)

    cost_data = {
        "Metric": [
            "Unit COGS — Muyuan (RMB/kg)", "Unit COGS — Industry Avg (RMB/kg)",
            "Muyuan Cost Advantage (RMB/kg)", "Soymeal % in Feed (Muyuan)",
            "Soymeal % in Feed (Industry)", "GP/kg (RMB/kg)"
        ],
        "2022A": [14.7, None, None, None, None, 3.3],
        "2023A": [14.1, None, None, None, None, 0.4],
        "2024A": [13.2, 16.4, 3.2, "7.3%", "10-17%", 3.1],
        "2025E": [11.4, 13.7, 2.3, None, None, 2.1],
        "2026E": [11.3, 13.7, 2.4, None, None, 2.0],
        "2027E": [11.5, None, None, None, None, 2.7],
    }
    df_cost = pd.DataFrame(cost_data)
    st.dataframe(df_cost, use_container_width=True, hide_index=True)

    # Cost comparison chart
    fig_cost = go.Figure()
    muyuan_cost = [15.7, 14.9, 14.0, 12.1, 10.9, 10.7]
    industry_cost = [None, None, 16.4, 13.7, 13.7, None]
    fig_cost.add_trace(go.Bar(x=years, y=muyuan_cost, name='Muyuan Complete Cost',
                               marker_color='#2962ff'))
    fig_cost.add_trace(go.Bar(x=years, y=industry_cost, name='Industry Avg Cost',
                               marker_color='#4a4e59'))
    fig_cost.update_layout(title="Complete Unit Cost: Muyuan vs Industry (RMB/kg)",
                            barmode='group', height=350, legend=DARK_LEGEND, **DARK_LAYOUT)
    st.plotly_chart(fig_cost, use_container_width=True)

    # Profitability
    st.markdown("### Profitability")
    profit_data = {
        "Metric": ["Gross Profit (RMB bn)", "EBITDA (RMB bn)", "NPAT (RMB bn)",
                    "EPS (RMB)", "DPS (RMB)", "Gross Margin", "EBITDA Margin", "Net Margin",
                    "ROE", "FCF (RMB bn)"],
        "2022A": [21.8, 26.8, 13.3, 2.47, 0.73, "17.5%", "21.4%", "10.6%", "21.0%", None],
        "2023A": [3.4, 9.4, -4.3, -0.79, 0, "3.1%", "8.5%", "NM", "-6.3%", -7.1],
        "2024A": [26.3, 34.2, 17.9, 3.27, 1.39, "19.1%", "24.8%", "13.0%", "26.5%", 25.2],
        "2025E": [23.0, 31.6, 15.5, 2.86, 1.14, "16.5%", "22.2%", "10.9%", "20.5%", 18.1],
        "2026E": [22.2, 46.0, 20.7, 3.69, 2.20, "17.6%", "31.6%", "15.6%", "22.4%", 37.1],
        "2027E": [33.4, 56.8, 34.1, 5.95, 3.57, "24.3%", "36.7%", "22.7%", "29.6%", 48.8],
    }
    df_profit = pd.DataFrame(profit_data)
    st.dataframe(df_profit, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="info-box">
    <strong>Key sensitivity:</strong> Every RMB 0.1/kg change in GP moves Muyuan's NPAT by ~RMB 0.9bn, or ~6% of 2026E earnings.
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# PAGE 3: BROKER ESTIMATES
# ════════════════════════════════════════════════════════════════
elif page == "Broker Estimates":
    st.markdown("# Broker Estimates Comparison")
    st.markdown("Side-by-side view of all 4 broker estimates from March 2026 initiation reports.")

    # Ratings
    st.markdown("### Ratings & Target Prices")
    ratings = {
        "": ["Rating (A)", "A-share TP (RMB)", "H-share TP (HKD)", "Valuation"],
        "BofA": ["Buy", "57.00", "54.00", "9x EV/EBITDA"],
        "UBS": ["Buy", "60.50", "—", "P/BV"],
        "Goldman Sachs": ["Buy", "67.00", "61.00", "Avg NTM/LT P/E"],
        "Morgan Stanley": ["Overweight", "58.00", "59.00", "18x mid-cycle P/E"],
    }
    df_ratings = pd.DataFrame(ratings)
    st.dataframe(df_ratings, use_container_width=True, hide_index=True)

    # TP comparison chart
    fig_tp = go.Figure()
    brokers = ["BofA", "UBS", "Goldman Sachs", "Morgan Stanley"]
    tps = [57.0, 60.5, 67.0, 58.0]
    fig_tp.add_trace(go.Bar(x=brokers, y=tps, marker_color=['#ef5350', '#2962ff', '#f0b90b', '#26a69a'],
                             text=[f"RMB {t:.0f}" for t in tps], textposition='outside',
                             textfont=dict(color="#d1d4dc")))
    fig_tp.add_hline(y=49.74, line_dash="dash", line_color="#787b86",
                      annotation_text="Current: RMB 49.74", annotation_position="right",
                      annotation_font_color="#d1d4dc")
    fig_tp.update_layout(title="A-share Target Prices (RMB)", height=350, yaxis_title="RMB", **DARK_LAYOUT)
    st.plotly_chart(fig_tp, use_container_width=True)

    # Key assumptions
    st.markdown("### Hog Price Assumptions (RMB/kg)")
    hog_px = {
        "Period": ["2025E", "1H26E", "2H26E", "2026E Avg", "2027E"],
        "BofA": [13.5, None, None, 13.3, 14.2],
        "UBS": [None, None, None, 13.0, 14.5],
        "Goldman Sachs": [13.8, 13.5, "14.8-15.3", 14.8, 15.3],
        "Morgan Stanley": [13.5, 12.2, 14.0, 13.0, 14.0],
    }
    df_hog = pd.DataFrame(hog_px)
    st.dataframe(df_hog, use_container_width=True, hide_index=True)

    # Earnings
    st.markdown("### Earnings Estimates")
    col1, col2 = st.columns(2)

    with col1:
        fig_npat = go.Figure()
        years_e = ["2025E", "2026E", "2027E"]
        fig_npat.add_trace(go.Bar(x=years_e, y=[15.4, 14.1, 21.1], name="BofA", marker_color="#ef5350"))
        fig_npat.add_trace(go.Bar(x=years_e, y=[16.6, 20.7, 34.1], name="UBS", marker_color="#2962ff"))
        fig_npat.add_trace(go.Bar(x=years_e, y=[15.6, 31.8, 43.4], name="GS", marker_color="#f0b90b"))
        fig_npat.add_trace(go.Bar(x=years_e, y=[15.3, 15.9, 27.4], name="MS", marker_color="#26a69a"))
        fig_npat.update_layout(title="NPAT Estimates (RMB bn)", barmode='group', height=380,
                                legend=DARK_LEGEND, **DARK_LAYOUT)
        st.plotly_chart(fig_npat, use_container_width=True)

    with col2:
        fig_eps = go.Figure()
        fig_eps.add_trace(go.Bar(x=years_e, y=[2.82, 2.50, 3.65], name="BofA", marker_color="#ef5350"))
        fig_eps.add_trace(go.Bar(x=years_e, y=[3.03, 3.69, 5.95], name="UBS", marker_color="#2962ff"))
        fig_eps.add_trace(go.Bar(x=years_e, y=[2.86, 5.50, 7.52], name="GS", marker_color="#f0b90b"))
        fig_eps.add_trace(go.Bar(x=years_e, y=[2.81, 2.75, 4.75], name="MS", marker_color="#26a69a"))
        fig_eps.update_layout(title="EPS Estimates (RMB)", barmode='group', height=380,
                                legend=DARK_LEGEND, **DARK_LAYOUT)
        st.plotly_chart(fig_eps, use_container_width=True)

    # Valuation multiples
    st.markdown("### Valuation Multiples")
    val_data = {
        "Metric": ["2026E P/E (x)", "2027E P/E (x)", "2026E EV/EBITDA (x)", "2027E EV/EBITDA (x)",
                    "2026E Div Yield", "2027E Div Yield", "2027E FCF Yield"],
        "BofA": ["16.4x", "11.2x", "9.3x", "7.6x", "3.8%", "5.5%", "10.8%"],
        "UBS": ["12.7x", "7.9x", "8.6x", "5.9x", "3.9%", "7.6%", "13.8%"],
        "Goldman Sachs": ["9.0x", "6.6x", "6.5x", "4.7x", "4.4%", "6.1%", "16.6%"],
        "Morgan Stanley": ["18.1x", "10.5x", "16.3x", "11.2x", "2.5%", "4.3%", "13.0%"],
    }
    df_val = pd.DataFrame(val_data)
    st.dataframe(df_val, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="info-box">
    <strong>Key divergence:</strong> GS is the most bullish (2026E NPAT RMB 31.8bn) while BofA is most conservative (RMB 14.1bn).
    The gap is driven primarily by hog price assumptions — GS expects a sharper 2H26 recovery.
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# PAGE 4: SENSITIVITY
# ════════════════════════════════════════════════════════════════
elif page == "Sensitivity":
    st.markdown("# Earnings & Dividend Sensitivity (2027E)")
    st.markdown("Interactive scenario analysis: how hog prices drive earnings and yields.")

    col1, col2, col3 = st.columns(3)
    with col1:
        cost_input = st.number_input("Production Cost (RMB/kg)", value=11.3, step=0.1, format="%.1f")
    with col2:
        weight_input = st.number_input("Avg Hog Weight (kg)", value=120, step=5)
    with col3:
        share_price = st.number_input("Share Price (RMB)", value=49.74, step=0.5, format="%.2f")

    market_hog = 80  # mn heads
    shares = 5737  # mn shares

    hog_prices = np.arange(12.0, 17.1, 0.5)
    np_per_head = (hog_prices - cost_input) * weight_input
    np_total = np_per_head * market_hog + 3000  # +piglet contribution

    # NP chart
    fig_np = go.Figure()
    fig_np.add_trace(go.Bar(
        x=[f"RMB {p:.1f}" for p in hog_prices],
        y=np_total,
        marker_color=['#26a69a' if n > 0 else '#ef5350' for n in np_total],
        text=[f"RMB {n/1000:.1f}bn" for n in np_total],
        textposition='outside',
        textfont=dict(color="#d1d4dc"),
    ))
    fig_np.update_layout(title="Net Profit at Various Hog Prices (2027E)", height=400,
                          yaxis_title="Net Profit (RMB mn)", xaxis_title="Hog Price (RMB/kg)", **DARK_LAYOUT)
    st.plotly_chart(fig_np, use_container_width=True)

    # Dividend yield heatmap
    st.markdown("### Dividend Yield Matrix")
    payouts = [0.4, 0.5, 0.6, 0.7, 0.8]
    prices_sel = [13.0, 13.5, 14.0, 14.5, 15.0, 15.5]
    mkt_cap = share_price * shares

    yields = []
    for po in payouts:
        row = []
        for p in prices_sel:
            np_h = (p - cost_input) * weight_input
            np_t = np_h * market_hog + 3000
            div_yield = (np_t * po) / mkt_cap * 100
            row.append(round(div_yield, 1))
        yields.append(row)

    fig_heat = go.Figure(go.Heatmap(
        z=yields,
        x=[f"RMB {p:.1f}/kg" for p in prices_sel],
        y=[f"{int(p*100)}% payout" for p in payouts],
        colorscale=[[0, '#131722'], [0.5, '#1a3a2a'], [1, '#26a69a']],
        text=[[f"{v:.1f}%" for v in row] for row in yields],
        texttemplate="%{text}",
        textfont={"size": 14, "color": "#d1d4dc"},
    ))
    fig_heat.update_layout(title="Dividend Yield (%) by Hog Price x Payout Ratio",
                            height=350, **DARK_LAYOUT)
    st.plotly_chart(fig_heat, use_container_width=True)

    # Implied P/E
    st.markdown("### Implied P/E at Current Price")
    pe_data = []
    for p in prices_sel:
        np_h = (p - cost_input) * weight_input
        np_t = np_h * market_hog + 3000
        eps = np_t / shares
        pe = share_price / eps if eps > 0 else None
        pe_data.append({"Hog Price": f"RMB {p:.1f}/kg", "NP (RMB bn)": f"{np_t/1000:.1f}",
                        "EPS (RMB)": f"{eps:.2f}", "Implied P/E": f"{pe:.1f}x" if pe else "NM"})
    st.dataframe(pd.DataFrame(pe_data), use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════
# PAGE 5: HOG CYCLE HISTORY
# ════════════════════════════════════════════════════════════════
elif page == "Hog Cycle History":
    st.markdown("# China Hog Price Cycle History")
    st.markdown("Each complete cycle is ~4 years, driven primarily by supply dynamics.")

    # Cycle table
    cycle_data = {
        "Cycle": ["Cycle 1", "Cycle 2", "Cycle 3", "Cycle 4 (ASF)", "Current"],
        "Period": ["Jul 2006 - Apr 2010", "Apr 2010 - Apr 2014", "Apr 2014 - May 2018",
                    "May 2018 - Apr 2022", "Apr 2022 - Present"],
        "Total (mths)": [45, 49, 50, 47, "48+"],
        "Upcycle (mths)": [21, 17, 26, 18, "?"],
        "Peak (RMB/kg)": [17.4, 19.9, 21.2, 41.0, "?"],
        "Peak Chg": ["+158%", "+110%", "+103%", "+286%", "?"],
        "Downcycle (mths)": [25, 32, 24, 15, "?"],
        "Trough (RMB/kg)": [9.0, 10.5, 10.0, 10.8, "~10.2"],
    }
    st.dataframe(pd.DataFrame(cycle_data), use_container_width=True, hide_index=True)

    # Timeline visualization
    fig_cycle = go.Figure()
    cycle_starts = [2006.5, 2010.3, 2014.3, 2018.4, 2022.3]
    cycle_ends = [2010.3, 2014.3, 2018.4, 2022.3, 2026.3]
    peaks = [17.4, 19.9, 21.2, 41.0, None]
    troughs = [9.0, 10.5, 10.0, 10.8, 10.2]
    colors = ["#2962ff", "#ab47bc", "#00bcd4", "#ef5350", "#f0b90b"]
    names = ["Cycle 1", "Cycle 2", "Cycle 3", "Cycle 4 (ASF)", "Current"]

    for i in range(5):
        mid = (cycle_starts[i] + cycle_ends[i]) / 2
        fig_cycle.add_shape(type="rect", x0=cycle_starts[i], x1=cycle_ends[i], y0=0, y1=peaks[i] or 15,
                             fillcolor=colors[i], opacity=0.15, line_width=0)
        if peaks[i]:
            fig_cycle.add_trace(go.Scatter(
                x=[cycle_starts[i], mid, cycle_ends[i]],
                y=[troughs[i], peaks[i], troughs[i] if i < 4 else 10.2],
                mode='lines+markers+text', name=names[i],
                line=dict(color=colors[i], width=3),
                text=["", f"Peak: {peaks[i]}", ""],
                textposition="top center",
            ))

    fig_cycle.update_layout(title="Hog Price Cycle Visualization", height=450,
                             xaxis_title="Year", yaxis_title="Hog Price (RMB/kg)",
                             legend={**DARK_LEGEND, 'y': -0.12}, **DARK_LAYOUT)
    st.plotly_chart(fig_cycle, use_container_width=True)

    # Sub-5x outcomes
    st.markdown("### When Hog/Feed Ratio Drops Below 5x — Historical Outcomes")
    st.markdown("*This is the key pattern for timing entries.*")

    outcome_data = {
        "Period": ["Mar-May 2014", "Mar 2015", "Sep-Oct 2021", "Feb-Apr 2022", "Jun-Jul 2023"],
        "Duration": ["8 weeks", "2 weeks", "5 weeks", "9 weeks", "7 weeks"],
        "Avg Ratio": ["4.7x", "4.9x", "4.4x", "4.4x", "4.9x"],
        "Sow Chg (2M)": ["-3.2%", "-2.9%", "-3.7%", "-2.1%", "-1.3%"],
        "Hog Px (2M)": ["+12%", "+17%", "+25%", "+12%", "+20%"],
        "Muyuan Stk (2M)": ["+16%", "+38%", "+23%", "-8%", "+6%"],
        "Hog Px (5M)": ["+28%", "+59%", "+2%", "+83%", "+5%"],
        "Muyuan Stk (5M)": ["+47%", "+124%", "+36%", "+4%", "-7%"],
    }
    st.dataframe(pd.DataFrame(outcome_data), use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="info-box">
        <strong>Average 2-month outcome after ratio < 5x:</strong><br>
        Hog prices: <strong>+17%</strong><br>
        Muyuan stock: <strong>+15%</strong>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="info-box">
        <strong>Average 5-month outcome after ratio < 5x:</strong><br>
        Hog prices: <strong>+35%</strong><br>
        Muyuan stock: <strong>+41%</strong> (excl. 2022)
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# PAGE 6: KEY RISKS
# ════════════════════════════════════════════════════════════════
elif page == "Key Risks":
    st.markdown("# Key Risks & Catalysts")

    st.markdown("### Upside Catalysts")
    catalysts = [
        ("Hog/corn ratio hits 5.0x", "Triggers NDRC reserve purchases = price floor. Asymmetric long.",
         "Hog-to-corn ratio (Wind/NDRC)"),
        ("Sow herd falls to 36.5mn target", "Govt target. Supply crunch 10-12 months later.",
         "MOA monthly sow data"),
        ("Hog price inflection in 2H26", "All 4 brokers expect rebound. GS: RMB 14.8-15.3/kg.",
         "Spot hog price, futures curve"),
        ("Further cost reduction", "GS targets RMB 10.0/kg by 2030E. Feed optimization + PSY gains.",
         "Quarterly cost disclosure"),
        ("Dividend payout increase", "Payout rose 20% to 40%. UBS models 50-60% for 2027E.",
         "Annual/interim dividends"),
        ("Slaughtering scale-up", "35mn head target 2026. Vertical integration + earnings diversification.",
         "Quarterly operating data"),
    ]

    for title, desc, metric in catalysts:
        with st.expander(f"**{title}**"):
            st.write(desc)
            st.caption(f"Monitor: {metric}")

    st.markdown("### Downside Risks")
    risks = [
        ("Slower destocking", "If sow culling slows, oversupply persists and hog price stays low.",
         "Monthly sow inventory trends"),
        ("Rising feed costs", "Corn/soymeal spike from geopolitics (Middle East, tariffs). 60% of COGS is feed.",
         "Corn & soybean meal futures"),
        ("Disease outbreak (ASF)", "African Swine Fever recurrence would disrupt supply chain.",
         "Industry news, biosecurity reports"),
        ("Weaker pork demand", "Population peaking + health trends reducing pork's share of protein.",
         "Monthly pork consumption data"),
        ("Execution risk on cost savings", "Failure to sustain cost advantage vs peers.",
         "Quarterly unit COGS disclosure"),
        ("Management transition", "Generational handover to younger management team.",
         "Corporate announcements"),
    ]

    for title, desc, metric in risks:
        with st.expander(f"**{title}**"):
            st.write(desc)
            st.caption(f"Monitor: {metric}")

    st.markdown("---")
    st.markdown("### Decision Framework Summary")
    st.markdown("""
    | Scenario | Hog/Corn Ratio | Hog Price | Action |
    |----------|---------------|-----------|--------|
    | Deep distress | < 5.0x | < RMB 11/kg | **Strong Buy** — Govt put + supply crunch setup |
    | Approaching floor | 5.0-5.5x | RMB 11-12/kg | **Accumulate** — Near intervention trigger |
    | Loss zone | 5.5-7.0x | RMB 12-14/kg | **Hold** — Industry culling but no urgency |
    | Breakeven | ~7.0x | RMB 14-16/kg | **Hold/Trim** — Stable, watch for supply builds |
    | High profit | > 9.0x | > RMB 17/kg | **Reduce** — Herd expansion = future oversupply |
    """)
