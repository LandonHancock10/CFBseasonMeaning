"""Leverage = |P(indicator | team wins) - P(indicator | team loses)|, from sims."""
import numpy as np
import pandas as pd
from . import config as C


def audience_weights(path=C.MANUAL / "brand_scores.csv") -> dict:
    df = pd.read_csv(path)
    mx = df["fanbase_millions"].max()
    w = (df.set_index("team")["fanbase_millions"] / mx) ** C.AUDIENCE_EXP
    default = (C.DEFAULT_FANBASE_M / mx) ** C.AUDIENCE_EXP
    return w.to_dict(), default


def _lev(ind: np.ndarray, team_won: np.ndarray) -> float:
    """ind: (n_sims,) bool for the team; team_won: (n_sims,) bool."""
    if team_won.all() or (~team_won).all():
        return 0.0
    return abs(ind[team_won].mean() - ind[~team_won].mean())


def game_meaning(outcome, h, a, cfp, conf, bye, rivalry=0.0, weights=None, default_w=0.0, home=None, away=None):
    """outcome: (n_sims,) True=home wins. h/a: team column indices.
    cfp/conf/bye: (n_sims, n_teams) bool. Returns (home_meaning, away_meaning, total)."""
    out = []
    for idx, won, name in ((h, outcome, home), (a, ~outcome, away)):
        m = (C.W_CFP * _lev(cfp[:, idx], won) + C.W_CONF * _lev(conf[:, idx], won)
             + C.W_BYE * _lev(bye[:, idx], won) + rivalry)
        w = (weights or {}).get(name, default_w)
        out.append(m * w)
    return out[0], out[1], out[0] + out[1]
