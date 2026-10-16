"""Pull CFBD data into data/raw/*.parquet. Usage: python scripts/pull_data.py [year ...]"""
import sys
from cfbmeaning import cfbd
from cfbmeaning.config import SEASON

years = [int(a) for a in sys.argv[1:]] or [SEASON]
for Y in years:
    jobs = {
        "games_regular": lambda: cfbd.get("games", year=Y, seasonType="regular"),
        "games_postseason": lambda: cfbd.get("games", year=Y, seasonType="postseason"),
        "lines": lambda: cfbd.get("lines", year=Y),
        "teams_fbs": lambda: cfbd.get("teams/fbs", year=Y),
        "rankings": lambda: cfbd.get("rankings", year=Y),
        "elo": lambda: cfbd.get("ratings/elo", year=Y),
        "sp": lambda: cfbd.get("ratings/sp", year=Y),
    }
    for name, fn in jobs.items():
        try:
            df = cfbd.cached(f"{name}_{Y}", fn, refresh=True)
            print(f"{Y} {name}: {len(df)} rows")
        except Exception as e:
            print(f"{Y} {name}: FAILED {e}")
