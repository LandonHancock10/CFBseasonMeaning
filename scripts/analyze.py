"""Team- and matchup-level comparison of the two formats across seasons."""
import pandas as pd, numpy as np
from cfbmeaning import config as C

YEARS = [2021, 2022, 2023, 2024, 2025]
gm = pd.concat([pd.read_csv(C.ROOT / "output" / f"game_meaning_{y}.csv") for y in YEARS])
FCS = "FCS"
# long format, one row per team-game, excluding title games (they only exist in the 12-team world)
rows = []
for s, opp in (("h", "away"), ("a", "home")):
    me = "home" if s == "h" else "away"
    t = gm[gm[me] != FCS]
    rows.append(pd.DataFrame(dict(season=t.season, team=t[me], opp=t[opp], week=t.week,
        raw12=t[f"raw12_{s}"], raw24=t[f"raw24_{s}"], cfp12=t[f"cfp12_{s}"], cfp24=t[f"cfp24_{s}"],
        conf12=t[f"conf12_{s}"], conf24=t[f"conf24_{s}"], bye12=t[f"bye12_{s}"], bye24=t[f"bye24_{s}"],
        m12=t.score12, m24=t.score24, is_title=t.is_title)))
tg = pd.concat(rows)
tg["raw24_x"] = tg.raw24.where(~tg.is_title)  # no title game in the 24-team world
ts = tg.groupby(["season", "team"]).agg(raw12=("raw12", "mean"), raw24=("raw24_x", "mean"), n=("raw12", "size")).reset_index()
ts["delta"] = ts.raw24 - ts.raw12

# conference + elo tier
elo = {}
for y in YEARS:
    g = pd.read_parquet(C.RAW / f"elo_{y}.parquet")
    conf = pd.read_parquet(C.RAW / f"teams_fbs_{y}.parquet").set_index("school").conference
    for tm, e in zip(g.team, g.elo):
        elo[(y, tm)] = (e, conf.get(tm))
ts["elo"] = [elo.get((y, t), (np.nan, None))[0] for y, t in zip(ts.season, ts.team)]
ts["conf"] = [elo.get((y, t), (np.nan, None))[1] for y, t in zip(ts.season, ts.team)]
ts["tier"] = ts.groupby("season").elo.transform(lambda x: pd.cut(x.rank(ascending=False), [0, 12, 30, 65, 200],
                                                                  labels=["Top 12", "13-30", "31-65", "66+"]))
pd.set_option("display.width", 250, "display.max_rows", 300)
print("== by season x tier (own-stake per game, unweighted) ==")
print(ts.groupby(["tier"]).agg(raw12=("raw12", "mean"), raw24=("raw24", "mean"), delta=("delta", "mean")).round(4))
print(ts.groupby(["season", "tier"]).delta.mean().unstack().round(4))
ts["grp"] = ts.conf.map(lambda c: c if c in ("SEC", "Big Ten", "Big 12", "ACC", "Pac-12") else
                        ("Independent" if c == "FBS Independents" else "Group of 5"))
print("== by conference group ==")
print(ts.groupby("grp").agg(raw12=("raw12", "mean"), raw24=("raw24", "mean"), delta=("delta", "mean")).round(4))
print(ts.groupby(["season", "grp"]).delta.mean().unstack().round(4))
ts.to_csv(C.ROOT / "output" / "team_season_meaning.csv", index=False)

pool = ts.groupby("team").agg(n_seasons=("season", "nunique"), raw12=("raw12", "mean"), raw24=("raw24", "mean"),
                              delta=("delta", "mean"), elo=("elo", "mean")).reset_index()
pool = pool[pool.n_seasons >= 4]
pool["pct"] = pool.delta / pool.raw12
pool.to_csv(C.ROOT / "output" / "team_pooled_meaning.csv", index=False)
print("== biggest boosts (pooled) ==\n", pool.sort_values("delta", ascending=False).head(25).round(3).to_string(index=False))
print("== biggest drops (pooled) ==\n", pool.sort_values("delta").head(25).round(3).to_string(index=False))
print(len(pool), (pool.delta > 0).sum(), "teams up")
print("== 2025 boosts ==\n", ts[ts.season == 2025].sort_values("delta", ascending=False).head(12).round(3).to_string(index=False))
print("== 2025 drops ==\n", ts[ts.season == 2025].sort_values("delta").head(12).round(3).to_string(index=False))

# matchups: weighted meaning difference, ordinary games only
m = gm[~gm.is_title].copy()
m["d_w"] = m.score24 - m.score12
m["d_u"] = m.unw24 - m.unw12
cols = ["season", "week", "home", "away", "score12", "score24", "unw12", "unw24"]
print("== games gaining most under 24 (weighted), all years ==\n", m.sort_values("d_w", ascending=False).head(25)[cols].round(3).to_string(index=False))
print("== games losing most under 24 (weighted), all years ==\n", m.sort_values("d_w").head(25)[cols].round(3).to_string(index=False))
print("== 2025 gain ==\n", m[m.season == 2025].sort_values("d_w", ascending=False).head(12)[cols].round(3).to_string(index=False))
print("== 2025 lose ==\n", m[m.season == 2025].sort_values("d_w").head(12)[cols].round(3).to_string(index=False))
t = gm[gm.is_title]
print("== title games (12-team meaning) ==\n", t.sort_values("score12", ascending=False).head(15)[["season", "home", "away", "score12", "unw12"]].round(3).to_string(index=False))
print("title game total/avg meaning by season:\n", t.groupby("season").score12.agg(["sum", "mean"]).round(3))
print("top games per format overall")
for k in ("12", "24"):
    print(k, gm.sort_values(f"meaning{k}", ascending=False).head(10)[["season", "week", "home", "away", f"meaning{k}"]].round(3).to_string(index=False))
# distribution: share of games with near-zero meaning
for k in ("12", "24"):
    x = gm[(~gm.is_title)][f"unw{k}"]
    print(k, "share of games with unweighted meaning < 0.05:", round((x < .05).mean(), 3), " > 0.5:", round((x > .5).mean(), 4))
# component breakdown
comp = pd.DataFrame({k: [tg[f"{k}12"].mean(), tg[f"{k}24"].mean()] for k in ("cfp", "conf", "bye")}, index=["12", "24"])
print(comp.round(4))
