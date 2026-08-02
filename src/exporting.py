"""Scraping result exports."""

import json

import pandas as pd


def csv_bytes(dataframe: pd.DataFrame) -> bytes:
    return dataframe.to_csv(index=False).encode("utf-8-sig")


def json_bytes(dataframe: pd.DataFrame) -> bytes:
    return json.dumps(dataframe.to_dict(orient="records"), ensure_ascii=False, indent=2).encode("utf-8")
