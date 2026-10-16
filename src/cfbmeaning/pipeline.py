"""End-to-end 2025 run: build games -> weekly frozen sims -> leverage -> playoff meaning.

Two "worlds" share the same regular-season outcomes each week:
  12-team world: conference championship games are played (champion = title game winner)
  24-team world: no conference championship games (champion = best conference record)
"""
from types import SimpleNamespace

import numpy as np
import pandas as pd
from . import config as C
from .meaning import audience_weights
from .selection import CFP24Selector, RulesSelector
from .winprob import elo_to_wp, spread_to_wp

P4 = {"Big Ten", "SEC", "Big 12", "ACC"}
FCS = "FCS"  # dummy team for any non-FBS opponent


def load(Y=C.SEASON):
    R = C.RAW
    return dict(
        reg=pd.read_parquet(R / f"games_regular_{Y}.parquet"),
        post=pd.read_parquet(R / f"games_postseason_{Y}.parquet"),
        lines=pd.read_parquet(R / f"lines_{Y}.parquet"),
        teams=pd.read_parquet(R / f"teams_fbs_{Y}.parquet"),
        sp=pd.read_parquet(R / f"sp_{Y}.parquet"),
        elo=pd.read_parquet(R / f"elo_{Y}.parquet"),
    )


def avg_spread(lines: pd.DataFrame) -> pd.Series:
    out = {}
    for gid, ls in zip(lines["id"], lines["lines"]):
        v = [d["spread"] for d in ls if d.get("spread") is not None]
        if v:
            out[gid] = float(np.mean(v))
    return pd.Series(out, name="spread")


def find_titles(reg, teams_df):
    """Title game = last same-conference FBS game in conferences with 8+ members, limited to
    the week most conferences hold theirs (avoids late games like Army-Navy)."""
    size = teams_df.conference.value_counts()
    same = reg[(reg.homeClassification == "fbs") & (reg.awayClassification == "fbs") &
               (reg.homeConference == reg.awayConference) & (reg.week >= 13)]
    same = same[same.homeConference.map(lambda c: size.get(c, 0) >= 8 and c != "FBS Independents")]
    first = same.groupby("homeConference").apply(lambda g: g.sort_values("startDate").iloc[-1].week)
    tw = first.mode().max()
    ids = []
    for _, g in same[same.week <= tw].groupby("homeConference"):
        g = g[g.week == g.week.max()]
        ids.append(g.sort_values(["neutralSite", "startDate"]).iloc[-1]["id"])
    return ids


def build_games(d):
    teams = sorted(d["teams"]["school"])
    tidx = {t: i for i, t in enumerate(teams)}
    tidx[FCS] = len(teams)
    reg = d["reg"].copy()
    reg = reg[(reg.homeClassification == "fbs") | (reg.awayClassification == "fbs")].copy()
    reg["home"] = np.where(reg.homeClassification == "fbs", reg.homeTeam, FCS)
    reg["away"] = np.where(reg.awayClassification == "fbs", reg.awayTeam, FCS)
    reg["spread"] = reg["id"].map(avg_spread(d["lines"]))
    hfa = np.where(reg.neutralSite, 0, 55)
    tel = d["elo"].set_index("team")["elo"]  # current-season Elo: fills in games without a pre-game Elo (unplayed games)
    hpre = reg.homePregameElo.fillna(reg.home.map(tel)).fillna(1500)
    apre = reg.awayPregameElo.fillna(reg.away.map(tel)).fillna(1500)
    p_elo = elo_to_wp(hpre, apre, home_field=hfa)
    p = np.where(reg.spread.notna(), spread_to_wp(reg.spread.fillna(0)), p_elo)
    p = np.where(reg.away == FCS, 0.97, np.where(reg.home == FCS, 0.03, p))
    reg["p_home"] = p
    reg["home_won"] = reg.homePoints > reg.awayPoints
    complete = reg.completed.mean() >= 0.95  # in-progress seasons have no title games scheduled yet
    reg["is_title"] = reg["id"].isin(find_titles(reg, d["teams"])) if complete else False
    reg["h"] = reg.home.map(tidx)
    reg["a"] = reg.away.map(tidx)
    return teams, tidx, reg.reset_index(drop=True)


