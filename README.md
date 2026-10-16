# CFB Season Meaning

Assigns a "meaning" score to every college football game (leverage on CFP odds,
conference title odds, rivalries, weighted by audience size), then compares the
2025 season under a 12-team vs 24-team playoff.

## Method
meaning(team, game) = w_cfp*dP(CFP) + w_conf*dP(conf title) + rivalry_flat
game meaning = sum over both teams of meaning * audience_weight(team)
dP = |P(outcome | team wins) - P(outcome | team loses)|, from Monte Carlo of the
remaining season, frozen at the start of each week. Playoff games = 1.0 per team.

## Setup
    python -m pip install -r requirements.txt
    python -m pip install -e .
    # .env must contain CFB_DATA_KEY=<collegefootballdata.com key>
    python scripts/pull_data.py          # writes data/raw/*.parquet

## Layout
- src/cfbmeaning/config.py     season + paths + selection settings
- src/cfbmeaning/cfbd.py       API client (Bearer auth, caching)
- src/cfbmeaning/winprob.py    spread / Elo -> win probability
- src/cfbmeaning/sim.py        weekly-frozen Monte Carlo
- src/cfbmeaning/selection.py  pluggable playoff selection (12 / 24 team)
- src/cfbmeaning/meaning.py    leverage + weights
- data/manual/                 hand-curated rivalries and brand scores

## Data sources and notes

### Fanbase size (data/manual/brand_scores.csv)
- Source: "Altimore College & Co." fanbase study (regional census patterns, digital
  engagement, alumni footprint). Top 65 FBS programs only; figures were pasted from
  an AI chat summary that cites 247Sports ("the 16 biggest fan bases", Ohio State at
  11.26M), On3 and Sports Media Watch. Obtained 2026-10-16.
- CAVEAT: I could not verify this study independently. Check the original (247Sports
  article) before putting numbers on camera.
- Gaps and judgement calls:
  - Teams ranked 66+ were not published. Group of Five teams get DEFAULT_FANBASE_M
    = 0.2M (midpoint of the stated 50k to 350k range). Boise State, UCF and South
    Florida are set to 0.95M ("right on the edge of 1 million"). Both are estimates.
  - TCU appears twice (rank 48 at 1.18M, rank 56 at 0.95M); the file uses 1.18M.
  - Oregon State and Washington State are labeled "Pac-12 / Ind." in the source.
  - Source notes Georgia's live TV audience is far higher than its fanbase rank
    (6.372M for the Alabama game per On3, Oct 15 2026). Consider blending viewership later.
- Audience weight = (fanbase / 11.26M) ** AUDIENCE_EXP (config.py).

### Bye stakes
Meaning includes W_BYE * |P(bye | win) - P(bye | loss)| in both formats.
12-team: top 4 ranked teams get byes (2025 rules). 24-team: top 8 get byes.

### Rivalries (data/manual/rivalries.csv)
Hand-curated by Claude from general college football knowledge (no external dataset),
about 65 pairs. The boost is a flat per-team add to meaning: 0.12 to 0.15 for the
biggest games, 0.08 to 0.10 for major rivalries, 0.03 to 0.06 for minor ones.
The values are judgement calls, so prune and adjust before filming. Team names follow
CFBD spelling and should be checked against the pulled teams file.

### Fanbase methodology (as described in the source chat, unverified)
Metrics said to be used to build the fanbase rankings:
- Nielsen TV ratings and share: total active audience, from marquee games (the source
  cites Texas vs. Ohio State at 13.99 million viewers) down to regional broadcasts on
  ESPN, FOX and CBS.
- Google Trends and search volume: baseline daily search interest nationwide,
  especially outside a team's home state.
- Social media follower counts: aggregated Instagram, TikTok and X followers, as a
  measure of younger demographics and digital footprint.
- Learfield and fanbase marketing databases: consumer datasets of verified fan
  profiles (licensed apparel, ticket purchases, newsletter subscriptions).
- Local census and ZIP code maps: regional census data cross-referenced with
  geo-targeted data (localized Facebook likes, sports betting data) to map where one
  school's territory ends and another's begins.
- Alumni registry records: official university registries of living graduates and
  where they live.
Source: AI chat summary pasted 2026-10-16. Same verification caveat as above.

## Running the analysis
    python scripts/pull_data.py      # once; needs CFB_DATA_KEY in .env
    python scripts/run_meaning.py    # ~5 seconds; writes output/game_meaning_2025.csv and summary_2025.csv
Code: src/cfbmeaning/pipeline.py (sims + leverage + brackets), scripts/run_meaning.py (summary).

### Modeling choices
- Win probability: average spread across providers, normal approximation (SD 13.5);
  pre-game Elo where no line; 97% for FBS vs FCS.
- Each week is frozen: earlier results are actual, later games are sampled (10k sims).
  Leverage = |P(outcome | team wins) - P(outcome | team loses)|; games with fewer than
  10 sims on one side get 0.
- Ratings for selection: 50/50 blend of z-scored Elo (as of that week) and final-season SP+
  (SP+ is hindsight, only available as a season-end number). Score = rating + 0.5 * wins.
- 12-team world: conference title games are played (top two in the standings meet,
  title game winner is champion); top 5 champions get auto-bids; top 4 ranked get byes.
- 24-team world: NO conference title games (per the format change), so the 9 title games
  have zero meaning and the champion is the best conference record (random tiebreak).
  P4 champions and the best G6 champion auto-qualify; the top 8 get byes.
- Only the CFP and conference title games are scored. Other bowls are ignored in both.
- Playoff games score 1.0 per team times audience weight. Brackets are simulated with
  Elo for the modeled fields; the "actual CFP games" row uses the real 2025 games.
- Pac-12 (2 teams) and independents have no modeled conference champion.

### First results (2025, 10k sims)
Weighted meaning (audience weight = fanbase / Ohio State's):
| format | reg games | reg meaning | playoff games | playoff meaning | total |
|---|---|---|---|---|---|
| 12-team (modeled field) | 888 | 25.4 | 11 | 7.95 | 33.3 |
| 24-team (no title games) | 879 | 33.3 | 23 | 14.1 | 47.4 |
| 12-team (actual CFP games) | 888 | 25.4 | 11 | 6.23 | 31.6 |
Per-game regular-season meaning is 0.029 (12) vs 0.038 (24). The modeled 12-team field
matches 10 of the actual 12 (it picks Notre Dame and Utah over Alabama and Oklahoma).
Treat these numbers as preliminary: they are sensitive to the selector, the resume
weight and the leverage weights in config.py.

### Multi-season run
`python scripts/pull_data.py 2021 2022 2023 2024 2025` then `python scripts/run_meaning.py 2021 2022 2023 2024 2025`
then `python scripts/analyze.py`. Results and video-script notes are in Findings.md.

### Multi-season run
`python scripts/pull_data.py 2021 2022 2023 2024 2025` then `python scripts/run_meaning.py 2021 2022 2023 2024 2025`
then `python scripts/analyze.py`. Results and video-script notes are in Findings.md.

### Update: brand removed from game meaning
Game scores no longer use fanbase weights (config.USE_AUDIENCE_WEIGHTS = False). Weights are now
CFP 1.0, conference 0.75, bye 0.4, rivalry up to 0.4. Game score = 100 * (stake A + stake B) / 2.0, capped
at 100; every playoff game is a flat 100. Fanbase size is used only in `python scripts/fan_impact.py`, which
counts fans on teams that are better or worse off under the 24-team format. The weighted-by-brand results
earlier in this README and the `output_v1/` folder are superseded. See Findings.md.
