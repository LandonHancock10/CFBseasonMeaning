import math
import numpy as np
from .config import SPREAD_SD

_erf = np.vectorize(math.erf)


def spread_to_wp(home_spread):
    """CFBD spread is from the home team's view (negative = home favored).
    Home win prob = P(margin > 0) with margin ~ N(-spread, SD)."""
    s = np.asarray(home_spread, dtype=float)
    return 0.5 * (1 + _erf((-s) / (SPREAD_SD * math.sqrt(2))))


def elo_to_wp(home_elo, away_elo, home_field=55):
    d = np.asarray(home_elo, dtype=float) + home_field - np.asarray(away_elo, dtype=float)
    return 1 / (1 + 10 ** (-d / 400))
