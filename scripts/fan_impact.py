"""How many fans does the 24-team format help vs hurt? Uses fanbase size only here, not in game meaning."""
import pandas as pd, numpy as np
from cfbmeaning import config as C

YEARS = [2021, 2022, 2023, 2024, 2025]
THR = 0.02  # a team is "better/worse off" if its stake per game moves by at least 2 points (0.02 of a playoff game)
gm = pd.concat([pd.read_csv(C.ROOT / "output" / f"game_meaning_{y}.csv") for y in YEARS])
brand = pd.read_csv(C.MANUAL / "brand_scores.csv").set_index("team").fanbase_millions
rows = []
for s in ("h", "a"):
    me = "home" if s == "h" else "away"
    t = gm[gm[me] != "FCS"]
    rows.append(pd.DataFrame(dict(season=t.season, team=t[me], s12=t[f"raw12_{s}"], s24=t[f"raw24_{s}"].where(~t.is_title))))  # title games exist only in the 12-team world
ts = pd.concat(rows).groupby(["season", "team"]).agg(s12=("s12", "mean"), s24=("s24", "mean"), games=("s12", "size")).reset_index()
ts["s12"] *= 100; ts["s24"] *= 100            # team stake per game on a 0-100 scale
ts["delta"] = ts.s24 - ts.s12
ts["published"] = ts.team.isin(brand.index)
ts["fans"] = ts.team.map(brand).fillna(C.DEFAULT_FANBASE_M)
ts["fans_x_delta"] = ts.fans * ts.delta


def summarize(d):
    tot = d.fans.sum()
    up, dn = d[d.delta >= THR * 100], d[d.delta <= -THR * 100]
    return pd.Series(dict(
        fans_total_M=tot, fans_better_M=up.fans.sum(), fans_worse_M=dn.fans.sum(),
        fans_flat_M=tot - up.fans.sum() - dn.fans.sum(),
        pct_better=up.fans.sum() / tot * 100, pct_worse=dn.fans.sum() / tot * 100,
        teams_better=len(up), teams_worse=len(dn), teams_total=len(d),
        fan_avg_stake_12=(d.fans * d.s12).sum() / tot, fan_avg_stake_24=(d.fans * d.s24).sum() / tot,
        team_avg_stake_12=d.s12.mean(), team_avg_stake_24=d.s24.mean()))


pd.set_option("display.width", 250, "display.max_columns", 30)
allf = ts.groupby("season").apply(summarize)
pub = ts[ts.published].groupby("season").apply(summarize)
print("== ALL FBS teams (G5 fanbases estimated at 0.2M) ==\n", allf.round(1).to_string())
print("== only teams with a published fanbase (top 65 + 3) ==\n", pub.round(1).to_string())
print("== 5-season average, all ==\n", allf.mean().round(1).to_string())
print("== 5-season average, published only ==\n", pub.mean().round(1).to_string())
allf.to_csv(C.ROOT / "output" / "fan_impact_by_season.csv")
# team-level pooled
pool = ts.groupby("team").agg(fans=("fans", "first"), seasons=("season", "nunique"), s12=("s12", "mean"), s24=("s24", "mean"),
                              delta=("delta", "mean")).reset_index()
pool["fan_delta"] = pool.fans * pool.delta
pool.to_csv(C.ROOT / "output" / "fan_impact_by_team.csv", index=False)
p4 = pool[pool.seasons >= 4]
print("== biggest fan-weighted gainers ==\n", p4.sort_values("fan_delta", ascending=False).head(15).round(1).to_string(index=False))
print("== biggest fan-weighted losers ==\n", p4.sort_values("fan_delta").head(15).round(1).to_string(index=False))
print("== top-15 brands ==\n", p4.sort_values("fans", ascending=False).head(15).round(1).to_string(index=False))
# by fanbase tier
ts["fan_tier"] = pd.cut(ts.fans, [0, 0.5, 1.5, 3, 20], labels=["<0.5M (mostly G5)", "0.5-1.5M", "1.5-3M", "3M+"])
print(ts.groupby("fan_tier").apply(lambda d: pd.Series(dict(teams=d.team.nunique(), s12=d.s12.mean(), s24=d.s24.mean(), delta=d.delta.mean(),
      share_up=(d.delta >= THR*100).mean()*100, share_down=(d.delta <= -THR*100).mean()*100, fans_M=d.groupby('season').fans.sum().mean()))).round(1))
