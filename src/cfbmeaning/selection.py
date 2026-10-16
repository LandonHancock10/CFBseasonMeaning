"""Pluggable playoff selection: simulated season state -> field of teams.
A selector takes (wins, losses, rating, conf_champs) arrays per sim and returns
a bool array (n_sims, n_teams) of CFP qualifiers."""
from typing import Protocol
import numpy as np


class Selector(Protocol):
    n_teams: int
    def __call__(self, wins: np.ndarray, rating: np.ndarray, conf_champ: np.ndarray) -> np.ndarray: ...


class RulesSelector:
    """Rules-based: auto-bids for top-N conference champions + at-large by
    composite of rating and wins. PLACEHOLDER pending your format decisions."""
    def __init__(self, n_teams: int = 12, n_auto: int = 5, resume_weight: float = 0.5):
        self.n_teams, self.n_auto, self.resume_weight = n_teams, n_auto, resume_weight

    def select(self, wins, rating, conf_champ):
        field = self._field(wins, rating, conf_champ)
        score = np.where(field, rating[None, :] + self.resume_weight * wins, -np.inf)
        bye = np.zeros_like(field)
        np.put_along_axis(bye, np.argsort(-score, axis=1)[:, :4], True, axis=1)  # 2025: top 4 ranked
        return field, bye

    def __call__(self, wins, rating, conf_champ):
        return self._field(wins, rating, conf_champ)

    def _field(self, wins, rating, conf_champ):
        score = rating[None, :] + self.resume_weight * wins  # crude; tune later
        n_sims, n_t = score.shape
        field = np.zeros((n_sims, n_t), bool)
        champ_score = np.where(conf_champ, score, -np.inf)
        for _ in range(self.n_auto):
            top = champ_score.argmax(axis=1)
            ok = np.isfinite(champ_score[np.arange(n_sims), top])
            field[np.arange(n_sims)[ok], top[ok]] = True
            champ_score[np.arange(n_sims), top] = -np.inf
        rest = np.where(field, -np.inf, score)
        for _ in range(self.n_teams - self.n_auto):
            top = rest.argmax(axis=1)
            field[np.arange(n_sims), top] = True
            rest[np.arange(n_sims), top] = -np.inf
        return field




class CFP24Selector:
    """24 teams: winner of each P4 conference auto-bids, highest-rated G6
    champion auto-bids, remaining spots at-large by rating + resume. Top 8
    by score receive byes (champions not guaranteed one). Returns field and
    bye masks via .select()."""
    n_teams = 24

    def __init__(self, is_p4_conf: np.ndarray, conf_id: np.ndarray, resume_weight: float = 0.5):
        self.is_p4 = np.asarray(is_p4_conf, bool)   # per team
        self.conf_id = np.asarray(conf_id)          # per team
        self.resume_weight = resume_weight

    def select(self, wins, rating, conf_champ):
        score = rating[None, :] + self.resume_weight * wins
        n_sims, n_t = score.shape
        rows = np.arange(n_sims)
        field = np.zeros((n_sims, n_t), bool)
        # P4 champions auto
        field |= conf_champ & self.is_p4[None, :]
        # best G6 champion auto
        g6 = np.where(conf_champ & ~self.is_p4[None, :], score, -np.inf)
        best = g6.argmax(axis=1)
        ok = np.isfinite(g6[rows, best])
        field[rows[ok], best[ok]] = True
        # at-large fill to 24
        rest = np.where(field, -np.inf, score)
        need = 24 - field.sum(axis=1)
        for k in range(int(need.max())):
            top = rest.argmax(axis=1)
            take = need > k
            field[rows[take], top[take]] = True
            rest[rows, top] = -np.inf
        # byes: top 8 by score among the field
        in_field = np.where(field, score, -np.inf)
        order = np.argsort(-in_field, axis=1)[:, :8]
        bye = np.zeros_like(field)
        np.put_along_axis(bye, order, True, axis=1)
        return field, bye

    def __call__(self, wins, rating, conf_champ):
        return self.select(wins, rating, conf_champ)[0]

SELECTORS = {"cfp12": RulesSelector(12, 5)}  # cfp24 needs team->conference arrays; build in pipeline
