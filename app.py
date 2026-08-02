"""Streamlit interface for Ethical Web Scraping Studio."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.demo import demo_result
from src.exporting import csv_bytes, json_bytes
from src.i18n import t
from src.scraper import ScrapingError, scrape_source
from src.sources import SOURCES


RESULT_SCHEMA_VERSION = 2

st.set_page_config(page_title="Ethical Web Scraping Studio", page_icon="🕸️", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
  .stApp { background:#f7f7fb; } [data-testid="stSidebar"] { background:#24213a; } [data-testid="stSidebar"] * { color:#fafafa; }
  [data-testid="stSidebar"] [data-baseweb="select"] *, [data-testid="stSidebar"] [data-baseweb="input"] *, [data-testid="stSidebar"] input { color:#24213a !important; }
  .hero { padding:2.35rem 2.5rem; border-radius:22px; color:white; margin-bottom:1.35rem; background:linear-gradient(120deg,#24213a 0%,#594a78 58%,#b85c78 100%); box-shadow:0 14px 35px rgba(36,33,58,.17); }
  .hero h1 { color:white; margin:.2rem 0 .45rem; font-size:2.5rem; } .hero p { color:#f5e4eb; margin:0; max-width:850px; font-size:1.05rem; }
  .tag { color:#ffc1d2; font-size:.73rem; font-weight:800; letter-spacing:.14em; } .language-label { color:#64748b; font-size:.78rem; text-align:right; }
  .card { background:white; padding:1.1rem; min-height:125px; border-radius:14px; border:1px solid #e4e2eb; } .card b { color:#594a78; }
  [data-testid="stMetric"] { background:white; padding:1rem; border-radius:14px; border:1px solid #e4e2eb; box-shadow:0 5px 15px rgba(15,23,42,.04); }
  .footer { color:#64748b; font-size:.84rem; border-top:1px solid #dedbe7; margin-top:2rem; padding-top:1rem; }
</style>
""", unsafe_allow_html=True)

if "language" not in st.session_state:
    st.session_state.language = "en"
if st.session_state.get("result_schema_version") != RESULT_SCHEMA_VERSION:
    st.session_state.pop("scrape_result", None)
    st.session_state.result_schema_version = RESULT_SCHEMA_VERSION
language = st.session_state.language


def choose_language(code: str) -> None:
    st.session_state.language = code
    st.rerun()


space, pt_col, en_col, es_col = st.columns([12, 1, 1, 1], vertical_alignment="bottom")
space.markdown('<div class="language-label">Language · Idioma</div>', unsafe_allow_html=True)
for column, flag, code, label in ((pt_col, "🇧🇷", "pt", "Português"), (en_col, "🇺🇸", "en", "English"), (es_col, "🇪🇸", "es", "Español")):
    if column.button(flag, help=label, type="primary" if language == code else "secondary", key=f"lang_{code}"):
        choose_language(code)

source_labels = {t(language, "demo_source"): "demo", t(language, "books_source"): "books", t(language, "quotes_source"): "quotes"}
with st.sidebar:
    st.markdown(f"## {t(language, 'settings')}")
    source_label = st.selectbox(t(language, "source"), list(source_labels))
    max_pages = st.slider(t(language, "pages_limit"), 1, 5, 2)
    delay = st.slider(t(language, "delay"), 0.5, 2.0, 0.8, 0.1)
    timeout = st.slider(t(language, "timeout"), 5, 30, 12)
    st.markdown("---")
    st.info(f"⚖️ {t(language, 'ethics')}")

st.markdown(f'<section class="hero"><div class="tag">{t(language, "tag")}</div><h1>{t(language, "title")}</h1><p>{t(language, "subtitle")}</p></section>', unsafe_allow_html=True)
st.markdown(f"### {t(language, 'why')}")
cards = st.columns(3)
for index in range(1, 4):
    cards[index - 1].markdown(f'<div class="card"><b>{t(language, f"card{index}")}</b><p>{t(language, f"card{index}_text")}</p></div>', unsafe_allow_html=True)

source_key = source_labels[source_label]
st.caption(f"💡 {t(language, 'offline') if source_key == 'demo' else t(language, 'live')}")
if st.button(t(language, "run"), type="primary", width="stretch"):
    try:
        result = demo_result(max_pages) if source_key == "demo" else scrape_source(SOURCES[source_key], max_pages, delay, timeout)
        st.session_state.scrape_result = result
    except (ScrapingError, ValueError) as error:
        st.error(f"{t(language, 'error')}: {error}")

if "scrape_result" in st.session_state:
    result = st.session_state.scrape_result
    display_data = result.data.copy()
    if result.source == "books" and "price" in display_data.columns:
        display_data["price"] = display_data["price"].astype("string").str.replace("Â£", "£", regex=False)
    st.success(f"✓ {t(language, 'success')}")
    metrics = st.columns(5)
    metrics[0].metric(t(language, "pages"), result.pages_visited)
    metrics[1].metric(t(language, "records"), len(display_data))
    metrics[2].metric(t(language, "requests"), result.requests_made)
    metrics[3].metric(t(language, "elapsed"), f"{result.elapsed_ms / 1000:.2f} s")
    average = len(display_data) / max(result.pages_visited, 1)
    metrics[4].metric(t(language, "average"), f"{average:.1f}")

    data_tab, summary_tab, log_tab = st.tabs([t(language, "data"), t(language, "summary"), t(language, "log")])
    with data_tab:
        if display_data.empty:
            st.info(t(language, "empty"))
        else:
            st.markdown(f"#### {t(language, 'preview')}")
            st.dataframe(display_data, width="stretch", hide_index=True)
    with summary_tab:
        numeric = display_data.select_dtypes(include="number")
        if not numeric.empty:
            st.markdown(f"#### {t(language, 'numeric')}")
            st.dataframe(numeric.describe().T, width="stretch")
        categorical = display_data.select_dtypes(exclude="number")
        if not categorical.empty:
            first_column = categorical.columns[0]
            counts = categorical[first_column].value_counts().head(10)
            st.markdown(f"#### {t(language, 'categories')}: `{first_column}`")
            st.bar_chart(counts, color="#b85c78")
    with log_tab:
        st.dataframe(result.log, width="stretch", hide_index=True)

    left, right = st.columns(2)
    left.download_button(t(language, "download_csv"), csv_bytes(display_data), f"{result.source}_scraped_data.csv", "text/csv", type="primary", width="stretch")
    right.download_button(t(language, "download_json"), json_bytes(display_data), f"{result.source}_scraped_data.json", "application/json", width="stretch")

st.markdown(f'<div class="footer">{t(language, "footer")}</div>', unsafe_allow_html=True)
