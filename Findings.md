# Findings: Does a 24-team playoff make the Power-conference season matter more?
Backbone for the video script. Seasons analyzed: 2021, 2022, 2023, 2024, 2025. All numbers come from `output/`. To regenerate:
`python scripts/run_meaning.py 2021 2022 2023 2024 2025`, then `python scripts/analyze.py`, `python scripts/fan_impact.py` and `python scripts/power_only.py`.

**Focus:** this write-up centers on the Power conferences (the Power 4 today, and the Power 5 in 2021-2023). G6 programs appear where the 24-team format notably helps or hurts them (section 6).

**Ground rules for every 12-team vs 24-team comparison**
- The 12-team format includes its conference championship games. The 24-team format has none. Title games are never left out of the 12-team numbers.
- **"Power" means** the Big Ten, SEC, Big 12 and ACC, plus the Pac-12 in 2021-2023 (when it had 12 teams), plus Notre Dame. Conference membership is each season's real membership (so Texas and Oklahoma count as Power throughout, Washington and Oregon move from the Pac-12 to the Big Ten, and so on).
- **A "Power game" is any game with at least one Power team**, including games against G6 and FCS opponents. That is about 485 games per season.
- Brand size is not part of any game score. It is used only to count fans (section 5).

---

## 1. The question
In 2027 the College Football Playoff expands to 24 teams. Does a bigger playoff make the regular season matter more or less for the Power conferences, and which teams benefit? I scored every game of five real seasons under two formats, using the exact same real game results:

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
- The simulation covers all of FBS (G6 teams still compete for playoff spots). The Power focus only filters which games and teams are reported.

### 2.3 How the playoff field is picked
Each simulated season becomes a playoff field with a rules-based selector. Teams are ranked by **rating + resume**: rating is a 50/50 blend of Elo (as of that week) and SP+; resume is 0.5 × wins.

**12-team world (current format)**
- Conference title games are played. The top two teams in the standings meet; the winner is champion.
- The top 5 conference champions get auto-bids; the rest are at-large.
- The top 4 ranked teams get byes.
- Check against reality: the modeled field matched all 12 real CFP teams in 2024 and 10 of 12 in 2025 (it took Notre Dame and Utah over Alabama and Oklahoma). For 2021-2023 the real playoff was 4 teams, so the 12-team field is hypothetical.

**24-team world (as modeled)**
- **No conference championship games.** The champion is the team with the best conference record (random tiebreak).
- The champion of each Power conference gets an auto-bid, as does the highest-rated G6 champion.
- The remaining spots are at-large, by rating + resume. The top 8 teams in the field get byes (champions are not guaranteed one).
- Bracket (fixed, no reseeding): seeds 9-24 play a first round (9v24 down to 16v17), then those winners meet the 8 bye teams. The 12-team format has 11 playoff games; the 24-team format has 23.

**Why conference-title odds differ between the formats:** "winning the conference" means different things in the two worlds. In the 12-team world a team must finish in the top two and then win the title game, so a regular-season result moves its odds by about half as much (the title game adds a coin flip). In the 24-team world the best record wins, so each late-season game counts more directly.

### 2.4 Playoff games
Every playoff game is a flat **100**. Both teams have everything on the line, and (since brand is out of the game score) the matchup's brand does not change it.