def rivalry_lookup():
    r = pd.read_csv(C.MANUAL / "rivalries.csv")
    return {frozenset((a, b)): x for a, b, x in zip(r.team_a, r.team_b, r.boost)}


def elo_now(reg, teams, w, elo_tbl=None):
    """Each team's Elo as of the start of week w (pre-game Elo of its next game).
    For an in-progress season pass elo_tbl (current Elo by team) and it is used for every week."""
    if elo_tbl is not None:
        e = elo_tbl.reindex(teams)
        return e.fillna(e.mean()).to_numpy(float)
    rows = []
    for side in ("home", "away"):
        rows.append(pd.DataFrame({"team": reg[side].where(reg[side] != FCS), "week": reg.week,
                                  "pre": reg[f"{side}PregameElo"], "post": reg[f"{side}PostgameElo"]}))
    tl = pd.concat(rows).dropna(subset=["team"]).sort_values("week")
    nxt = tl[tl.week >= w].groupby("team")["pre"].first()
    last = tl.groupby("team")["post"].last()
    e = nxt.reindex(teams).fillna(last.reindex(teams))
    return e.fillna(e.mean()).to_numpy(float)


def z(x):
    return (x - x.mean()) / x.std()


def run(season=C.SEASON, n_sims=C.N_SIMS, resume_weight=C.RESUME_WEIGHT, verbose=True):
    d = load(season)
    teams, tidx, reg = build_games(d)
    n, T = len(teams), len(teams) + 1
    conf = d["teams"].set_index("school").loc[teams, "conference"].to_numpy()
    conf_names = sorted(set(conf))
    conf_id = np.array([conf_names.index(c) for c in conf])
    p4 = set(P4) | ({"Pac-12"} if season <= 2023 else set())  # the Pac-12 counted as Power only through 2023
    is_p4 = np.array([c in p4 for c in conf])
    sp = d["sp"].set_index("team")["rating"].reindex(teams)
    z_sp = z(sp.fillna(sp.mean()).to_numpy(float))
    wts, dflt = audience_weights()
    w_team = np.array([wts.get(t, dflt) for t in teams] + [0.0])
    riv = rivalry_lookup()

    sel12 = RulesSelector(12, 5, resume_weight)
    sel24 = CFP24Selector(is_p4, conf_id, resume_weight)

    games = reg[~reg.is_title].reset_index(drop=True)
    titles = {r.homeConference: r for r in reg[reg.is_title].itertuples()}
    incomplete = reg.completed.mean() < 0.95
    elo_tbl = d["elo"].set_index("team")["elo"] if incomplete else None
    if incomplete:
        # no title games are scheduled yet: assume one per conference with 10+ teams (champion = winner of a
        # simulated game between the top two); the Pac-12 (8 teams) is decided by record
        size = d["teams"].conference.value_counts()
        titles = {c: SimpleNamespace(week=99, h=-1, a=-1, p_home=0.5, home_won=False)
                  for c in size.index if size[c] >= 10 and c != "FBS Independents"}
    G = len(games)
    Hm = np.zeros((G, T), np.float32)
    Am = np.zeros((G, T), np.float32)
    Hm[np.arange(G), games.h] = 1
    Am[np.arange(G), games.a] = 1
    cmask = games.conferenceGame.to_numpy(bool)[:, None].astype(np.float32)
    conf_games = (Hm * cmask).sum(0) + (Am * cmask).sum(0)
    members = {c: np.where(conf == c)[0] for c in titles}
    conf_members = {c: np.where(conf == c)[0] for c in conf_names}

    def state(w, seed, now=False):
        rng = np.random.default_rng(seed + w)  # same seed every season is fine
        S = n_sims
        o = rng.random((S, G)) < games.p_home.to_numpy()
        done = games.completed.to_numpy(bool)
        lock = done if now else ((games.week < w).to_numpy() & done)
        o[:, lock] = games.home_won.to_numpy(bool)[lock]
        of = o.astype(np.float32)
        wins = of @ Hm + (1 - of) @ Am
        cwins = (of * cmask.T) @ Hm + ((1 - of) * cmask.T) @ Am
        cpct = cwins / np.maximum(conf_games, 1)
        elo = elo_now(reg, teams, w, elo_tbl)
        rating = 0.5 * z(elo) + 0.5 * z_sp
        rows = np.arange(S)

        # Resume: each win is worth more against a strong opponent, each loss costs more against a weak one
        # (opponent strength = the rating z-score, clipped); FCS win = 0.2, FCS loss = -2.0.
        s_opp = np.clip(np.append(rating, np.nan), -1.5, 2.5)
        so_h, so_a = s_opp[games.a.to_numpy()], s_opp[games.h.to_numpy()]  # opponent of the home / away team
        fcs_h, fcs_a = np.isnan(so_h), np.isnan(so_a)
        cr_h = np.where(fcs_h, 0.2, 1 + C.RESUME_OPP * np.nan_to_num(so_h)); db_h = np.where(fcs_h, 2.0, 1 - C.RESUME_OPP * np.nan_to_num(so_h))
        cr_a = np.where(fcs_a, 0.2, 1 + C.RESUME_OPP * np.nan_to_num(so_a)); db_a = np.where(fcs_a, 2.0, 1 - C.RESUME_OPP * np.nan_to_num(so_a))
        resume = (of @ (Hm * cr_h[:, None].astype(np.float32)) + (1 - of) @ (Am * cr_a[:, None].astype(np.float32))
                  - of @ (Am * db_a[:, None].astype(np.float32)) - (1 - of) @ (Hm * db_h[:, None].astype(np.float32)))

        # 24-team world: no title games, champion = best conference record (random tiebreak)
        wins24 = wins.copy()
        res24 = resume.copy()
        champ24 = np.zeros((S, T), bool)
        # 12-team world: title games between top two in the standings
        wins12 = wins.copy()
        res12 = resume.copy()
        champ12 = np.zeros((S, T), bool)
        tout = {}
        for c, m in conf_members.items():
            if c == "FBS Independents" or (c not in titles and len(m) < 6):
                continue  # no champion modeled
            key = cpct[:, m] + 0.02 * rng.random((S, len(m))) + 0.002 * rating[m]
            order = np.argsort(-key, axis=1)
            champ24[rows, m[order[:, 0]]] = True
            if c not in titles:
                champ12[rows, m[order[:, 0]]] = True
                continue
            t = titles[c]
            if w >= t.week:
                A, B, pA = np.full(S, t.h), np.full(S, t.a), np.full(S, t.p_home)
            else:
                A, B = m[order[:, 0]], m[order[:, 1]]
                pA = elo_to_wp(elo[A], elo[B], home_field=0)
            aw = rng.random(S) < pA
            if w > t.week:
                aw[:] = bool(t.home_won)
            win = np.where(aw, A, B)
            lose = np.where(aw, B, A)
            wins12[rows, win] += 1
            res12[rows, win] += 1.0   # title game: +1 for the winner, -1 for the loser
            res12[rows, lose] -= 1.0
            champ12[rows, win] = True
            if w == t.week:
                tout[c] = aw
        return o, tout, rating, (res12, champ12, wins12), (res24, champ24, wins24)

    def selection(rating, w12, w24):
        f12, b12 = sel12.select(w12[0][:, :n], rating, w12[1][:, :n])
        f24, b24 = sel24.select(w24[0][:, :n], rating, w24[1][:, :n])
        pad = lambda x: np.concatenate([x, np.zeros((x.shape[0], 1), bool)], axis=1)
        return pad(f12), pad(b12), pad(f24), pad(b24)

    def lev(ind, won):
        k = int(won.sum())
        if k < 10 or len(won) - k < 10:
            return 0.0
        return abs(ind[won].mean() - ind[~won].mean())

    out = []
    weeks = sorted(reg.week.unique())
    if incomplete:
        share = games.groupby("week").completed.mean()
        current_week = int(share[share < 0.5].index.min())
        weeks = [w for w in weeks if w < current_week]
    for w in weeks:
        o, tout, rating, w12, w24 = state(w, C.SEED)
        sel = selection(rating, w12, w24)
        wkg = games[games.week == w]
        for i, r in zip(wkg.index, wkg.itertuples()):
            out.append(_row(r, o[:, i], sel, w12[1], w24[1], riv, w_team, lev))
        for c, t in titles.items():
            if t.week == w:
                out.append(_row(t, tout[c], sel, w12[1], w24[1], riv, w_team, lev))
        if verbose:
            print(f"week {w}: {len(wkg)} games + {sum(t.week == w for t in titles.values())} title games done")
    gm = pd.DataFrame(out)

    if incomplete:  # snapshot of the season right now: team odds + the scores of the next few weeks of games
        o, tout, rating, w12, w24 = state(current_week, C.SEED, now=True)
        f12, b12, f24, b24 = selection(rating, w12, w24)
        rec = {t: [0, 0] for t in teams}
        for h, a, hw, dn in zip(games.home, games.away, games.home_won, games.completed):
            if dn:
                if h in rec: rec[h][0 if hw else 1] += 1
                if a in rec: rec[a][1 if hw else 0] += 1
        snap = pd.DataFrame(dict(team=teams, conf=conf, wins=[rec[t][0] for t in teams], losses=[rec[t][1] for t in teams],
                                 rating=rating, cfp12=f12[:, :n].mean(0), cfp24=f24[:, :n].mean(0),
                                 bye12=b12[:, :n].mean(0), bye24=b24[:, :n].mean(0),
                                 champ12=w12[1][:, :n].mean(0), champ24=w24[1][:, :n].mean(0)))
        up = games[(~games.completed) & (games.week >= current_week) & (games.week <= current_week + 2)]
        urows = [_row(r, o[:, i], (f12, b12, f24, b24), w12[1], w24[1], riv, w_team, lev)
                 for i, r in zip(up.index, up.itertuples())]
        return dict(games=gm, snapshot=snap, upcoming=pd.DataFrame(urows), current_week=current_week, teams=teams)

    # final state (everything locked): fields for sanity check and bracket sims
    o, tout, rating, w12, w24 = state(99, C.SEED)
    sel = selection(rating, w12, w24)
    sc12 = rating + resume_weight * w12[0][0, :n]
    sc24 = rating + resume_weight * w24[0][0, :n]
    seeds12 = sorted(np.where(sel[0][0, :n])[0], key=lambda i: -sc12[i])
    seeds24 = sorted(np.where(sel[2][0, :n])[0], key=lambda i: -sc24[i])
    champs24 = [teams[i] for i in np.where(w24[1][0, :n])[0]]
    return dict(games=gm, teams=teams, w_team=w_team, seeds12=seeds12, seeds24=seeds24,
                elo=elo_now(reg, teams, 99), post=d["post"], tidx=tidx, champs24=champs24,
                rating=rating, wins12=w12[2][0, :n], wins24=w24[2][0, :n], resume12=w12[0][0, :n], resume24=w24[0][0, :n],
                resume_weight=resume_weight)


