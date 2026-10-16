import os
import pandas as pd
import requests
from dotenv import load_dotenv
from .config import ROOT, RAW

BASE = "https://api.collegefootballdata.com"
load_dotenv(ROOT / ".env")


def _headers():
    key = os.environ.get("CFB_DATA_KEY")
    if not key:
        raise RuntimeError("CFB_DATA_KEY not set in .env")
    return {"Authorization": f"Bearer {key}"}


def get(endpoint: str, **params) -> pd.DataFrame:
    r = requests.get(f"{BASE}/{endpoint}", params=params, headers=_headers(), timeout=60)
    r.raise_for_status()
    return pd.json_normalize(r.json())


def cached(name: str, fn, refresh: bool = False) -> pd.DataFrame:
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / f"{name}.parquet"
    if path.exists() and not refresh:
        return pd.read_parquet(path)
    df = fn()
    df.to_parquet(path)
    return df