### 2.5 Fan impact (where brand size is used)
- Source: a fanbase-size study by "Altimore College & Co." (Ohio State 11.26M at #1), as cited by 247Sports. **I have not checked the original study**; verify it before showing these numbers on camera.
- The study publishes only the top 65 programs. Teams outside it get 0.2M (the midpoint of the stated 50K-350K range for smaller programs). Boise State, UCF and South Florida are set to 0.95M. The same 2025 numbers are used for all five seasons.
- For each team in each season, I take its **average stake per game** (0-100 scale, regular season). In the 12-team format that includes the team's title game if it played in one; the 24-team format has none. A team is **better off** if the average rises by 2 points or more under the 24-team format, **worse off** if it falls by 2 points or more, otherwise **unchanged**.
- I then add up the fanbase sizes of each group. Fans are counted once per team they follow, so someone who follows two teams is counted twice, and these are rough estimates.

### 2.6 Other data and judgment calls
- **CollegeFootballData.com (CFBD) API**: schedules and scores, betting lines, pre-game Elo, SP+ ratings, conferences, and the real playoff games.
- **Rivalries:** about 72 pairs curated by me from general knowledge, scaled so the biggest are 0.4 (the smallest are about 0.08). These are judgment calls. See `data/manual/rivalries.csv`.
- Only the CFP and conference title games are scored. Other bowl games are ignored in both formats.

---

## 3. Headline numbers (Power games)
The 12-team numbers include the conference title games.

### Average game score
| Season | 12-team, regular season | 24-team, regular season | 12-team, with playoffs | 24-team, with playoffs |
|---|---|---|---|---|
| 2021 | 10.9 | 15.6 | 12.9 | 19.3 |
| 2022 | 10.8 | 15.7 | 12.8 | 19.5 |
| 2023 | 9.8 | 12.9 | 11.8 | 16.8 |
| 2024 | 11.4 | 12.7 | 13.3 | 16.6 |
| 2025 | 10.7 | 15.1 | 12.7 | 18.8 |
| **5-year avg** | **10.7** | **14.4** (+35%) | **12.7** | **18.2** (+43%) |

- **The 24-team format scores higher in every one of the five seasons.** The narrowest gap is 2024 (11.4 vs 12.7).
- For context, across all of FBS the numbers are 8.6 vs 11.7 (+36%), so the Power-only result tells the same story.
- Playoff games always include at least one Power team: 11 per season in the 12-team format and 22-23 in the 24-team format.
- Most games still carry little at stake. The median Power game scores **3.0 in the 12-team format and 10.8 in the 24-team format.**

### Distribution (Power games, per season)
| Measure | 12-team | 24-team |
|---|---|---|
| Games scoring under 5 | **55%** | **38%** |
| Games scoring 25+ | 67 | **92** (+38%) |
| Games scoring 50+ | 17.8 | 19.4 (+9%) |
| Median game score | 3.0 | 10.8 |

The 50+ category is the one place the formats are close: the 12-team format's Power title games (all scoring 75 or higher) make up 4-5 of its roughly 18 games at 50 or higher. In 2024, the 12-team format had more 50+ games than the 24-team format (22 vs 13).

### Season totals (Power games; add up every game's score)
| | 12-team | 24-team |
|---|---|---|
| Regular season, including title games in the 12-team format | 5,193 | 6,901 |
| (of which Power title games) | (412) | n/a |
| Playoff games (11 vs 22-23, at 100 each) | 1,100 | 2,240 |
| **Season total** | **6,293** | **9,138** (+45%) |

Per-game numbers are the fairer comparison, since the 24-team format has more playoff games. Per game, the 24-team format is ahead by 35% (regular season) and 43% (with playoffs).

### What's driving it
Average odds swing per Power team per game (in points of 100, regular season, games in both formats):
| Stake | 12-team | 24-team |
|---|---|---|
| Playoff odds | 5.3 | **8.5** |
| Conference title odds | 3.0 | **4.5** |
| Bye odds | 2.7 | **4.2** |

Every stake grows by about half. A wider field puts far more Power teams on the bubble, and with 8 byes in a 24-team field the bye race is wide open.

---

## 4. The conference title game effect (Power conferences)
The 12-team format has 4-5 Power-conference title games a year. They are the highest-scoring games of the season:
- Scores range from 75 to 100 and average **90**. 35% of them hit the 100 cap.
- Together they add about **412 points a year**, about 8% of the 12-team Power regular-season total.
- Examples: Alabama-Georgia 2025, Iowa-Michigan 2021, Washington-Oregon 2023, SMU-Clemson 2024, Arizona State-Iowa State 2024.

The 24-team format removes them, and still comes out ahead (14.4 vs 10.7 per game).

**Where the replacement meaning comes from:** the last week of the season. With no title game, the final regular-season games (and their rivalries) decide the conference champion, and a conference champion gets an auto-bid.

---

## 5. Who gains and who loses among Power teams

### Fan impact: how many people are better or worse off?
Using the method in 2.5, for Power teams only (about 163M fans per season):

| Season | Fans better off | Fans worse off | Unchanged | Better : worse |
|---|---|---|---|---|
| 2021 | 78.4M (49%) | 22.9M (14%) | 60.0M | 3.4 : 1 |
| 2022 | 98.9M (61%) | 29.0M (18%) | 33.4M | 3.4 : 1 |
| 2023 | 56.0M (34%) | 53.5M (33%) | 55.3M | 1.0 : 1 |
| 2024 | 53.9M (33%) | 54.8M (34%) | 54.4M | 1.0 : 1 |
| 2025 | 66.0M (41%) | 32.4M (20%) | 64.7M | 2.0 : 1 |
| **5-year avg** | **70.7M (44%)** | **38.5M (24%)** | 53.6M (33%) | **1.8 : 1** |

- **About 1.8 fans are better off for every fan who is worse off**, but it swings by season: 3.4 to 1 in 2021 and 2022, a dead heat in 2023 and 2024, and 2 to 1 in 2025.
- On average, 29 Power teams are better off and 8 are worse off, out of about 67.
- **The fan-weighted average stake** (what the average Power fan's team sees): **18.4 (12-team) to 21.3 (24-team)**, up 16%. In 2024 it fell, from 20.6 to 18.0.
- **2023 and 2024 are the "not a free lunch" years.** The fans who gain and the fans who lose are about equal in size.
- **The biggest brands are split.** Among the 19 teams with a fanbase of 3M or more, 30% see their stake per game fall and 44% see it rise.

### Power teams that lose (5-season pooled; stake per game, 12-team to 24-team)
| Team | Fans | 12-team | 24-team | Change |
|---|---|---|---|---|
| Alabama | 5.3M | 42.3 | 28.1 | **-14.2** |
| Georgia | 4.0M | 36.1 | 27.7 | -8.5 |
| Miami | 2.3M | 22.8 | 16.7 | -6.1 |
| Notre Dame | 8.2M | 27.5 | 22.6 | -4.9 |
| Penn State | 6.4M | 29.6 | 25.8 | -3.8 |
| Oregon | 5.5M | 41.0 | 38.9 | -2.1 |
| Ohio State | 11.3M | 27.6 | 26.6 | -1.1 |
| Indiana, Texas Tech | | | | about flat |

The teams that lose are the perennial contenders. They are safe enough that a loss no longer threatens their spot, only a bye, and the ones that reach a title game (Alabama, Georgia) lose that high-stakes game. Alabama, Notre Dame and Georgia account for the largest fan-weighted losses. The pooled drop list is short: apart from these teams, only a handful of Power teams lose anything.

### Power teams that gain (5-season pooled)
| Group | Examples (12-team to 24-team stake per game) |
|---|---|
| **Good-but-not-elite teams (the biggest group)** | Texas A&M 18.3 to 31.7, Iowa 14.2 to 31.1, Washington 16.0 to 28.3, LSU 16.0 to 25.5, Louisville 10.2 to 21.4, USC 20.7 to 28.3, Wisconsin 5.7 to 13.9, North Carolina 10.3 to 20.6 |
| **Rarely-contending teams that suddenly have a path** | Missouri 3.4 to 20.3, Illinois 3.4 to 13.2, Georgia Tech 6.1 to 13.9, NC State 5.3 to 13.0 |
| **Top-brand programs that also gain** | Michigan 25.6 to 30.9, Texas 35.5 to 39.3, Florida 9.3 to 13.7 |

Largest fan-weighted gainers: Texas A&M, LSU, Washington, Wisconsin, Iowa, USC, Michigan, Texas.

### By conference (Power teams, stake per game, 5-season average)
| Group | 12-team | 24-team | Change |
|---|---|---|---|
| ACC | 10.0 | 14.6 | +4.6 |
| SEC | 14.8 | 19.2 | +4.4 |
| Big Ten | 10.3 | 14.3 | +4.0 |
| Big 12 | 12.6 | 15.2 | +2.7 |
| Pac-12 (2021-2023 only) | 14.0 | 20.4 | +6.5 |
| Notre Dame | 27.5 | 22.6 | -4.9 |

Every conference gains. Notre Dame is the exception. My interpretation (not verified): it has no conference title or conference record to chase, so the 24-team format adds little for it.

By team-season, **44% of Power teams are better off by at least 2 points, 12% are worse off, and the rest are about unchanged.**

### 2025 specifically (Power teams)
- **Biggest boosts:** Georgia Tech (20 to 59), Washington (8 to 44), Michigan (13 to 48), Iowa (9 to 43), Tennessee (16 to 48), Virginia (22 to 49), Texas (19 to 46), SMU (22 to 48), Missouri (7 to 31), Louisville (14 to 37).
- **Biggest drops:** Georgia (53 to 27), Miami (48 to 24), Utah (51 to 28), Alabama (61 to 43), Oregon (35 to 18), Ole Miss (44 to 28), Texas Tech (45 to 39). These were the teams with the strongest 12-team cases.

---

## 6. Notable G6 programs
G6 is still a minor part of the story. Across the 61 G6 programs with at least four seasons of data, **the average stake per game rises 2.6 points, 34% are better off by 2 or more, and only 3% are worse off.** The 24-team format mostly gives G6 teams a little more.

### G6 boosts (5-season pooled; stake per game, 12-team to 24-team)
- **Tulane: 20.9 to 38.0** (+17.2), the biggest G6 gain.
- **Memphis: 5.0 to 18.1.**
- **Toledo: 12.7 to 22.9.**
- **UTSA: 14.2 to 24.2.**
- **Troy: 7.5 to 17.5.**
- **Liberty: 12.4 to 22.3.**
- **James Madison: 25.3 to 33.7** (four seasons).
- Others: South Alabama (5.3 to 15.0), Louisiana (11.9 to 21.3), Fresno State (13.0 to 19.7), South Florida (5.7 to 11.8), San Diego State (10.0 to 15.7). Boise State rises less (24.4 to 28.7).
- Programs that moved up to a Power conference during these years (SMU, BYU, UCF, Cincinnati, Houston) also gain in the pooled numbers, for example SMU 20.4 to 35.0 and BYU 16.9 to 24.3. Those figures mix their G6 and Power seasons, so treat them as rough.

### G6 drops
- **North Texas: 13.1 to 8.7** (-4.4), the biggest G6 drop. It reached a title game in 2022 and 2025.
- **Miami (OH): 11.2 to 9.0.**
- **Coastal Carolina: 11.5 to 9.5.**
- Likely reason (my interpretation, not verified): these teams lose their conference title game, and the G6 title game plus the auto-bid for the best G6 champion is a stake that mattered more in the 12-team format.

The rest of the G6 sits near zero in both formats.

---

## 7. Matchups that change the most (Power games; game score, 12-team to 24-team)
These are games with at least one Power team that exist in both formats. The title games, which exist only in the 12-team format, are covered in section 4.

### Gain the most under 24 teams
| Season | Game | 12-team | 24-team | Likely reason (my interpretation, not verified) |
|---|---|---|---|---|
| 2022 | Ohio State vs Michigan | 40 | **100** | Decides the conference champion, with no title game as a backstop, plus a 0.4 rivalry bonus |
| 2023 | Michigan vs Ohio State | 49 | **100** | Same |
| 2022 | Notre Dame at USC | 33 | 95 | Bubble stakes for both |
| 2025 | Texas vs Texas A&M | 45 | 94 | Conference record and bye race |
| 2025 | Virginia Tech at Virginia | 32 | 88 | Conference title race |
| 2025 | Louisville at SMU | 28 | 78 | Bubble/conference race |
| 2022 | Mississippi State at Ole Miss | 27 | 77 | Egg Bowl with bubble stakes |
| 2023 | Utah at Arizona | 1 | 73 | Went from irrelevant to a conference title race |
| 2023 | Washington at Oregon State | 8 | 73 | Same |
| 2023 | Iowa at Nebraska (and again in 2025) | 21 | 71 | Bubble |
| 2023 | Georgia at Tennessee | 4 | 54 | Same |
| 2022 | UCLA at California | 0 | 49 | Went from nothing to a bubble game |

**Script hooks:** *"Ohio State-Michigan scores 40 today. With no title game and a wide playoff, it's a 100."* And: *"UCLA at Cal in 2022 scored 0 out of 100. In a 24-team playoff it's a 49."*

### Lose the most under 24 teams
| Season | Game | 12-team | 24-team | Likely reason (my interpretation, not verified) |
|---|---|---|---|---|
| 2024 | Tennessee at Georgia | 97 | 42 | Safe seeds, so less to lose |
| 2023 | TCU at Oklahoma | 52 | 1 | Oklahoma's season no longer on the line |
| 2025 | Utah at Kansas | 48 | 0 | Utah's 12-team stake disappears |
| 2024 | Tennessee at Vanderbilt | 65 | 18 | Same |
| 2024 | Georgia at Ole Miss | 72 | 31 | Both teams much safer |
| 2022 | Kansas at Kansas State | 62 | 21 | Same |
| 2023 | Oklahoma at BYU | 44 | 4 | Playoff stakes gone |
| 2025 | Kansas State at Utah | 40 | 2 | Same |
| 2024 | Alabama at Tennessee | 91 | 57 | Bye race matters less with 8 byes |
| 2023 | Notre Dame at Clemson | 40 | 5 | Playoff-lock game |

**Script hook:** *"Georgia at Ole Miss in 2024 was a 72. With 24 teams, it drops to 31."*

### Biggest games in each format
- **12-team:** the 4-5 Power title games each year (75-100 each; Alabama-Georgia 2025, Iowa-Michigan 2021, Washington-Oregon 2023 and others hit 100), then regular-season games like Tennessee at Georgia 2024 (97), Oregon-Utah 2022 (91), Alabama at Tennessee 2024 (91) and Texas-Oklahoma 2023 (89).
- **24-team:** Ohio State-Michigan 2022 and 2023 (100 each), Oklahoma-Oklahoma State 2021 (100), Oregon at Utah 2021 (100), Notre Dame at USC 2022 (95), Texas-Texas A&M 2025 (94), Texas A&M-Texas 2024 (90).

---

## 8. Caveats to say out loud (or at least know)
1. **Results are model outputs, not facts.** They depend on the weights (1.0 / 0.75 / 0.4, rivalry up to 0.4), the selector, the resume weight and the bracket I picked. I have not tested how sensitive they are. A sensitivity pass is the most important next step.
2. **The Power filter is a choice.** I counted Notre Dame as Power, counted the Pac-12 only in 2021-2023, and counted every game with at least one Power team (including games against G6 and FCS opponents, about 14% of all games involve an FCS opponent and most score near zero). Excluding those would raise both formats' averages.
3. **The rivalry scale matters a lot.** At up to 0.4 per team, a pure rivalry game scores up to 40 even with no other stakes, which is a large share of the scale. The list and values are my judgment.
4. **The 24-team format isn't finalized.** I used your rules (top 8 byes, Power champions auto-bid, best G6 champion, no title games). If those change, rerun.
5. **Fanbase numbers are unverified**, and the fan counts depend on them. Fans are counted per team they follow, so the totals double count people. The "better off / worse off" call uses a 2-point threshold, which is a judgment call. A few Power teams are not in the published top 65 and use the 0.2M default.
6. **The same 2025 fanbase numbers are used for all five seasons.**
7. **SP+ ratings are end-of-season values**, a mild hindsight leak into the selector. Elo is as of each week.
8. **12-team results for 2021-2023 are hypothetical** (the real playoff was 4 teams).
9. **Only the CFP and conference title games are scored.** Other bowl games are ignored in both formats.
10. **The playoff brackets and fields are simplified.** Fixed seeding, Elo-based win odds. Since every playoff game is a flat 100, bracket details only change *which* games exist, not their scores.
11. **Simulation noise.** 10,000 sims per week; a team's odds can wobble by a point or two. Games where one side wins fewer than 10 of the 10,000 simulations are scored 0.

---

## 9. Open questions for the script
- **Headline stat:** probably "the median Power game goes from 3 to 10.8 out of 100" or "the average Power game score goes from 10.7 to 14.4 (and 12.7 to 18.2 with playoffs)."
- **Fan story:** "About 2 Power fans are better off for every 1 who is worse off, but in 2023 and 2024 it was a coin flip." The losers are Alabama, Georgia, Miami, Notre Dame and Penn State.
- Do we want a 12-team vs 24-team bracket visual for 2025 (who gets in under each)?
- Should the rivalry scale be softened? Right now a rivalry game alone can be worth 40.
- Do we want a sensitivity table (different weights, with and without the bye term) before publishing?
