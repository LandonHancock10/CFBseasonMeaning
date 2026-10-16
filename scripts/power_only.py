"""Rerun the comparison for Power teams only: Big Ten, SEC, Big 12, ACC, Pac-12 (2021-23, when it had 12 teams)
and Notre Dame. A game counts if AT LEAST ONE team is a Power team (includes games vs Group of 5 and FCS opponents). The simulation itself is unchanged (Group of 5
teams still compete for playoff spots); only the reporting is filtered."""
import numpy as np, pandas as pd
from cfbmeaning import config as C, pipeline as P

YEARS = [2021, 2022, 2023, 2024, 2025]
THR = 2.0
brand = pd.read_csv(C.MANUAL / "brand_scores.csv").set_index("team").fanbase_millions
out = C.ROOT / "output"
summ, team_rows = [], []
for Y in YEARS:
    res = P.run(Y, verbose=False)
    tf = pd.read_parquet(C.RAW / f"teams_fbs_{Y}.parquet").set_index("school").conference
    power_confs = {"Big Ten", "SEC", "Big 12", "ACC"} | ({"Pac-12"} if (tf == "Pac-12").sum() >= 8 else set())
    power_set = {t for t, c in tf.items() if c in power_confs} | {"Notre Dame"}
    teams = res["teams"]
    pmask = np.array([t in power_set for t in teams] + [False])
    gm = P.combine(res["games"]); gm.insert(0, "season", Y)
    gp = gm[gm.home.isin(power_set) | gm.away.isin(power_set)]
    g24 = gp[~gp.is_title]
    pm12, ng12, sc12 = P.sim_bracket(res["seeds12"], "12", res["elo"], np.ones_like(res["w_team"]), C.N_SIMS, power=pmask, any_power=True); pg12 = P.sim_bracket.power_games
    pm24, ng24, sc24 = P.sim_bracket(res["seeds24"], "24", res["elo"], np.ones_like(res["w_team"]), C.N_SIMS, power=pmask, any_power=True); pg24 = P.sim_bracket.power_games
    for fmt, d, pg in (("12-team", gp, pg12), ("24-team", g24, pg24)):
        k = fmt[:2]; x = d[f"score{k}"]
        summ.append(dict(season=Y, format=fmt, power_teams=len(power_set & set(teams)), games=len(d), avg=x.mean(), median=x.median(),
                         under5_pct=(x < 5).mean() * 100, games_25plus=int((x >= 25).sum()), games_50plus=int((x >= 50).sum()),
                         playoff_games_any_power=pg, avg_with_playoffs=(x.sum() + 100 * pg) / (len(d) + pg),
                         season_total=x.sum() + 100 * pg))
    # team-level (all games of each Power team; title games count in the 12-team format only)
    for s_, me in (("h", "home"), ("a", "away")):
        t = gm[gm[me].isin(power_set)]
        team_rows.append(pd.DataFrame(dict(season=Y, team=t[me], conf=t[me].map(tf), s12=t[f"raw12_{s_}"] * 100,
                                           s24=(t[f"raw24_{s_}"] * 100).where(~t.is_title))))
S = pd.DataFrame(summ); S.to_csv(out / "power_only_summary.csv", index=False)
pd.set_option("display.width", 250, "display.max_columns", 30)
print(S.round(1).to_string(index=False)); print(S.groupby("format").mean(numeric_only=True).drop(columns="season").round(1).T)
ts = pd.concat(team_rows).groupby(["season", "team"]).agg(conf=("conf", "first"), s12=("s12", "mean"), s24=("s24", "mean")).reset_index()
ts["delta"] = ts.s24 - ts.s12
ts["fans"] = ts.team.map(brand).fillna(C.DEFAULT_FANBASE_M)
def fan(d):
    tot = d.fans.sum(); up = d[d.delta >= THR]; dn = d[d.delta <= -THR]
    return pd.Series(dict(teams=len(d), fans_M=tot, better_M=up.fans.sum(), worse_M=dn.fans.sum(), flat_M=tot - up.fans.sum() - dn.fans.sum(),
                          pct_better=up.fans.sum() / tot * 100, pct_worse=dn.fans.sum() / tot * 100, teams_better=len(up), teams_worse=len(dn),
                          fan_avg_12=(d.fans * d.s12).sum() / tot, fan_avg_24=(d.fans * d.s24).sum() / tot))
F = ts.groupby("season").apply(fan); F.to_csv(out / "power_only_fan_impact.csv")
print(F.round(1).to_string()); print(F.mean().round(1).to_string())
pool = ts.groupby("team").agg(conf=("conf", "first"), n=("season", "nunique"), fans=("fans", "first"), s12=("s12", "mean"), s24=("s24", "mean")).reset_index()
pool["delta"] = pool.s24 - pool.s12; pool["fan_delta"] = pool.fans * pool.delta
pool = pool[pool.n >= 4]; pool.to_csv(out / "power_only_by_team.csv", index=False)
print("gainers\n", pool.sort_values("delta", ascending=False).head(12).round(1).to_string(index=False))
print("losers\n", pool.sort_values("delta").head(14).round(1).to_string(index=False))
print("by conf\n", ts.groupby("conf").agg(s12=("s12", "mean"), s24=("s24", "mean"), delta=("delta", "mean")).round(1))
print("share of Power teams up/down/flat:", (ts.delta >= THR).mean().round(3), (ts.delta <= -THR).mean().round(3))
