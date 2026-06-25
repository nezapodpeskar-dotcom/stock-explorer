import random
import datetime as _dt
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Big Tech Stock Explorer",
    page_icon="📈",
    layout="wide",
)

st.markdown(
    """
    <style>
        .block-container { padding-top: 2.5rem; padding-bottom: 3rem; max-width: 1200px; }
        html, body, [class*="css"] { font-size: 17px !important; }
        h1 { font-size: 2.4rem !important; font-weight: 700 !important; color: #0d2b45 !important; letter-spacing: -0.5px; }
        h2 { font-size: 1.5rem !important; font-weight: 600 !important; color: #0d2b45 !important; margin-top: 0.5rem !important; }
        h5 { font-size: 1.05rem !important; font-weight: 600 !important; color: #1B4F72 !important; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.6rem !important; }
        p, li { font-size: 1rem !important; line-height: 1.7; color: #2c3e50; }
        [data-testid="stCaptionContainer"] p { font-size: 0.88rem !important; color: #6b7a8d !important; }
        [data-testid="metric-container"] { background: #ffffff; border: 1px solid #cdd6e4; border-top: 4px solid #1B4F72; border-radius: 10px; padding: 1.2rem 1.4rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
        [data-testid="stMetricLabel"] { font-size: 0.85rem !important; font-weight: 600 !important; color: #6b7a8d !important; text-transform: uppercase; letter-spacing: 0.05em; }
        [data-testid="stMetricValue"] { font-size: 1.9rem !important; font-weight: 700 !important; color: #0d2b45 !important; }
        [data-testid="stMetricDelta"] { font-size: 1rem !important; font-weight: 500 !important; }
        [data-testid="stTab"] button { font-size: 1rem !important; font-weight: 600 !important; padding: 0.6rem 1.2rem !important; }
        [data-testid="stSidebar"] { background-color: #0d2b45 !important; }
        [data-testid="stSidebar"] * { color: #dce6f0 !important; }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #ffffff !important; }
        hr { border-color: #dde3ed; margin: 1.8rem 0; }
        [data-testid="stAlert"] p { font-size: 1rem !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = px.data.stocks()
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()
tickers = [c for c in df.columns if c != "date"]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Controls")
    st.caption("Choose which stocks to compare and the time window you want to analyse.")

    chosen = st.multiselect(
        "Stocks to compare",
        options=tickers,
        default=["AAPL", "MSFT", "GOOG"],
        help="You can select as many stocks as you like.",
    )

    if not chosen:
        st.warning("Please select at least one stock to continue.")
        st.stop()

    st.markdown("---")

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    start_date, end_date = st.slider(
        "Date range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="MMM YYYY",
        help="Drag the handles to zoom in on a specific period.",
    )

    st.markdown("---")
    st.caption("Data source: Plotly built-in stock dataset. Prices are re-indexed to 1.0 at the start of the selected range.")
    st.markdown("---")

    _sidebar_facts = [
        ("Apple 🍎",     "Apple operates over 540 retail stores worldwide — each designed to serve as a community space as much as a shop."),
        ("Google 🔍",    "Google's first server was built from Lego bricks in a Stanford dorm room. The founders originally called it 'Backrub'."),
        ("Amazon 📦",    "Amazon has helped digitize 12 million small businesses and supported 2.8 million jobs in India alone."),
        ("Netflix 📺",   "Netflix now entertains over half a billion people in more than 190 countries across 50 different languages."),
        ("Meta 🌐",      "Facebook launched in 2004 to connect a single university campus. Today Meta owns four apps each used by over a billion people."),
        ("Microsoft 💻", "IBM launched its first personal computer on August 12, 1981 — running Microsoft's MS-DOS 1.0, the deal that built Microsoft's empire."),
        ("Nike 👟",      "Between 1994 and 1998 Nike signed Brazil & US Soccer and launched the first Mercurial boot — the four years that made Nike a global football brand."),
    ]
    random.seed(int(_dt.date.today().strftime("%Y%m%d")))
    _company, _fact = random.choice(_sidebar_facts)

    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.18);
                    border-left:4px solid #7ecbf7;border-radius:8px;padding:1rem 1.1rem;">
            <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.1em;
                        text-transform:uppercase;color:#7ecbf7;margin-bottom:0.4rem;">💡 Did You Know?</div>
            <div style="font-size:0.82rem;font-weight:600;color:#ffffff;margin-bottom:0.3rem;">{_company}</div>
            <div style="font-size:0.8rem;color:#c0d8ee;line-height:1.5;">{_fact}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Filter & re-index ─────────────────────────────────────────────────────────
mask = (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)
dff = df[mask].copy().reset_index(drop=True)

if dff.empty:
    st.warning("No data found for this date range. Please widen the window.")
    st.stop()

for t in tickers:
    first = dff[t].iloc[0]
    if first != 0:
        dff[t] = dff[t] / first

# ── Metrics ───────────────────────────────────────────────────────────────────
growths    = {t: (dff[t].iloc[-1] - 1) * 100 for t in chosen}
best_stock = max(growths, key=growths.get)
daily_vol  = {t: dff[t].pct_change().std() * 100 for t in chosen}
most_vol   = max(daily_vol, key=daily_vol.get)

COLORS = px.colors.qualitative.Set2
CHART_LAYOUT = dict(plot_bgcolor="white", paper_bgcolor="white",
                    margin=dict(t=40, b=20), font=dict(family="sans-serif"))

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📈 Big Tech Stock Explorer")
st.markdown(
    "An interactive dashboard for analysing the historical performance of major technology stocks. "
    "Use the sidebar to select stocks and adjust the date range — all charts and figures update instantly."
)
st.markdown("---")

tab_overview, tab_calculator, tab_peak, tab_insights = st.tabs(
    ["📊  Overview & Charts", "💰  Investment Calculator", "🏔️  Peak Tracker", "💡  Market Insights"]
)

# ── TAB 1: Overview & Charts ──────────────────────────────────────────────────
with tab_overview:
    st.subheader("How did each stock perform?")
    st.markdown(
        f"Results cover **{start_date.strftime('%b %Y')}** to **{end_date.strftime('%b %Y')}**. "
        "A reading of 2.00× means the stock doubled during that window."
    )
    st.markdown("##### Stock-by-stock results")
    for col, t in zip(st.columns(len(chosen)), chosen):
        col.metric(label=t, value=f"{dff[t].iloc[-1]:.2f}×", delta=f"{growths[t]:+.1f}%")

    st.markdown("---")
    st.markdown("##### Highlights")
    hi1, hi2 = st.columns(2)
    with hi1:
        st.metric("🏆  Best Performer", best_stock, f"{growths[best_stock]:+.1f}% total growth")
        st.caption("The stock that grew the most over the selected period.")
    with hi2:
        st.metric("📊  Most Volatile", most_vol, f"±{daily_vol[most_vol]:.2f}% average daily move", delta_color="off")
        st.caption("The stock whose price moved up and down the most from day to day.")

    st.markdown("---")
    st.subheader("Price trends over time")
    st.markdown("All stocks start at 1.0, so you can compare growth directly regardless of actual price.")
    fig_line = px.line(dff, x="date", y=chosen,
                       labels={"value": "Relative price (1.0 = start)", "date": "Date", "variable": "Stock"},
                       color_discrete_sequence=COLORS)
    fig_line.update_layout(**CHART_LAYOUT, hovermode="x unified",
                           legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                           legend_title_text="")
    fig_line.update_xaxes(showgrid=False, title_text="")
    fig_line.update_yaxes(gridcolor="#EEF0F5", title_text="Relative price")
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")
    st.markdown("##### Total growth, side by side")
    st.caption("Sorted from highest to lowest. Figures show percentage change over the full selected period.")
    growth_df = (pd.DataFrame({"Stock": list(growths.keys()), "Growth (%)": list(growths.values())})
                 .sort_values("Growth (%)", ascending=False).reset_index(drop=True))
    fig_bar = px.bar(growth_df, x="Stock", y="Growth (%)", color="Stock",
                     text_auto=".1f", color_discrete_sequence=COLORS)
    fig_bar.update_traces(textposition="outside", textfont_size=13)
    fig_bar.update_layout(**CHART_LAYOUT, showlegend=False)
    fig_bar.update_xaxes(showgrid=False, title_text="")
    fig_bar.update_yaxes(gridcolor="#EEF0F5", title_text="Total growth (%)")
    st.plotly_chart(fig_bar, use_container_width=True)

# ── TAB 2: Investment Calculator ──────────────────────────────────────────────
with tab_calculator:
    st.subheader("What would my investment be worth?")
    st.markdown("Enter an amount and pick a stock to see how that money would have grown over the selected period.")
    input_col, _, result_col = st.columns([1, 0.15, 2])
    with input_col:
        st.markdown("##### Your inputs")
        invest_amount = st.number_input("Starting investment ($)", min_value=1, value=1000, step=100)
        invest_stock  = st.selectbox("Stock to invest in", options=chosen)
    final_value = invest_amount * dff[invest_stock].iloc[-1]
    profit      = final_value - invest_amount
    growth_pct  = growths[invest_stock]
    is_gain     = profit >= 0
    with result_col:
        st.markdown("##### Results")
        rc1, rc2, rc3 = st.columns(3)
        rc1.metric("Invested", f"${invest_amount:,.0f}")
        rc2.metric("End value", f"${final_value:,.2f}", delta=f"{growth_pct:+.1f}%")
        rc3.metric("Gain" if is_gain else "Loss", f"${abs(profit):,.2f}")
        st.markdown("")
        if is_gain:
            st.success(f"A ${invest_amount:,.0f} investment in {invest_stock} would have grown to ${final_value:,.2f} — a gain of ${profit:,.2f} ({growth_pct:+.1f}%).")
        else:
            st.error(f"A ${invest_amount:,.0f} investment in {invest_stock} would have fallen to ${final_value:,.2f} — a loss of ${abs(profit):,.2f} ({growth_pct:+.1f}%).")
        st.caption("Assumes purchase on the first day and sale on the last day of the selected period. Excludes taxes, fees, and dividends.")

# ── TAB 3: Peak Tracker ───────────────────────────────────────────────────────
with tab_peak:
    st.subheader("When did a stock reach its highest point?")
    st.markdown("Select a stock to find the exact date it hit its highest price within your chosen date range.")
    peak_stock = st.selectbox("Which stock would you like to track?", options=chosen, key="peak_select")
    peak_idx   = dff[peak_stock].idxmax()
    peak_date  = dff.loc[peak_idx, "date"]
    peak_value = dff.loc[peak_idx, peak_stock]
    days_ago   = (dff["date"].iloc[-1] - peak_date).days
    pk1, pk2, pk3 = st.columns(3)
    pk1.metric("Stock", peak_stock)
    pk2.metric("Peak date", peak_date.strftime("%d %b %Y"))
    pk3.metric("Peak value", f"{peak_value:.2f}×")
    if days_ago == 0:
        st.info(f"{peak_stock} reached its peak on the very last day of the selected range.")
    elif days_ago <= 30:
        st.info(f"{peak_stock} hit its highest point just {days_ago} day(s) before the end of the selected range.")
    else:
        st.info(f"{peak_stock} reached its peak on {peak_date.strftime('%d %b %Y')} — {days_ago} days before the end of the selected range.")
    st.markdown("---")
    fig_peak = px.line(dff, x="date", y=peak_stock,
                       labels={"date": "Date", peak_stock: "Relative price"},
                       color_discrete_sequence=["#2E86AB"])
    fig_peak.add_scatter(x=[peak_date], y=[peak_value], mode="markers+text",
                         marker=dict(color="#E63946", size=14, symbol="star"),
                         text=[f"  Peak: {peak_value:.2f}×"], textposition="top right", name="Peak")
    fig_peak.update_layout(**CHART_LAYOUT, title=f"{peak_stock} — price history with peak highlighted",
                           hovermode="x unified",
                           legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig_peak.update_xaxes(showgrid=False, title_text="")
    fig_peak.update_yaxes(gridcolor="#EEF0F5", title_text="Relative price")
    st.plotly_chart(fig_peak, use_container_width=True)

# ── TAB 4: Market Insights ────────────────────────────────────────────────────
COMPANY_INSIGHTS = {
    "Apple 🍎": {
        "headline": "540+ stores. One design philosophy.",
        "fact": ("Apple operates over 540 retail stores worldwide — more physical locations than most luxury "
                 "fashion houses. Every store follows the same architectural brief: open space, natural "
                 "materials, and no cash registers on countertops. Apple's stores generate more revenue "
                 "per square foot than almost any other retailer on earth."),
        "stats": [("Founded", "1976"), ("2025 Revenue", "$416B"), ("Retail Stores", "540+")],
        "source": "apple.com/newsroom", "accent": "#555555",
    },
    "Google 🔍": {
        "headline": "The billion-dollar idea that started on Lego.",
        "fact": ("Google's first server was built from Lego bricks in a Stanford dorm room — cheap, expandable, "
                 "and good at keeping hard drives in place. The founders named the engine 'Backrub' before "
                 "renaming it Google, a play on 'googol' (1 followed by 100 zeros). The first external "
                 "cheque — $100,000 from Sun co-founder Andy Bechtolsheim — was written before Google "
                 "was even incorporated."),
        "stats": [("Founded", "1998"), ("First investment", "$100K"), ("Countries", "190+")],
        "source": "about.google/our-story", "accent": "#4285F4",
    },
    "Amazon 📦": {
        "headline": "From books to billions of livelihoods.",
        "fact": ("Amazon's mission is to make customers' lives better and easier every day. Since launching "
                 "in India, Amazon has helped digitize 12 million small businesses and supported 2.8 million "
                 "jobs — a snapshot of how e-commerce reshapes local economies at scale. Today Amazon spans "
                 "online shopping, cloud computing, AI services, streaming, healthcare, and more."),
        "stats": [("Founded", "1994"), ("Small biz digitized", "12M"), ("Jobs supported (India)", "2.8M")],
        "source": "aboutamazon.com", "accent": "#FF9900",
    },
    "Netflix 📺": {
        "headline": "Half a billion fans. 190 countries. 50 languages.",
        "fact": ("Netflix started as a DVD-by-mail service in 1997. Today it entertains over half a billion "
                 "people in more than 190 countries across 50 different languages — one of the most widely "
                 "distributed entertainment platforms ever built. When a Netflix series becomes a hit, it "
                 "drives measurable spikes in music streams, book sales, fashion trends, and even tourism."),
        "stats": [("Founded", "1997"), ("Subscribers", "500M+"), ("Countries", "190+")],
        "source": "about.netflix.com", "accent": "#E50914",
    },
    "Meta 🌐": {
        "headline": "One dorm room. Four billion-user apps.",
        "fact": ("When Facebook launched in 2004, its only goal was to connect a single university campus. "
                 "Meta now owns Facebook, Instagram, WhatsApp, and Messenger — four of the world's most-used "
                 "apps, each serving over a billion people. Meta is now moving beyond 2D screens, investing "
                 "heavily in mixed reality and AI to build the next evolution in social technology."),
        "stats": [("Founded", "2004"), ("Apps with 1B+ users", "4"), ("Mission", "Connect the world")],
        "source": "about.meta.com/company-info", "accent": "#0082FB",
    },
    "Microsoft 💻": {
        "headline": "The deal that built the PC era.",
        "fact": ("On August 12, 1981, IBM launched its first personal computer running Microsoft's MS-DOS 1.0 — "
                 "a licensing deal that handed Microsoft control of the operating system for an entire industry. "
                 "Microsoft went public on March 13, 1986. By October 2012, Microsoft employee charitable "
                 "giving had crossed $1 billion — one of the largest corporate giving programmes in history."),
        "stats": [("Founded", "1975"), ("IPO date", "Mar 1986"), ("Employee giving", "$1B+")],
        "source": "news.microsoft.com/facts-about-microsoft", "accent": "#00A4EF",
    },
    "Nike 👟": {
        "headline": "Four years that launched a global football empire.",
        "fact": ("Between 1994 and 1998, Nike signed both the Brazil and U.S. Soccer national teams, debuted "
                 "iconic advertising campaigns, and launched the first-ever Mercurial boot — the lightest "
                 "football boot of its time. Those four years transformed Nike from a running and basketball "
                 "brand into the world's dominant force in football."),
        "stats": [("Founded", "1964"), ("Countries", "190+"), ("Breakthrough era", "1994–1998")],
        "source": "about.nike.com", "accent": "#111111",
        "note": "Nike (NKE) is not in the Plotly stock dataset used by this app's charts.",
    },
}

with tab_insights:
    st.subheader("Market Insights")
    st.markdown("Select a company to explore a curated business fact — each sourced from the company's own public website.")
    selected_company = st.selectbox("Choose a company", options=list(COMPANY_INSIGHTS.keys()))
    info   = COMPANY_INSIGHTS[selected_company]
    accent = info["accent"]
    st.markdown("---")
    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,#0d2b45 0%,#1B4F72 100%);
                    border-left:6px solid {accent};border-radius:14px;
                    padding:2.2rem 2.5rem;margin-bottom:1.5rem;
                    box-shadow:0 4px 20px rgba(13,43,69,0.18);">
            <div style="font-size:0.75rem;font-weight:700;letter-spacing:0.12em;
                        text-transform:uppercase;color:#7ecbf7;margin-bottom:0.6rem;">💡 Did You Know?</div>
            <div style="font-size:1.45rem;font-weight:700;color:#ffffff;line-height:1.4;margin-bottom:1rem;">{info['headline']}</div>
            <div style="font-size:1rem;color:#c0d8ee;line-height:1.7;">{info['fact']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("##### Key figures")
    for col, (label, value) in zip(st.columns(len(info["stats"])), info["stats"]):
        col.metric(label=label, value=value)
    if "note" in info:
        st.caption(f"ℹ️ {info['note']}")
    st.markdown("---")
    st.markdown("##### Why this matters for investors")
    st.markdown(
        "Every stock price is ultimately a bet on the people, decisions, and culture behind a company. "
        "The stories above are reminders that today's trillion-dollar valuations were shaped by specific "
        "moments — a dorm room, a licensing deal, a product launch, a market entry. Understanding that "
        "history adds context to every chart in this dashboard."
    )
    st.markdown("")
    st.caption(f"Source: {info['source']} · Fetched June 2026.")