def _row(r, outcome, sel, champ12, champ24, riv, w_team, lev):
    f12, b12, f24, b24 = sel
    h, a = r.h, r.a
    title = bool(r.is_title)
    rec = dict(id=r.id, week=r.week, home=r.home, away=r.away, is_title=title,
               rivalry=riv.get(frozenset((r.home, r.away)), 0.0), wh=w_team[h], wa=w_team[a])
    keys = ("cfp12", "cfp24", "conf12", "conf24", "bye12", "bye24")
    for side, idx, won in (("h", h, outcome), ("a", a, ~outcome)):
        if idx >= len(w_team) - 1:  # FCS dummy
            for k in keys:
                rec[f"{k}_{side}"] = 0.0
            continue
        # playoff odds if this team wins / loses the game (useful for sanity checks)
        for k, ind in (("cfp12", f12), ("cfp24", f24)):
            nw = int(won.sum())
            rec[f"{k}_pwin_{side}"] = ind[won, idx].mean() if nw else np.nan
            rec[f"{k}_ploss_{side}"] = ind[~won, idx].mean() if nw < len(won) else np.nan
        rec[f"cfp12_{side}"] = lev(f12[:, idx], won)
        rec[f"conf12_{side}"] = lev(champ12[:, idx], won)
        rec[f"bye12_{side}"] = lev(b12[:, idx], won)
        # title games do not exist in the 24-team world
        for k, ind in (("cfp24", f24), ("conf24", champ24), ("bye24", b24)):
            rec[f"{k}_{side}"] = 0.0 if title else lev(ind[:, idx], won)
    return rec


