# Findings: How much does a college football game *mean*, and who does a 24-team playoff help?
Backbone for the video script. Seasons analyzed: 2021, 2022, 2023, 2024, 2025. All numbers come from `output/`. To regenerate:
`python scripts/run_meaning.py 2021 2022 2023 2024 2025`, then `python scripts/analyze.py` and `python scripts/fan_impact.py`.

**Two separate questions, answered separately:**
1. **How much does each game matter?** A 0-100 score for every game, based only on stakes (playoff odds, conference odds, bye odds, rivalry). Brand size is *not* used here.
2. **Who benefits?** Brand/fanbase size is used only afterward, to count how many fans are better off or worse off under a 24-team playoff.

**Ground rule for every 12-team vs 24-team comparison:** the 12-team format includes its conference championship games (9-10 per season). The 24-team format has none. Title games are never left out of the 12-team numbers.

---

## 1. The question
In 2027 the College Football Playoff expands to 24 teams. Does a bigger playoff make the regular season matter more or less, and for whom? I scored every game of five real seasons under two formats, using the exact same real game results:

- **12-team format** (the current setup): conference championship games are played.
- **24-team format** (the 2027 setup, as modeled): conference championship games are gone.

---

## 2. Methodology

### 2.1 The game score (0-100)
For each team in a game, I measure how much the result changes that team's odds of three things, plus a rivalry bonus:

| Stake | Weight |
|---|---|
| Making the playoff | **1.0** |
| Winning the conference | **0.75** |
| Earning a first-round bye | **0.4** |
| Rivalry game | flat bonus per team, **0.08 up to 0.4** for the biggest rivalries |

`team stake = 1.0 × ΔP(make CFP) + 0.75 × ΔP(win conference) + 0.4 × ΔP(bye) + rivalry bonus`

ΔP = |P(outcome if the team wins) − P(outcome if the team loses)|, measured over 10,000 simulated seasons.

`game score = 100 × (team A stake + team B stake) ÷ 2.0`, capped at 100.

**How to read the 0-100 scale**
- **100** = both teams' whole season on the line, like a playoff game. Every actual playoff game is a flat 100.
- **A game with no stakes** at all scores 0-1.
- **A pure rivalry game** with nothing else on the line scores 100 × the rivalry bonus: 40 for the biggest ones (Ohio State-Michigan, Alabama-Auburn, Texas-Oklahoma), down to about 8 for minor ones.
- A game's score does not depend on how likely the outcome was. A heavy favorite's game can still score high if a loss would wreck their season.
- **Brand size is not in this score.** An Iowa State game and an Ohio State game with the same stakes score the same.

### 2.2 How the odds are calculated (no hindsight)
- For each week, I freeze the season: results through the previous week are real, everything after is unknown.
- I simulate the rest of the season **10,000 times**, using each game's pre-game win probability.
- For each game that week, I split the simulated seasons into "team A won" and "team B won" and compare each team's playoff, conference and bye odds between the two groups.
- Win probabilities come from **betting spreads** (average across sportsbooks), converted with a normal curve (standard deviation of 13.5 points). If a game has no line, I use **pre-game Elo**. FBS vs FCS games are set to 97% for the FBS team.

### 2.3 How the playoff field is picked
Each simulated season becomes a playoff field with a rules-based selector. Teams are ranked by **rating + resume**: rating is a 50/50 blend of Elo (as of that week) and SP+; resume is 0.5 × wins.

**12-team world (current format)**
- Conference title games are played. The top two teams in the standings meet; the winner is champion.
- The top 5 conference champions get auto-bids; the rest are at-large.
- The top 4 ranked teams get byes.
- Check against reality: the modeled field matched all 12 real CFP teams in 2024 and 10 of 12 in 2025 (it took Notre Dame and Utah over Alabama and Oklahoma). For 2021-2023 the real playoff was 4 teams, so the 12-team field is hypothetical.

**24-team world (as modeled)**
- **No conference championship games.** The champion is the team with the best conference record (random tiebreak).
- The champion of each Power conference gets an auto-bid, as does the highest-rated Group of 5 champion.
- The remaining spots are at-large, by rating + resume. The top 8 teams in the field get byes (champions are not guaranteed one).
- Power conferences are the Big Ten, SEC, Big 12, ACC (plus the Pac-12 in 2021-2023, when it had 12 teams).
- Bracket (fixed, no reseeding): seeds 9-24 play a first round (9v24 down to 16v17), then those winners meet the 8 bye teams. The 12-team format has 11 playoff games; the 24-team format has 23.

