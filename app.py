import random
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
        /* ── Layout ── */
        .block-container {
            padding-top: 2.5rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        /* ── Global font size boost ── */
        html, body, [class*="css"] {
            font-size: 17px !important;
        }

        /* ── Page title ── */
        h1 {
            font-size: 2.4rem !important;
            font-weight: 700 !important;
            color: #0d2b45 !important;
            letter-spacing: -0.5px;
        }

        /* ── Section headings (st.subheader) ── */
        h2 {
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            color: #0d2b45 !important;
            margin-top: 0.5rem !important;
        }

        /* ── Sub-section headings (##### markdown) ── */
        h5 {
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            color: #1B4F72 !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.6rem !important;
        }

        /* ── Body text & captions ── */
        p, li { font-size: 1rem !important; line-height: 1.7; color: #2c3e50; }
        [data-testid="stCaptionContainer"] p {
            font-size: 0.88rem !important;
            color: #6b7a8d !important;
        }

        /* ── Metric cards ── */
        [data-testid="metric-container"] {
            background: #ffffff;
            border: 1px solid #cdd6e4;
            border-top: 4px solid #1B4F72;
            border-radius: 10px;
            padding: 1.2rem 1.4rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            color: #6b7a8d !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.9rem !important;
            font-weight: 700 !important;
            color: #0d2b45 !important;
        }
        [data-testid="stMetricDelta"] {
            font-size: 1rem !important;
            font-weight: 500 !important;
        }

        /* ── Tab labels ── */
        [data-testid="stTab"] button {
            font-size: 1rem !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.2rem !important;
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background-color: #0d2b45 !important;
        }
        [data-testid="stSidebar"] * {
            color: #dce6f0 !important;
        }
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #ffffff !important;
        }

        /* ── Divider ── */
        hr { border-color: #dde3ed; margin: 1.8rem 0; }

        /* ── Alert / info boxes ── */
        [data-testid="stAlert"] p { font-size: 1rem !important; }

        /* ── Mobile tweaks ── */
        @media (max-width: 768px) {
            .block-container {
                padding-left: 0.8rem !important;
                padding-right: 0.8rem !important;
                padding-top: 1.2rem !important;
            }
            h1 { font-size: 1.65rem !important; }
            h2 { font-size: 1.15rem !important; }
            h5 { font-size: 0.9rem !important; }
            p, li { font-size: 0.95rem !important; }
            [data-testid="stMetricValue"]  { font-size: 1.35rem !important; }
            [data-testid="stMetricLabel"]  { font-size: 0.75rem !important; }
            [data-testid="metric-container"] { padding: 0.8rem 0.9rem !important; }
            [data-testid="stTab"] button {
                font-size: 0.78rem !important;
                padding: 0.4rem 0.5rem !important;
            }
        }
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

    # ── Sidebar Did You Know ──────────────────────────────────────────────────
    _sidebar_facts = [
        ("Apple 🍎",     "Apple operates over 540 retail stores worldwide — each location is designed to serve as a community space as much as a shop."),
        ("Google 🔍",    "Google's first server was built from Lego bricks in a Stanford dorm room. The founders originally called it 'Backrub'."),
        ("Amazon 📦",    "Amazon has helped digitize 12 million small businesses and supported 2.8 million jobs in India alone."),
        ("Netflix 📺",   "Netflix now entertains over half a billion people in more than 190 countries across 50 different languages."),
        ("Meta 🌐",      "Facebook launched in 2004 to connect a single university campus. Today Meta owns four apps each used by over a billion people."),
        ("Microsoft 💻", "IBM launched its first personal computer on August 12, 1981 — running Microsoft's MS-DOS 1.0, the deal that built Microsoft's empire."),
        ("Nike 👟",      "Between 1994 and 1998 Nike signed Brazil & US Soccer and launched the first Mercurial boot — the four years that made Nike a global football brand."),
    ]
    import datetime as _dt
    random.seed(int(_dt.date.today().strftime("%Y%m%d")))
    _company, _fact = random.choice(_sidebar_facts)

    st.markdown(
        f"""
        <div style="
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.18);
            border-left: 4px solid #7ecbf7;
            border-radius: 8px;
            padding: 1rem 1.1rem;
            margin-top: 0.2rem;
        ">
            <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.1em;
                        text-transform:uppercase;color:#7ecbf7;margin-bottom:0.4rem;">
                💡 Did You Know?
            </div>
            <div style="font-size:0.82rem;font-weight:600;color:#ffffff;margin-bottom:0.3rem;">
                {_company}
            </div>
            <div style="font-size:0.8rem;color:#c0d8ee;line-height:1.5;">
                {_fact}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Filter & re-index to the selected date range ──────────────────────────────
mask = (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)
dff = df[mask].copy().reset_index(drop=True)

if dff.empty:
    st.warning("No data found for this date range. Please widen the window.")
    st.stop()

for t in tickers:
    first = dff[t].iloc[0]
    if first != 0:
        dff[t] = dff[t] / first

# ── Pre-compute shared metrics ────────────────────────────────────────────────
growths    = {t: (dff[t].iloc[-1] - 1) * 100 for t in chosen}
best_stock = max(growths, key=growths.get)
daily_vol  = {t: dff[t].pct_change().std() * 100 for t in chosen}
most_vol   = max(daily_vol, key=daily_vol.get)

COLORS = px.colors.qualitative.Set2
CHART_LAYOUT = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(t=40, b=20),
    font=dict(family="sans-serif"),
)

# ── Page title ────────────────────────────────────────────────────────────────
st.title("📈 Big Tech Stock Explorer")
st.markdown(
    "An interactive dashboard for analysing the historical performance of major technology stocks. "
    "Use the sidebar to select stocks and adjust the date range — all charts and figures update instantly."
)
st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_overview, tab_calculator, tab_peak, tab_insights, tab_funfacts = st.tabs(
    ["📊  Overview & Charts", "💰  Investment Calculator", "🏔️  Peak Tracker", "💡  Market Insights", "🎯  Fun Facts"]
)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 · Overview & Charts
# ─────────────────────────────────────────────────────────────────────────────
with tab_overview:
    st.subheader("How did each stock perform?")
    st.markdown(
        f"Results cover **{start_date.strftime('%b %Y')}** to **{end_date.strftime('%b %Y')}**. "
        "A reading of 2.00× means the stock doubled during that window. "
        "The percentage below each figure shows the same result as a percentage gain or loss."
    )

    st.markdown("##### Stock-by-stock results")
    _per_row = 3
    for _row_start in range(0, len(chosen), _per_row):
        _row_tickers = chosen[_row_start : _row_start + _per_row]
        _row_cols = st.columns(len(_row_tickers))
        for col, t in zip(_row_cols, _row_tickers):
            col.metric(
                label=t,
                value=f"{dff[t].iloc[-1]:.2f}×",
                delta=f"{growths[t]:+.1f}%",
            )

    st.markdown("---")
    st.markdown("##### Highlights")

    hi1, hi2 = st.columns(2)

    with hi1:
        st.metric(
            label="🏆  Best Performer",
            value=best_stock,
            delta=f"{growths[best_stock]:+.1f}% total growth",
        )
        st.caption("The stock that grew the most over the selected period.")

    with hi2:
        st.metric(
            label="📊  Most Volatile",
            value=most_vol,
            delta=f"±{daily_vol[most_vol]:.2f}% average daily move",
            delta_color="off",
        )
        st.caption(
            "The stock whose price moved up and down the most from day to day. "
            "Higher volatility can mean bigger gains — but also bigger losses."
        )

    st.markdown("---")
    st.subheader("Price trends over time")
    st.markdown(
        "The line chart tracks each stock's relative price from the start of your chosen period. "
        "All stocks start at 1.0, so you can compare growth directly regardless of their actual price."
    )

    fig_line = px.line(
        dff,
        x="date",
        y=chosen,
        labels={"value": "Relative price (1.0 = start of range)", "date": "Date", "variable": "Stock"},
        color_discrete_sequence=COLORS,
    )
    fig_line.update_layout(
        **CHART_LAYOUT,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        legend_title_text="",
    )
    fig_line.update_xaxes(showgrid=False, title_text="")
    fig_line.update_yaxes(gridcolor="#EEF0F5", title_text="Relative price")
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")
    st.markdown("##### Total growth, side by side")
    st.caption("Sorted from highest to lowest. Figures show percentage change over the full selected period.")

    growth_df = (
        pd.DataFrame({"Stock": list(growths.keys()), "Growth (%)": list(growths.values())})
        .sort_values("Growth (%)", ascending=False)
        .reset_index(drop=True)
    )

    fig_bar = px.bar(
        growth_df,
        x="Stock",
        y="Growth (%)",
        color="Stock",
        text_auto=".1f",
        color_discrete_sequence=COLORS,
    )
    fig_bar.update_traces(textposition="outside", textfont_size=13)
    fig_bar.update_layout(
        **CHART_LAYOUT,
        showlegend=False,
        uniformtext_minsize=8,
    )
    fig_bar.update_xaxes(showgrid=False, title_text="")
    fig_bar.update_yaxes(gridcolor="#EEF0F5", title_text="Total growth (%)")
    st.plotly_chart(fig_bar, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 · Investment Calculator
# ─────────────────────────────────────────────────────────────────────────────
with tab_calculator:
    st.subheader("What would my investment be worth?")
    st.markdown(
        "Enter an amount below and pick a stock to see how that money would have grown "
        "if you had invested it at the start of the selected period."
    )

    st.markdown("##### Your inputs")
    _calc_col1, _calc_col2 = st.columns([1, 1])
    with _calc_col1:
        invest_amount = st.number_input(
            "Starting investment ($)",
            min_value=1,
            value=1000,
            step=100,
            help="The amount you would have invested on the first day of the period.",
        )
    with _calc_col2:
        invest_stock = st.selectbox(
            "Stock to invest in",
            options=chosen,
            help="Only one stock can be calculated at a time.",
        )

    final_value = invest_amount * dff[invest_stock].iloc[-1]
    profit      = final_value - invest_amount
    growth_pct  = growths[invest_stock]
    is_gain     = profit >= 0

    st.markdown("##### Results")
    rc1, rc2, rc3 = st.columns(3)
    rc1.metric("Invested", f"${invest_amount:,.0f}")
    rc2.metric("End value", f"${final_value:,.2f}", delta=f"{growth_pct:+.1f}%")
    rc3.metric("Gain" if is_gain else "Loss", f"${abs(profit):,.2f}")

    st.markdown("")

    if is_gain:
        st.success(
            f"An investment of ${invest_amount:,.0f} in {invest_stock} at the start of this period "
            f"would have grown to ${final_value:,.2f} — "
            f"a gain of ${profit:,.2f} ({growth_pct:+.1f}%)."
        )
    else:
        st.error(
            f"An investment of ${invest_amount:,.0f} in {invest_stock} at the start of this period "
            f"would have fallen to ${final_value:,.2f} — "
            f"a loss of ${abs(profit):,.2f} ({growth_pct:+.1f}%)."
        )

    st.caption(
        "This calculator assumes you bought on the first day of the selected period "
        "and sold on the last day. It does not account for taxes, broker fees, or dividends."
    )


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 · Peak Tracker
# ─────────────────────────────────────────────────────────────────────────────
with tab_peak:
    st.subheader("When did a stock reach its highest point?")
    st.markdown(
        "Select a stock to find the exact date it hit its highest price "
        "within your chosen date range. The chart below marks that peak with a star."
    )

    peak_stock = st.selectbox(
        "Which stock would you like to track?",
        options=chosen,
        key="peak_select",
    )

    peak_idx   = dff[peak_stock].idxmax()
    peak_date  = dff.loc[peak_idx, "date"]
    peak_value = dff.loc[peak_idx, peak_stock]
    days_ago   = (dff["date"].iloc[-1] - peak_date).days

    pk1, pk2, pk3 = st.columns(3)
    pk1.metric("Stock", peak_stock)
    pk2.metric("Peak date", peak_date.strftime("%d %b %Y"))
    pk3.metric("Peak value", f"{peak_value:.2f}×", help="Relative to the price at the start of the selected period.")

    if days_ago == 0:
        st.info(f"{peak_stock} reached its peak on the very last day of the selected range.")
    elif days_ago <= 30:
        st.info(f"{peak_stock} hit its highest point just {days_ago} day(s) before the end of the selected range.")
    else:
        st.info(
            f"{peak_stock} reached its peak on {peak_date.strftime('%d %b %Y')} "
            f"— {days_ago} days before the end of the selected range."
        )

    st.markdown("---")

    fig_peak = px.line(
        dff,
        x="date",
        y=peak_stock,
        labels={"date": "Date", peak_stock: "Relative price"},
        color_discrete_sequence=["#2E86AB"],
    )
    fig_peak.add_scatter(
        x=[peak_date],
        y=[peak_value],
        mode="markers+text",
        marker=dict(color="#E63946", size=14, symbol="star"),
        text=[f"  Peak: {peak_value:.2f}×"],
        textposition="top right",
        name="Peak",
    )
    fig_peak.update_layout(
        **CHART_LAYOUT,
        title=f"{peak_stock} — price history with peak highlighted",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig_peak.update_xaxes(showgrid=False, title_text="")
    fig_peak.update_yaxes(gridcolor="#EEF0F5", title_text="Relative price")
    st.plotly_chart(fig_peak, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 · Market Insights  —  per-company facts
# ─────────────────────────────────────────────────────────────────────────────

# Company data — facts sourced from official company websites (fetched June 2026)
COMPANY_INSIGHTS = {
    "Apple 🍎": {
        "headline": "540+ stores. One design philosophy.",
        "fact": (
            "Apple operates over 540 retail stores worldwide — more physical "
            "locations than most luxury fashion houses. Every store follows the "
            "same architectural brief: open space, natural materials, and no "
            "cash registers on countertops. Apple's stores generate more revenue "
            "per square foot than almost any other retailer on earth."
        ),
        "stats": [("Founded", "1976"), ("2025 Revenue", "$416B"), ("Retail Stores", "540+")],
        "source": "apple.com/newsroom",
        "accent": "#555555",
    },
    "Google 🔍": {
        "headline": "The billion-dollar idea that started on Lego.",
        "fact": (
            "Google's first server was built from Lego bricks in a Stanford "
            "dorm room — cheap, expandable, and good at keeping hard drives "
            "in place. The founders named the engine 'Backrub' before renaming "
            "it Google, a play on 'googol' (1 followed by 100 zeros), reflecting "
            "their mission to organise the world's information. The first "
            "external cheque — $100,000 from Sun co-founder Andy Bechtolsheim — "
            "was written before Google was even incorporated."
        ),
        "stats": [("Founded", "1998"), ("First investment", "$100K"), ("Countries", "190+")],
        "source": "about.google/our-story",
        "accent": "#4285F4",
    },
    "Amazon 📦": {
        "headline": "From books to billions of livelihoods.",
        "fact": (
            "Amazon's mission is simply to make customers' lives better and "
            "easier every day. Since launching in India, Amazon has helped "
            "digitize 12 million small businesses and supported 2.8 million "
            "jobs — a snapshot of how e-commerce reshapes local economies "
            "at scale. Today Amazon spans online shopping, cloud computing, "
            "AI services, streaming, healthcare, and more."
        ),
        "stats": [("Founded", "1994"), ("Small biz digitized", "12M"), ("Jobs supported (India)", "2.8M")],
        "source": "aboutamazon.com",
        "accent": "#FF9900",
    },
    "Netflix 📺": {
        "headline": "Half a billion fans. 190 countries. 50 languages.",
        "fact": (
            "Netflix started as a DVD-by-mail service in 1997. Today it "
            "entertains over half a billion people in more than 190 countries "
            "across 50 different languages — making it one of the most widely "
            "distributed entertainment platforms ever built. When a Netflix "
            "series becomes a hit, it drives measurable spikes in music streams, "
            "book sales, fashion trends, and even tourism."
        ),
        "stats": [("Founded", "1997"), ("Subscribers", "500M+"), ("Countries", "190+")],
        "source": "about.netflix.com",
        "accent": "#E50914",
    },
    "Meta 🌐": {
        "headline": "One dorm room. Four billion-user apps.",
        "fact": (
            "When Facebook launched in 2004, its only goal was to connect a "
            "single university campus. Meta now owns Facebook, Instagram, "
            "WhatsApp, and Messenger — four of the world's most-used apps, "
            "each serving over a billion people. Meta is now moving beyond "
            "2D screens entirely, investing heavily in mixed reality and AI "
            "to build what it calls the next evolution in social technology."
        ),
        "stats": [("Founded", "2004"), ("Apps with 1B+ users", "4"), ("Mission", "Connect the world")],
        "source": "about.meta.com/company-info",
        "accent": "#0082FB",
    },
    "Microsoft 💻": {
        "headline": "The deal that built the PC era.",
        "fact": (
            "On August 12, 1981, IBM launched its first personal computer "
            "running Microsoft's MS-DOS 1.0 — a licensing deal that handed "
            "Microsoft control of the operating system for an entire industry. "
            "Microsoft went public on March 13, 1986. By October 2012, "
            "Microsoft employee charitable giving had crossed $1 billion — "
            "one of the largest corporate employee giving programmes in history."
        ),
        "stats": [("Founded", "1975"), ("IPO date", "Mar 1986"), ("Employee giving", "$1B+")],
        "source": "news.microsoft.com/facts-about-microsoft",
        "accent": "#00A4EF",
    },
    "Nike 👟": {
        "headline": "Four years that launched a global football empire.",
        "fact": (
            "Between 1994 and 1998, Nike signed both the Brazil and U.S. Soccer "
            "national teams, debuted iconic advertising campaigns, and launched "
            "the first-ever Mercurial boot — the lightest football boot of its "
            "time. Those four years transformed Nike from a running and basketball "
            "brand into the world's dominant force in football, a position it "
            "has held ever since."
        ),
        "stats": [("Founded", "1964"), ("Countries", "190+"), ("Breakthrough era", "1994–1998")],
        "source": "about.nike.com",
        "accent": "#111111",
        "note": "Nike (NKE) is not in the Plotly stock dataset used by this app's charts.",
    },
}

with tab_insights:
    st.subheader("Market Insights")
    st.markdown(
        "Select a company below to explore a curated business fact — "
        "each sourced directly from the company's own public website."
    )

    selected_company = st.selectbox(
        "Choose a company",
        options=list(COMPANY_INSIGHTS.keys()),
        index=0,
    )

    info = COMPANY_INSIGHTS[selected_company]
    accent = info["accent"]

    st.markdown("---")

    # ── Hero fact card ─────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #0d2b45 0%, #1B4F72 100%);
            border-left: 6px solid {accent};
            border-radius: 14px;
            padding: 2.2rem 2.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(13,43,69,0.18);
        ">
            <div style="font-size:0.75rem;font-weight:700;letter-spacing:0.12em;
                        text-transform:uppercase;color:#7ecbf7;margin-bottom:0.6rem;">
                💡 Did You Know?
            </div>
            <div style="font-size:1.45rem;font-weight:700;color:#ffffff;
                        line-height:1.4;margin-bottom:1rem;">
                {info['headline']}
            </div>
            <div style="font-size:1rem;color:#c0d8ee;line-height:1.7;">
                {info['fact']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Stat pills ─────────────────────────────────────────────────────────────
    st.markdown("##### Key figures")
    stat_cols = st.columns(len(info["stats"]))
    for col, (label, value) in zip(stat_cols, info["stats"]):
        col.metric(label=label, value=value)

    # ── Optional note (e.g. Nike not in dataset) ───────────────────────────────
    if "note" in info:
        st.caption(f"ℹ️ {info['note']}")

    st.markdown("---")

    # ── Takeaway ───────────────────────────────────────────────────────────────
    st.markdown("##### Why this matters for investors")
    st.markdown(
        "Every stock price is ultimately a bet on the people, decisions, and culture behind "
        "a company. The stories above are reminders that today's trillion-dollar valuations "
        "were shaped by specific moments — a dorm room, a licensing deal, a product launch, "
        "a market entry. Understanding that history adds context to every chart in this dashboard."
    )

    st.markdown("")
    st.caption(f"Source: {info['source']} · Fetched June 2026.")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 · Fun Facts — True / False Quiz
# Facts sourced from official public pages (fetched June 2026)
# ─────────────────────────────────────────────────────────────────────────────

QUIZ_FACTS = [
    {
        "company": "Apple 🍎",
        "statement": "Apple's IPO share price was $22.00 per share when it went public on December 12, 1980.",
        "answer": True,
        "right_msg": "Correct! Apple went public at exactly $22.00 per share.",
        "wrong_msg": "Not quite — Apple's IPO was priced at $22.00 per share on December 12, 1980.",
        "detail": "After five stock splits, that original $22 share is worth just $0.10 on a split-adjusted basis today — yet Apple became the most valuable company in history.",
        "source": "investor.apple.com/faq",
        "accent": "#555555",
    },
    {
        "company": "Apple 🍎",
        "statement": "Apple's stock has split exactly three times since the company went public.",
        "answer": False,
        "right_msg": "Correct! Apple's stock has actually split five times — not three.",
        "wrong_msg": "Apple's stock has split five times in total, not three.",
        "detail": "The five splits were: June 1987 (2-for-1), June 2000 (2-for-1), Feb 2005 (2-for-1), June 2014 (7-for-1), and August 2020 (4-for-1).",
        "source": "investor.apple.com/faq",
        "accent": "#555555",
    },
    {
        "company": "Microsoft 💻",
        "statement": "Microsoft was founded in 1975 — the same year early personal computer kits first went on sale.",
        "answer": True,
        "right_msg": "Correct! Microsoft was founded in 1975 by Bill Gates and Paul Allen.",
        "wrong_msg": "Microsoft was actually founded in 1975 by Bill Gates and Paul Allen.",
        "detail": "Microsoft was created specifically to write software for the Altair 8800, one of the first personal computers sold as a kit to hobbyists.",
        "source": "news.microsoft.com/facts-about-microsoft",
        "accent": "#00A4EF",
    },
    {
        "company": "Microsoft 💻",
        "statement": "Microsoft launched the original Xbox gaming console in 2001.",
        "answer": True,
        "right_msg": "Correct! The original Xbox launched on November 15, 2001.",
        "wrong_msg": "Xbox did launch in 2001 — on November 15, 2001 to be exact.",
        "detail": "Microsoft entered the console market with Xbox on November 15, 2001, going head-to-head with Sony's PlayStation 2 and Nintendo's GameCube.",
        "source": "news.microsoft.com/facts-about-microsoft",
        "accent": "#00A4EF",
    },
    {
        "company": "Microsoft 💻",
        "statement": "Microsoft acquired Skype in 2015.",
        "answer": False,
        "right_msg": "Correct! Microsoft acquired Skype in 2011, not 2015.",
        "wrong_msg": "Microsoft actually closed its acquisition of Skype in October 2011 — not 2015.",
        "detail": "Microsoft closed the Skype acquisition on October 13, 2011. At the time it was one of Microsoft's largest acquisitions ever at $8.5 billion.",
        "source": "news.microsoft.com/facts-about-microsoft",
        "accent": "#00A4EF",
    },
    {
        "company": "Google / Alphabet 🔍",
        "statement": "YouTube, Chrome, Android, and Google Maps each have over one billion users.",
        "answer": True,
        "right_msg": "Correct! All four have each crossed the one billion user milestone.",
        "wrong_msg": "Actually, all four — YouTube, Chrome, Android, and Google Maps — do have over a billion users each.",
        "detail": "Alphabet's founders described these as things that 'seemed crazy at the time' but each now have over a billion users, as confirmed on abc.xyz.",
        "source": "abc.xyz (Alphabet founders' letter)",
        "accent": "#4285F4",
    },
    {
        "company": "Google / Alphabet 🔍",
        "statement": 'The name "Alphabet" partly refers to "alpha" — a finance term for investment return above benchmark.',
        "answer": True,
        "right_msg": "Correct! The double meaning is confirmed in Alphabet's own founding letter on abc.xyz.",
        "wrong_msg": 'The name does partly mean "alpha-bet" — with alpha being the finance term for returns above benchmark.',
        "detail": 'From abc.xyz: "We also like that it means alpha-bet (Alpha is investment return above benchmark), which we strive for!"',
        "source": "abc.xyz (Alphabet founders' letter)",
        "accent": "#4285F4",
    },
    {
        "company": "Netflix 📺",
        "statement": "Netflix is available in more than 190 countries and offers content in over 50 languages.",
        "answer": True,
        "right_msg": "Correct! Netflix is one of the most globally distributed entertainment platforms ever built.",
        "wrong_msg": "Netflix is indeed available in 190+ countries across 50+ languages.",
        "detail": 'Netflix states on about.netflix.com: "We are entertaining over half a billion people in more than 190 countries and 50 languages."',
        "source": "about.netflix.com",
        "accent": "#E50914",
    },
    {
        "company": "Meta 🌐",
        "statement": "Facebook was launched in 2004.",
        "answer": True,
        "right_msg": "Correct! Facebook launched in 2004 and changed the way people connect.",
        "wrong_msg": "Facebook did launch in 2004 — from Mark Zuckerberg's Harvard dorm room.",
        "detail": 'Meta confirms on about.meta.com: "When Facebook launched in 2004, it changed the way people connect."',
        "source": "about.meta.com/company-info",
        "accent": "#0082FB",
    },
    {
        "company": "Meta 🌐",
        "statement": "Meta charges users a monthly subscription fee to use Facebook and Instagram.",
        "answer": False,
        "right_msg": "Correct! Meta's services are free — revenue comes from advertising, not subscriptions.",
        "wrong_msg": "Meta's core services are actually free. The business model is advertising.",
        "detail": 'Meta states on about.meta.com: "our business model is ads so our services can be free." This ad model generated over $160 billion in revenue in 2024.',
        "source": "about.meta.com/company-info",
        "accent": "#0082FB",
    },
    {
        "company": "Nvidia 🟢",
        "statement": 'NVIDIA describes itself as having "pioneered accelerated computing".',
        "answer": True,
        "right_msg": "Correct! That's NVIDIA's own phrasing from their official About page.",
        "wrong_msg": 'NVIDIA does use this exact phrase on its about page: "NVIDIA pioneered accelerated computing."',
        "detail": "NVIDIA positions accelerated computing — not just gaming GPUs — as its defining contribution to technology, now driving the AI revolution.",
        "source": "nvidia.com/en-us/about-nvidia",
        "accent": "#76B900",
    },
    {
        "company": "Apple 🍎",
        "statement": "On a split-adjusted basis, Apple's original 1980 IPO share price was just $0.10.",
        "answer": True,
        "right_msg": "Correct! Five stock splits turned that $22 IPO price into $0.10 on a split-adjusted basis.",
        "wrong_msg": "Apple's $22 IPO price is indeed just $0.10 on a split-adjusted basis today, after five stock splits.",
        "detail": "Stated directly on investor.apple.com: 'on a split-adjusted basis the IPO share price was $.10.' A powerful reminder of the wealth Apple has created for long-term shareholders.",
        "source": "investor.apple.com/faq",
        "accent": "#555555",
    },
]

with tab_funfacts:
    st.subheader("🎯 Fun Facts Quiz")
    st.markdown(
        "How well do you know the world's biggest tech companies? "
        "Read each statement and decide whether it is **True** or **False**."
    )

    # ── Session state initialisation ──────────────────────────────────────────
    for _k, _v in [("q_idx", 0), ("q_answered", False), ("q_chosen", None), ("q_score", 0)]:
        if _k not in st.session_state:
            st.session_state[_k] = _v

    _total = len(QUIZ_FACTS)
    _idx   = st.session_state.q_idx

    # ── Progress bar ──────────────────────────────────────────────────────────
    _progress_col, _score_col = st.columns([3, 1])
    with _progress_col:
        st.progress(min(_idx / _total, 1.0), text=f"Question {min(_idx + 1, _total)} of {_total}")
    with _score_col:
        st.metric("Score", f"{st.session_state.q_score} / {_idx if not st.session_state.q_answered else _idx}")

    st.markdown("---")

    # ── Final results screen ──────────────────────────────────────────────────
    if _idx >= _total:
        _score = st.session_state.q_score
        _pct   = _score / _total * 100
        if _pct == 100:
            _grade, _grade_emoji = "Perfect score!", "🏆"
        elif _pct >= 75:
            _grade, _grade_emoji = "Excellent work!", "🎉"
        elif _pct >= 50:
            _grade, _grade_emoji = "Good effort!", "📚"
        else:
            _grade, _grade_emoji = "Keep exploring!", "💡"

        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #0d2b45 0%, #1B4F72 100%);
                border-radius: 14px; padding: 2.5rem 2.5rem; text-align: center;
                box-shadow: 0 4px 20px rgba(13,43,69,0.2);
            ">
                <div style="font-size:3rem; margin-bottom:0.5rem;">{_grade_emoji}</div>
                <div style="font-size:1.6rem; font-weight:700; color:#ffffff; margin-bottom:0.5rem;">
                    Quiz Complete!
                </div>
                <div style="font-size:2.5rem; font-weight:800; color:#7ecbf7; margin-bottom:0.8rem;">
                    {_score} / {_total}
                </div>
                <div style="font-size:1.05rem; color:#c0d8ee;">
                    {_grade} You answered {_score} out of {_total} questions correctly.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("")
        if st.button("🔄  Play Again", use_container_width=True, type="primary"):
            st.session_state.q_idx      = 0
            st.session_state.q_answered = False
            st.session_state.q_chosen   = None
            st.session_state.q_score    = 0
            st.rerun()

    # ── Active question ───────────────────────────────────────────────────────
    else:
        _fact   = QUIZ_FACTS[_idx]
        _accent = _fact["accent"]

        # Question card
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #0d2b45 0%, #1B4F72 100%);
                border-left: 6px solid {_accent};
                border-radius: 14px; padding: 2rem 2.5rem; margin-bottom: 1.5rem;
                box-shadow: 0 4px 20px rgba(13,43,69,0.15);
            ">
                <div style="font-size:0.75rem; font-weight:700; letter-spacing:0.12em;
                            text-transform:uppercase; color:#7ecbf7; margin-bottom:0.5rem;">
                    {_fact['company']}
                </div>
                <div style="font-size:1.3rem; font-weight:700; color:#ffffff;
                            line-height:1.5; margin-bottom:1rem;">
                    "{_fact['statement']}"
                </div>
                <div style="font-size:0.95rem; color:#aac8e0; font-weight:500;">
                    👆 Is this True or False?
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Buttons (only show before answering)
        if not st.session_state.q_answered:
            _b1, _b2 = st.columns(2)
            if _b1.button("✅   True", use_container_width=True, type="primary"):
                st.session_state.q_chosen   = True
                st.session_state.q_answered = True
                if _fact["answer"] is True:
                    st.session_state.q_score += 1
                st.rerun()
            if _b2.button("❌   False", use_container_width=True):
                st.session_state.q_chosen   = False
                st.session_state.q_answered = True
                if _fact["answer"] is False:
                    st.session_state.q_score += 1
                st.rerun()

        # Feedback (show after answering)
        else:
            _correct = st.session_state.q_chosen == _fact["answer"]

            if _correct:
                st.success(f"🎉 {_fact['right_msg']}")
            else:
                _chosen_label  = "True" if st.session_state.q_chosen else "False"
                _correct_label = "True" if _fact["answer"] else "False"
                st.error(
                    f"You answered **{_chosen_label}** — the correct answer is **{_correct_label}**. "
                    f"{_fact['wrong_msg']}"
                )

            st.info(f"💡 {_fact['detail']}")
            st.caption(f"Source: {_fact['source']} · Fetched June 2026.")

            st.markdown("")
            _next_label = "Next Question  →" if _idx < _total - 1 else "See My Score  →"
            if st.button(_next_label, use_container_width=True, type="primary"):
                st.session_state.q_idx      += 1
                st.session_state.q_answered  = False
                st.session_state.q_chosen    = None
                st.rerun()