def combine(gm: pd.DataFrame):
    """Add raw and audience-weighted meaning per game for each format."""
    gm = gm.copy()
    for fmt in ("12", "24"):
        absent = gm.is_title if fmt == "24" else pd.Series(False, index=gm.index)
        for s in ("h", "a"):
            fcs_side = gm["home" if s == "h" else "away"] == FCS
            raw = (C.W_CFP * gm[f"cfp{fmt}_{s}"] + C.W_CONF * gm[f"conf{fmt}_{s}"]
                   + C.W_BYE * gm[f"bye{fmt}_{s}"] + gm.rivalry)
            gm[f"raw{fmt}_{s}"] = np.where(fcs_side | absent, 0.0, raw)
        gm[f"unw{fmt}"] = gm[f"raw{fmt}_h"] + gm[f"raw{fmt}_a"]
        wh = gm.wh if C.USE_AUDIENCE_WEIGHTS else 1.0
        wa = gm.wa if C.USE_AUDIENCE_WEIGHTS else 1.0
        gm[f"meaning{fmt}"] = gm[f"raw{fmt}_h"] * wh + gm[f"raw{fmt}_a"] * wa
        gm[f"score{fmt}_uncapped"] = 100 * gm[f"meaning{fmt}"] / C.SCORE_REF
        gm[f"score{fmt}"] = gm[f"score{fmt}_uncapped"].clip(upper=100)
    return gm


