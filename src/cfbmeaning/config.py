from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
MANUAL = ROOT / "data" / "manual"

SEASON = 2025
N_SIMS = 10_000
SEED = 42

# Std dev of final margin around the point spread (~13.5 is the common NCAAF figure)
SPREAD_SD = 13.5

# Meaning weights (tunable)
W_CFP = 1.0
W_CONF = 0.75
PLAYOFF_GAME_MEANING = 1.0  # per team, equals a 100% -> 0% game

# Bye stake: weight on change in P(first-round bye). Applies to both 12 and 24 team.
W_BYE = 0.4
BYES = {"cfp12": 4, "cfp24": 8}

# Audience weight = (fanbase_millions / max) ** AUDIENCE_EXP; teams missing from
# data/manual/brand_scores.csv get DEFAULT_FANBASE_M (G5 midpoint estimate).
AUDIENCE_EXP = 1.0
DEFAULT_FANBASE_M = 0.2

# Brand/fanbase size is NOT used in game meaning. It is only used afterwards to count how many fans
# each format helps or hurts (scripts/fan_impact.py). Set True to restore brand-weighted meaning.
USE_AUDIENCE_WEIGHTS = False

# 0-100 game score = 100 * (stake of team A + stake of team B) / SCORE_REF, capped at 100.
# A playoff game is 1.0 stake per team = 2.0 total = 100 (flat, every playoff game).
SCORE_REF = 2.0

# Playoff selection score = RATING_WEIGHT * rating (Elo/SP+ z-score) + RESUME_WEIGHT * resume.
# Resume = sum of win credits (1 + RESUME_OPP * opponent strength) - loss debits (1 - RESUME_OPP * opponent strength).
RESUME_WEIGHT = 0.5
RESUME_OPP = 0.25
