# 📈 Big Tech Stock Explorer

An interactive stock market dashboard built with **Streamlit** and **Plotly** for business school analysis.

## Features

| Tab | What it does |
|---|---|
| 📊 Overview & Charts | Compare normalised stock prices and total growth across selected companies |
| 💰 Investment Calculator | See what a hypothetical investment would be worth over any date range |
| 🏔️ Peak Tracker | Find the exact date a stock hit its highest price in the selected period |
| 💡 Market Insights | Curated company facts sourced from official websites (Apple, Google, Amazon, Netflix, Meta, Microsoft, Nike) |

## Getting started

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Data source

Uses the **built-in Plotly stock dataset** — no external APIs or data files required.  
Tickers available: `AAPL`, `GOOG`, `AMZN`, `FB` (Meta), `MSFT`, `NFLX`.

## Tech stack

- [Streamlit](https://streamlit.io/) — dashboard framework
- [Plotly Express](https://plotly.com/python/plotly-express/) — interactive charts
- [Pandas](https://pandas.pydata.org/) — data manipulation

---

Built as a business school data analytics project.