def sim_bracket(seeds, fmt, elo, w_team, n_sims, seed=7, power=None, any_power=False):
    """Expected playoff meaning (flat PLAYOFF_GAME_MEANING per team x audience weight)."""
    rng = np.random.default_rng(seed)
    S = n_sims
    total = np.zeros(S)
    score = np.zeros(S)
    per_game = []
    pcount = np.zeros(S)  # games with both (or, if any_power, at least one) team in `power` (bool array over teams)
    games = 0
    s = [np.full(S, i) for i in seeds]

    def play(a, b):
        nonlocal games
        games += 1
        m = C.PLAYOFF_GAME_MEANING * (w_team[a] + w_team[b])
        total[:] += m
        per_game.append(m)
        if power is not None:
            pcount[:] += (power[a] | power[b]) if any_power else (power[a] & power[b])
        score[:] += np.minimum(100.0, 100 * m / C.SCORE_REF)
        p = elo_to_wp(elo[a], elo[b], home_field=0)
        return np.where(rng.random(S) < p, a, b)

    if fmt == "12":
        w89, w512, w710, w611 = play(s[7], s[8]), play(s[4], s[11]), play(s[6], s[9]), play(s[5], s[10])
        q1, q4, q2, q3 = play(s[0], w89), play(s[3], w512), play(s[1], w710), play(s[2], w611)
    else:
        pairs = [(9, 24), (10, 23), (11, 22), (12, 21), (13, 20), (14, 19), (15, 18), (16, 17)]
        r1w = [play(s[a - 1], s[b - 1]) for a, b in pairs]
        face = {1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1, 8: 0}  # bye seed -> R1 winner it meets
        r2 = [play(s[k - 1], r1w[face[k]]) for k in range(1, 9)]
        q1 = play(r2[0], r2[7])
        q4 = play(r2[3], r2[4])
        q2 = play(r2[1], r2[6])
        q3 = play(r2[2], r2[5])
    sf1, sf2 = play(q1, q4), play(q2, q3)
    play(sf1, sf2)
    sim_bracket.last_games = np.concatenate(per_game)  # every simulated playoff game's meaning
    sim_bracket.power_games = pcount.mean()
    return total.mean(), games, score.mean()
