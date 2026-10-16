"""Weekly-frozen Monte Carlo. Games with week < freeze_week use actual results;
the rest are sampled from pre-game win probabilities."""
import numpy as np
import pandas as pd
from .config import N_SIMS, SEED


def simulate_outcomes(games: pd.DataFrame, freeze_week: int, n_sims: int = N_SIMS, seed: int = SEED):
    """games needs: week, p_home, home_won (bool/NaN until played).
    Returns bool array (n_sims, n_games): True = home team wins."""
    rng = np.random.default_rng(seed + freeze_week)
    draws = rng.random((n_sims, len(games))) < games["p_home"].to_numpy()
    locked = (games["week"] < freeze_week).to_numpy()
    actual = games["home_won"].fillna(False).to_numpy(bool)
    draws[:, locked] = actual[locked]
    return draws


def team_wins(games: pd.DataFrame, outcomes: np.ndarray, teams: list[str]) -> np.ndarray:
    """(n_sims, n_teams) win totals from simulated outcomes."""
    idx = {t: i for i, t in enumerate(teams)}
    h = games["home"].map(idx).to_numpy()
    a = games["away"].map(idx).to_numpy()
    w = np.zeros((outcomes.shape[0], len(teams)), dtype=np.int16)
    for g in range(outcomes.shape[1]):
        w[np.arange(outcomes.shape[0]), np.where(outcomes[:, g], h[g], a[g])] += 1
    return w
