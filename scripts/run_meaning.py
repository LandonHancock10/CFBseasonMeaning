"""Run the meaning analysis for 12-team vs 24-team playoffs. Usage: python scripts/run_meaning.py [year ...]"""
import sys
import numpy as np
import pandas as pd
from cfbmeaning import config as C, pipeline as P

years = [int(a) for a in sys.argv[1:]] or [C.SEASON]
out_dir = C.ROOT / "output"
out_dir.mkdir(exist_ok=True)
pd.set_option("display.width", 250, "display.max_columns", 30)
summ = []
for Y in years:
    res = P.run(Y, verbose=False)
    gm = P.combine(res["games"])
    gm.insert(0, "season", Y)
    teams, elo = res["teams"], res["elo"]
    w = res["w_team"] if C.USE_AUDIENCE_WEIGHTS else np.ones_like(res["w_team"])
    gm.to_csv(out_dir / f"game_meaning_{Y}.csv", index=False)
    cfp = res["post"][res["post"].get("playoff.competition", pd.Series(dtype=object)) == "cfp"] \
        if "playoff.competition" in res["post"] else res["post"].iloc[0:0]
    actual = set(cfp.homeTeam) | set(cfp.awayTeam)
    model12 = {teams[i] for i in res["seeds12"]}
    S = C.N_SIMS
    pm12, g12, sc12 = P.sim_bracket(res["seeds12"], "12", elo, w, S)
    pm24, g24, sc24 = P.sim_bracket(res["seeds24"], "24", elo, w, S)
    n12, n24 = len(gm), int((~gm.is_title).sum())
    for label, k, nreg, pm, ng, psc in (("12-team", "12", n12, pm12, g12, sc12), ("24-team", "24", n24, pm24, g24, sc24)):
        reg = gm[f"meaning{k}"].sum()
        rg = gm if k == "12" else gm[~gm.is_title]
        rs = rg[f"score{k}"]
        summ.append(dict(season=Y, format=label, reg_games=nreg, reg_meaning=reg, reg_per_game=reg / nreg,
                         playoff_games=ng, playoff_meaning=pm, total=reg + pm,
                         all_per_game=(reg + pm) / (nreg + ng), reg_unweighted=gm[f"unw{k}"].sum(),
                         reg_unw_per_game=gm[f"unw{k}"].sum() / nreg,
                         title_games=int(gm.is_title.sum()) if k == "12" else 0,
                         reg_avg_score=rs.mean(), playoff_avg_score=psc / ng,
                         all_avg_score=(rs.sum() + psc) / (nreg + ng), reg_score_sum=rs.sum(),
                         season_score_total=rs.sum() + psc,
                         games_25plus=int((rs >= 25).sum()), games_50plus=int((rs >= 50).sum()),
                         games_under_5=int((rs < 5).sum()), top100_avg_score=rs.nlargest(100).mean(), capped_games=int((rg[f"score{k}_uncapped"] > 100).sum())))
    print(Y, "12-team field overlap with actual CFP:" , len(actual & model12) if len(cfp) > 4 else "n/a (4-team era)")
    print("  modeled 12:", sorted(model12))
    print("  modeled 24 champs (no title game):", sorted(res["champs24"]))
summary = pd.DataFrame(summ)
summary.to_csv(out_dir / "summary_all_years.csv", index=False)
print(summary.round(3).to_string(index=False))