### 2.4 Playoff games
Every playoff game is a flat **100**. Both teams have everything on the line, and (since brand is out of the game score) the matchup's brand does not change it.

### 2.5 Fan impact (where brand size is used)
- Source: a fanbase-size study attributed to "Altimore College & Co." (Ohio State 11.26M at #1). The numbers were copied from an AI chat summary that cites 247Sports, On3 and Sports Media Watch. **I could not verify the study independently**; check the original 247Sports article before showing these numbers on camera.
- The study publishes only the top 65 programs. Teams outside it get 0.2M (the midpoint of the stated 50K-350K range for Group of 5 teams). Boise State, UCF and South Florida are set to 0.95M. The same 2025 numbers are used for all five seasons.
- For each team in each season, I take its **average stake per game** (0-100 scale, regular season). In the 12-team format that includes the team's title game if it played in one; the 24-team format has none. A team is **better off** if the average rises by 2 points or more under the 24-team format, **worse off** if it falls by 2 points or more, otherwise **unchanged**.
- I then add up the fanbase sizes of each group. Fans are counted once per team they follow, so someone who follows two teams is counted twice, and these are rough estimates.

### 2.6 Other data and judgment calls
- **CollegeFootballData.com (CFBD) API**: schedules and scores, betting lines, pre-game Elo, SP+ ratings, conferences, and the real playoff games.
- **Rivalries:** about 72 pairs curated by me from general knowledge, scaled so the biggest are 0.4 (the smallest are about 0.08). These are judgment calls. See `data/manual/rivalries.csv` (the earlier, smaller scale is saved as `rivalries_v1.csv`).
- Only the CFP and conference title games are scored. Other bowl games are ignored in both formats.

---

## 3. Headline numbers

### Average game score
The 12-team numbers include the conference title games.

| Season | 12-team, regular season | 24-team, regular season | 12-team, with playoffs | 24-team, with playoffs |
|---|---|---|---|---|
| 2021 | 9.3 | 12.8 | 10.5 | 15.2 |
| 2022 | 8.5 | 12.8 | 9.7 | 15.1 |
| 2023 | 8.0 | 10.6 | 9.1 | 13.0 |
| 2024 | 8.7 | 10.7 | 9.8 | 13.0 |
| 2025 | 8.5 | 11.7 | 9.6 | 13.9 |
| **5-year avg** | **8.6** | **11.7** (+36%) | **9.7** | **14.0** (+44%) |

- **The 24-team format scores higher in every one of the five seasons.**
- **There is no outlier season.** (An earlier version that weighted games by brand showed 2024 going the other way. That was caused by the brand weighting, not the format.)
- The averages are low because most games carry almost no stakes. This is the main finding, not a flaw. The median game scores **1.9 in the 12-team format and 5.7 in the 24-team format.**

### Distribution (regular season, per-season average; the 12-team numbers include title games)
| Measure | 12-team | 24-team |
|---|---|---|
| Games scoring under 5 | **62%** | **49%** |
| Games scoring 25+ | 86 | **134** (+56%) |
| Games scoring 50+ | 24 | 26 (+12%) |
| Median game score | 1.9 | 5.7 |

The 50+ category is the one place the formats are close. The 12-team format's title games (all scoring 75-100) make up 9-10 of its roughly 24 games at 50 or higher. In 2024, the 12-team format had more 50+ games than the 24-team format (28 vs 17).

### Season totals (add up every game's score)
| | 12-team | 24-team |
|---|---|---|
| Regular season, including title games in the 12-team format | 7,445 | 10,038 |
| (of which title games) | (843) | n/a |
| Playoff games (11 vs 23, at 100 each) | 1,100 | 2,300 |
| **Season total, everything** | **8,545** | **12,338** (+44%) |

Per-game numbers are the fairer comparison, since the 24-team format has more playoff games. Per game, the 24-team format is ahead by 36% (regular season) and 44% (with playoffs).

### What's driving it
Average odds swing per team per game (in points of 100, regular season, games in both formats):
| Stake | 12-team | 24-team |
|---|---|---|
| Playoff odds | 3.4 | **6.1** |
| Conference title odds | 3.1 | **4.3** |
| Bye odds | 1.3 | **2.2** |

Every stake grows. The biggest jump is in playoff odds: a wider field puts far more teams on the bubble.

---

## 4. The conference title game effect
The 12-team format has 9-10 conference title games a year. They are the highest-scoring games of the season by a wide margin:
- Title game scores range from 75 to 100 and average **88**. 38% of them hit the 100 cap.
- Together they add about **843 points a year**, about 11% of the 12-team regular-season total.
- Examples: Alabama-Georgia 2025, Iowa-Michigan 2021, Washington-Oregon 2023, and (surprisingly) Group of 5 title games like Boise State-UNLV 2024, Tulane-North Texas 2025 and Wake Forest-Pittsburgh 2021. Without brand weighting, every title game is a near-100 game for both teams.

The 24-team format removes them, and still comes out ahead: 11.7 on about 857 games, versus 8.6 on about 867 games (title games included) in the 12-team world.

**Where the replacement meaning comes from:** the last week of the season. With no title game, the final regular-season games (and their rivalries) decide the conference champion, and a conference champion gets an auto-bid.

---

## 5. Who gains and who loses

### Fan impact: how many people are better or worse off?
Using the method in 2.5 (team stake per game rising or falling by at least 2 points, with title games counted in the 12-team format):

| Season | Fans better off | Fans worse off | Unchanged | Better : worse |
|---|---|---|---|---|
| 2021 | 83.7M (47%) | 23.1M (13%) | 71.7M | 3.6 : 1 |
| 2022 | 106.0M (59%) | 29.6M (17%) | 43.0M | 3.6 : 1 |
| 2023 | 58.4M (33%) | 55.2M (31%) | 65.4M | 1.1 : 1 |
| 2024 | 57.2M (32%) | 55.9M (31%) | 66.2M | 1.0 : 1 |
| 2025 | 70.9M (39%) | 33.2M (19%) | 75.6M | 2.1 : 1 |
| **5-year avg** | **75.2M (42%)** | **39.4M (22%)** | 64.4M (36%) | **1.9 : 1** |

- **About 1.9 fans are better off for every fan who is worse off**, but it varies a lot by season: 3.6 to 1 in 2021 and 2022, essentially a tie in 2023 and 2024.
- On average, 45 FBS teams are better off and 11 are worse off.
- The total of about 179M fans per season double counts people who follow more than one team. Counting only the 67 teams with a published fanbase gives nearly the same answer (72M better, 39M worse), so the Group of 5 estimates aren't driving it.
- **The fan-weighted average stake** (what the average fan's team sees): **17.4 (12-team) to 20.3 (24-team)**, up 17%. In 2024 it fell, from 19.3 to 17.3.
- **2023 and 2024 are the "not a free lunch" years.** The fans who gain and the fans who lose are about equal in size.
- **The biggest brands are split.** Among the 19 teams with a fanbase of 3M or more, 30% see their stake per game fall and 44% see it rise.

### Who drops (5-season pooled; stake per game, 12-team to 24-team)
| Team | Fans | 12-team | 24-team | Change |
|---|---|---|---|---|
| Alabama | 5.3M | 42.3 | 28.1 | **-14.2** |
| Georgia | 4.0M | 36.1 | 27.7 | -8.5 |
| Miami | 2.3M | 22.8 | 16.7 | -6.1 |
| Notre Dame | 8.2M | 27.5 | 22.6 | -4.9 |
| North Texas (Group of 5) | 0.2M | 13.1 | 8.7 | -4.4 |
| Penn State | 6.4M | 29.6 | 25.8 | -3.8 |
| Oregon | 5.5M | 41.0 | 38.9 | -2.1 |
| Ohio State | 11.3M | 27.6 | 26.6 | -1.1 |

The teams that lose are the perennial contenders and the title game regulars. They are safe enough that a loss no longer threatens their spot, only a bye, and teams that reach a title game lose that high-stakes game (Alabama and Georgia in the SEC title game, North Texas in the AAC). Alabama, Notre Dame and Georgia account for the largest fan-weighted losses.

### Who gains (5-season pooled)
| Group | Examples (12-team to 24-team stake per game) |
|---|---|
| **Good-but-not-elite Power teams (the biggest group)** | Texas A&M 18.3 to 31.7, Iowa 14.2 to 31.1, Washington 16.0 to 28.3, LSU 16.0 to 25.5, Louisville 10.2 to 21.4, USC 20.7 to 28.3, Wisconsin 5.7 to 13.9 |
| **Strong Group of 5 programs** | Tulane 20.9 to 38.0, SMU 20.4 to 35.0, Memphis 5.0 to 18.1, Toledo 12.7 to 22.9, UTSA 14.2 to 24.2, Troy 7.5 to 17.5 |
| **Rarely-contending Power teams** | Oregon State 4.4 to 20.1, Missouri 3.4 to 20.3, Washington State 2.4 to 11.4, Illinois 3.4 to 13.2 |
| **Top-brand programs that also gain** | Michigan 25.6 to 30.9, Texas 35.5 to 39.3, Florida 9.3 to 13.7 |

Largest fan-weighted gainers: Texas A&M, LSU, Washington, Wisconsin, Iowa, USC, Michigan, Texas.

### By tier (teams ranked by Elo, stake per game, 5-season average)
| Tier | 12-team | 24-team | Change |
|---|---|---|---|
| Top 12 | 35.1 | 31.3 | **-3.8** |
| 13-30 | 19.1 | 31.1 | **+12.0** (+63%) |
| 31-65 | 9.1 | 16.3 | **+7.2** (+79%) |
| 66 and below | 2.0 | 2.6 | +0.6 (still close to nothing) |

By season the top-12 tier moves +4.9, +3.5, -6.7, -16.6, -4.1 (2021 to 2025). 2024 stands out: the elite teams lost the most that year, and it was also a split year for fans. I haven't investigated why.

### By conference (stake per game, 5-season average)
| Group | 12-team | 24-team | Change |
|---|---|---|---|
| ACC | 10.0 | 14.6 | +4.6 |
| SEC | 14.8 | 19.2 | +4.4 |
| Big Ten | 10.3 | 14.3 | +4.1 |
| Big 12 | 12.6 | 15.2 | +2.7 |
| Independents | 7.5 | 10.3 | +2.7 |
| Group of 5 | 6.2 | 8.8 | +2.6 |

Every group gains. (Pac-12 figures are ignored; it was down to 2 teams in 2024-25.)

### The tail
The bottom of FBS gets almost nothing. Teams ranked 66th and below see their stake per game move from 2.0 to 2.6, and about 71 teams are in that group. The 24-team playoff makes the middle of the sport matter more, not the bottom.

### 2025 specifically
- **Biggest boosts:** Georgia Tech (20 to 59), Washington (8 to 45), Michigan (13 to 48), Iowa (9 to 43), Tennessee (16 to 48), South Florida (24 to 55), Virginia (22 to 49), Texas (19 to 46), SMU (22 to 48), Missouri (7 to 31).
- **Biggest drops:** Georgia (53 to 27), Miami (48 to 24), Utah (51 to 28), Alabama (61 to 43), North Texas (54 to 37), Oregon (35 to 18), Ole Miss (44 to 28). These were the teams with the strongest 12-team cases, plus title game teams.

---

## 6. Matchups that change the most (game score, 12-team to 24-team)
These are games that exist in both formats. The title games, which exist only in the 12-team format, are covered in section 4.

### Gain the most under 24 teams
| Season | Game | 12-team | 24-team | Likely reason (my interpretation, not verified) |
|---|---|---|---|---|
| 2022 | Ohio State vs Michigan | 40 | **100** | Decides the conference champion, with no title game as a backstop, plus a 0.4 rivalry bonus |
| 2023 | Michigan vs Ohio State | 49 | **100** | Same |
| 2022 | USC at Notre Dame | 33 | 95 | Bubble stakes for both |
| 2025 | Texas vs Texas A&M | 45 | 94 | Conference record and bye race |
| 2025 | Virginia vs Virginia Tech | 32 | 88 | Conference title race |
| 2023 | Arizona vs Utah | 0.6 | 73 | Went from irrelevant to a conference title game |
| 2023 | Oregon State vs Washington | 8 | 73 | Same |
| 2025 | SMU vs Louisville | 28 | 78 | Bubble/conference race |
| 2025 | Nebraska vs Iowa | 21 | 71 | Bubble |
| 2025 | Tennessee vs Oklahoma | 2 | 48 | Went from irrelevant to a bubble game |
| 2025 | Washington vs Illinois | 0.2 | 43 | Same |

**Script hooks:** *"Ohio State-Michigan scores 40 today. With no title game and a wide playoff, it's a 100."* And: *"Tennessee-Oklahoma in 2025 scored 2 out of 100. In a 24-team playoff it's a 48."*

### Lose the most under 24 teams
| Season | Game | 12-team | 24-team | Likely reason (my interpretation, not verified) |
|---|---|---|---|---|
| 2024 | Tennessee at Georgia | 97 | 42 | Safe seeds, so less to lose |
| 2023 | TCU at Oklahoma | 52 | 1.5 | Oklahoma's season no longer on the line |
| 2025 | Utah at Kansas | 48 | 0.04 | Utah's 12-team stake disappears |
| 2024 | Tennessee at Vanderbilt | 65 | 18 | Same |
| 2025 | Kansas State at Utah | 40 | 1.6 | Same |
| 2024 | Georgia at Ole Miss | 72 | 31 | Both teams much safer |
| 2023 | Oklahoma at BYU | 44 | 4 | Playoff stakes gone |
| 2024 | Alabama at Tennessee | 91 | 57 | Bye race matters less with 8 byes |
| 2023 | Notre Dame at Clemson | 40 | 5 | Playoff-lock game |

**Script hook:** *"Georgia at Ole Miss in 2024 was a 72. With 24 teams, it drops to 31."*

### Biggest games in each format
- **12-team:** the 9-10 title games each year (75-100 each), then regular-season games like Tennessee at Georgia 2024 (97), Utah at Oregon 2022 (91), Alabama at Tennessee 2024 (91) and Texas-Oklahoma 2023 (89).
- **24-team:** Bedlam 2021 (Oklahoma vs Oklahoma State, 100), Ohio State-Michigan 2022 and 2023 (100 each), Oregon at Utah 2021 (100), USC at Notre Dame 2022 (95), Texas-Texas A&M 2025 (94).

---

## 7. Caveats to say out loud (or at least know)
1. **Results are model outputs, not facts.** They depend on the weights (1.0 / 0.75 / 0.4, rivalry up to 0.4), the selector, the resume weight and the bracket I picked. I have not tested how sensitive they are. A sensitivity pass is the most important next step.
2. **The rivalry scale matters a lot now.** At up to 0.4 per team, a pure rivalry game scores up to 40 even with no other stakes, which is a large share of the scale. The list and values are my judgment.
3. **The 24-team format isn't finalized.** I used your rules (top 8 byes, Power champions auto-bid, best Group of 5 champion, no title games). If those change, rerun.
4. **Fanbase numbers are unverified**, and the fan counts depend on them. Fans are counted per team they follow, so the totals double count people. The "better off / worse off" call uses a 2-point threshold, which is a judgment call.
5. **The same 2025 fanbase numbers are used for all five seasons.**
6. **SP+ ratings are end-of-season values**, a mild hindsight leak into the selector. Elo is as of each week.
7. **12-team results for 2021-2023 are hypothetical** (the real playoff was 4 teams). James Madison (2023) and Liberty were modeled as eligible even if they had postseason restrictions.
8. **Only the CFP and conference title games are scored.** Other bowl games are ignored in both formats.
9. **Conference membership changed a lot** (Pac-12 collapse after 2023, expansions). The model uses each season's real membership. The Pac-12 has only 2 teams in 2024-25 and gets no modeled champion.
10. **The playoff brackets and fields are simplified.** Fixed seeding, Elo-based win odds. Since every playoff game is a flat 100, bracket details only change *which* games exist, not their scores.
11. **Simulation noise.** 10,000 sims per week; a team's odds can wobble by a point or two. Games where one side wins fewer than 10 of the 10,000 simulations are scored 0.

---

## 8. Open questions for the script
- **Headline stat:** probably "the median game goes from 1.9 to 5.7" or "the average game score goes from 8.6 to 11.7 (and 9.7 to 14.0 with playoffs)."
- **Fan story:** "About 2 fans are better off for every 1 who is worse off, but in 2023 and 2024 it was a coin flip." The losers are Alabama, Georgia, Miami, Notre Dame and Penn State.
- Do we want a 12-team vs 24-team bracket visual for 2025 (who gets in under each)?
- Should the rivalry scale be softened? Right now a rivalry game alone can be worth 40.
- Do we want a sensitivity table (different weights, with and without the bye term) before publishing?
