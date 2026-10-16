# Findings: Does a 24-team playoff make the Power-conference season matter more?
Seasons analyzed: 2021, 2022, 2023, 2024, 2025, 2026

**Focus:** this write-up centers on the Power conferences (the Power 4 today, and the Power 5 in 2021-2023). G6 programs appear where the 24-team format notably helps or hurts them (section 6). Section 10 covers the 2026 season so far.

**Ground rules for every 12-team vs 24-team comparison**
- The 12-team format includes its conference championship games. The 24-team format has none. Title games are never left out of the 12-team numbers.
- **"Power" means** the Big Ten, SEC, Big 12 and ACC, plus the Pac-12 in 2021-2023 (when it had 12 teams), plus Notre Dame. Conference membership is each season's real membership (so Texas and Oklahoma count as Power throughout, Washington and Oregon move from the Pac-12 to the Big Ten, and so on).
- **A "Power game" is any game with at least one Power team**, including games against G6 and FCS opponents. That is about 485 games per season.
- Brand size is not part of any game score. It is used only to count fans (section 5).
- **Selection:** the playoff field leans on each team's resume (who it beat and who it lost to), with power ratings (Elo and SP+) as a smaller factor. See 2.3.

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
Each simulated season becomes a playoff field with a rules-based selector. Teams are ranked by a **selection score = rating + 0.5 × resume**.
- **Resume** is built game by game. A win is worth 1 plus a bonus for a strong opponent (up to +0.6) or minus a bit for a weak one. A loss costs 1, but less when the opponent is strong and more when it is weak. A win over an FCS team is worth only 0.2, and a loss to one costs 2. In the 12-team world, a title game win adds 1 and a title game loss subtracts 1.
- **Rating** is a 50/50 blend of Elo (as of that week) and SP+. It is the smaller factor: about a quarter of the variation in the selection score, versus nearly half in the previous version of this analysis.
- Check against reality: the modeled 12-team field matched **all 12 real CFP teams in 2024 and 11 of 12 in 2025** (it took Notre Dame over Alabama). For 2021-2023 the real playoff was 4 teams, so the 12-team field is hypothetical.

**12-team world (current format)**
- Conference title games are played. The top two teams in the standings meet; the winner is champion.
- The top 5 conference champions get auto-bids; the rest are at-large.
- The top 4 ranked teams get byes.

**24-team world (as modeled)**
- **No conference championship games.** The champion is the team with the best conference record (random tiebreak).
- The champion of each Power conference gets an auto-bid, as does the highest-rated G6 champion.
- The remaining spots are at-large, by the selection score. The top 8 teams in the field get byes (champions are not guaranteed one).
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
- **Rivalries:** about 72 pairs curated by me from general knowledge, scaled so the biggest are 0.4 (the smallest are about 0.08). These are judgment calls.
- Only the CFP and conference title games are scored. Other bowl games are ignored in both formats.

---

## 3. Headline numbers (Power games)
The 12-team numbers include the conference title games.

### Average game score
| Season | 12-team, regular season | 24-team, regular season | 12-team, with playoffs | 24-team, with playoffs |
|---|---|---|---|---|
| 2021 | 12.7 | 17.3 | 14.7 | 21.0 |
| 2022 | 12.1 | 17.8 | 14.1 | 21.5 |
| 2023 | 11.6 | 14.3 | 13.5 | 18.0 |
| 2024 | 12.1 | 14.7 | 14.0 | 18.4 |
| 2025 | 12.4 | 16.8 | 14.3 | 20.6 |
| **5-year avg** | **12.2** | **16.2** (+33%) | **14.1** | **19.9** (+41%) |

- **The 24-team format scores higher in every one of the five seasons.** The narrowest gaps are 2023 (11.6 vs 14.3) and 2024 (12.1 vs 14.7).
- For context, across all of FBS the numbers are 9.3 vs 12.7 (+37%), so the Power-only result tells the same story.
- Playoff games always include at least one Power team: 11 per season in the 12-team format and 22-23 in the 24-team format.
- Most games still carry little at stake. The median Power game scores **4.6 in the 12-team format and 13.3 in the 24-team format.**

### Distribution (Power games, per season)
| Measure | 12-team | 24-team |
|---|---|---|
| Games scoring under 5 | **51%** | **32%** |
| Games scoring 25+ | 79 | **109** (+39%) |
| Games scoring 50+ | 19.8 | 21.8 (+10%) |
| Median game score | 4.6 | 13.3 |

The 50+ category is the one place the formats are close: the 12-team format's Power title games (4-5 per season, all scoring 75 or higher) make up much of its roughly 20 games at 50 or higher. In 2024, the 12-team format had more 50+ games than the 24-team format (23 vs 16).

### Season totals (Power games; add up every game's score)
| | 12-team | 24-team |
|---|---|---|
| Regular season, including title games in the 12-team format | 5,902 | 7,767 |
| (of which Power title games) | (440) | n/a |
| Playoff games (11 vs 22-23, at 100 each) | 1,100 | 2,210 |
| **Season total** | **7,002** | **9,978** (+43%) |

Per-game numbers are the fairer comparison, since the 24-team format has more playoff games. Per game, the 24-team format is ahead by 33% (regular season) and 41% (with playoffs).

### What's driving it
Average odds swing per Power team per game (in points of 100, regular season, games in both formats):
| Stake | 12-team | 24-team |
|---|---|---|
| Playoff odds | 6.7 | **10.1** |
| Conference title odds | 3.0 | **4.5** |
| Bye odds | 3.4 | **5.5** |

Every stake grows by about half. A wider field puts far more Power teams on the bubble, and with 8 byes in a 24-team field the bye race is wide open.

---

## 4. The conference title game effect (Power conferences)
The 12-team format has 4-5 Power-conference title games a year. They are the highest-scoring games of the season:
- Scores range from 75 to 100 and average **96**. 70% of them hit the 100 cap.
- Together they add about **440 points a year**, about 7.5% of the 12-team Power regular-season total.
- Examples: Georgia-LSU 2022, Iowa-Michigan 2021, Washington-Oregon 2023, SMU-Clemson 2024, Arizona State-Iowa State 2024.

The 24-team format removes them, and still comes out ahead (16.2 vs 12.2 per game).

**Where the replacement meaning comes from:** the last week of the season. With no title game, the final regular-season games (and their rivalries) decide the conference champion, and a conference champion gets an auto-bid.

---

## 5. Who gains and who loses among Power teams

### Fan impact: how many people are better or worse off?
Using the method in 2.5, for Power teams only (about 163M fans per season):

| Season | Fans better off | Fans worse off | Unchanged | Better : worse |
|---|---|---|---|---|
| 2021 | 75.2M (47%) | 36.4M (23%) | 49.8M | 2.1 : 1 |
| 2022 | 83.8M (52%) | 34.1M (21%) | 43.4M | 2.5 : 1 |
| 2023 | 59.1M (36%) | 65.1M (40%) | 40.5M | 0.9 : 1 |
| 2024 | 74.9M (46%) | 58.5M (36%) | 29.7M | 1.3 : 1 |
| 2025 | 70.8M (43%) | 31.6M (19%) | 60.7M | 2.2 : 1 |
| **5-year avg** | **72.7M (45%)** | **45.2M (28%)** | 44.8M (28%) | **1.6 : 1** |

- **About 1.6 fans are better off for every fan who is worse off**, but it swings by season: 2.5 to 1 in 2022, and in 2023 slightly more fans were worse off than better off (0.9 to 1).
- On average, 31 Power teams are better off and 9 are worse off, out of about 67. By team-season, **47% of Power teams are better off by at least 2 points, 14% are worse off, and the rest are about unchanged.**
- **The fan-weighted average stake** (what the average Power fan's team sees): **21.2 (12-team) to 23.4 (24-team)**, up 10%. In 2023 it was flat (23.3 vs 23.2) and in 2024 it fell, from 22.2 to 20.8.
- **2023 and 2024 are the "not a free lunch" years.**
- **The biggest brands are split.** Among the 19 teams with a fanbase of 3M or more, 43% see their stake per game rise and 35% see it fall.

### Power teams that lose (5-season pooled; stake per game, 12-team to 24-team)
| Team | Fans | 12-team | 24-team | Change |
|---|---|---|---|---|
| Alabama | 5.3M | 47.2 | 30.7 | **-16.5** |
| Georgia | 4.0M | 40.4 | 30.7 | -9.7 |
| Penn State | 6.4M | 33.9 | 27.2 | -6.7 |
| Notre Dame | 8.2M | 34.0 | 27.6 | -6.4 |
| Oregon | 5.5M | 47.5 | 42.7 | -4.8 |
| Ole Miss | 2.0M | 39.1 | 34.6 | -4.5 |
| Miami | 2.3M | 23.8 | 20.2 | -3.6 |
| Oklahoma | 3.1M | 36.2 | 33.4 | -2.7 |
| Ohio State | 11.3M | 30.3 | 28.1 | -2.1 |
| Indiana, Texas | | | | -1.5, -0.9 |

The teams that lose are the perennial contenders. They are safe enough that a loss no longer threatens their spot, only a bye, and the ones that reach a title game (Alabama, Georgia) lose that high-stakes game. Alabama, Notre Dame, Penn State and Georgia account for the largest fan-weighted losses. Only 9 of 63 Power teams (with 4+ seasons of data) lose 2 points or more.

### Power teams that gain (5-season pooled)
| Group | Examples (12-team to 24-team stake per game) |
|---|---|
| **Good-but-not-elite teams (the biggest group)** | Iowa 19.1 to 32.1, Utah 26.2 to 38.3, Texas A&M 20.7 to 32.3, Washington 17.4 to 27.7, Louisville 11.8 to 23.0, LSU 23.3 to 30.4, USC 26.2 to 31.7 |
| **Rarely-contending teams that suddenly have a path** | Illinois 5.1 to 19.9, Missouri 9.4 to 21.0, North Carolina 11.0 to 21.4, NC State 5.6 to 15.4, Kentucky 5.7 to 15.4, Mississippi State 3.8 to 12.9 |
| **Top-brand programs that also gain** | Florida 10.5 to 16.4, Wisconsin 10.9 to 17.3, Texas A&M (above) |

Largest fan-weighted gainers: Texas A&M, Florida, Washington, Wisconsin, Iowa, LSU, USC, Utah.

### By conference (Power teams, stake per game, 5-season average)
| Group | 12-team | 24-team | Change |
|---|---|---|---|
| ACC | 10.5 | 16.2 | +5.7 |
| SEC | 18.2 | 22.2 | +3.9 |
| Big 12 | 13.7 | 17.5 | +3.8 |
| Big Ten | 12.5 | 16.3 | +3.7 |
| Pac-12 (2021-2023 only) | 14.9 | 22.0 | +7.1 |
| Notre Dame | 34.0 | 27.6 | -6.4 |

Every conference gains. Notre Dame is the exception. My interpretation (not verified): it has no conference title or conference record to chase, so the 24-team format adds little for it.

### 2025 specifically (Power teams)
- **Biggest boosts:** Georgia Tech (21 to 60), Washington (11 to 45), Iowa (11 to 44), Tennessee (18 to 51), Illinois (6 to 36), Virginia (18 to 47), Missouri (10 to 32), Louisville (15 to 37), SMU (19 to 39), Michigan (21 to 40).
- **Biggest drops:** Georgia (58 to 31), Alabama (69 to 46), Oregon (45 to 23), Miami (49 to 32), Ole Miss (50 to 37), Notre Dame (42 to 29), Oklahoma (35 to 29). These were the teams with the strongest 12-team cases.

---

## 6. Notable G6 programs
G6 is still a minor part of the story. Across the 61 G6 programs with at least four seasons of data, **the average stake per game rises 2.8 points, 36% are better off by 2 or more, and only 2% are worse off.** The 24-team format mostly gives G6 teams a little more.

### G6 boosts (5-season pooled; stake per game, 12-team to 24-team)
- **Tulane: 21.8 to 44.8** (+23.1), the biggest G6 gain.
- **Troy: 7.6 to 21.6.**
- **UTSA: 10.1 to 23.4.**
- **Memphis: 4.5 to 14.1.**
- **Toledo: 11.9 to 21.0.**
- **James Madison: 26.0 to 34.2** (four seasons).
- **Boise State: 24.3 to 30.6.**
- Others: Liberty (14.2 to 21.3), App State (8.3 to 16.9), Air Force (12.3 to 19.4), Louisiana (11.2 to 17.8), Fresno State (10.5 to 16.9).
- Programs that moved up to a Power conference during these years (SMU, BYU, UCF, Cincinnati, Houston) also gain in the pooled numbers, for example SMU 15.6 to 36.3 and BYU 18.7 to 26.4. Those figures mix their G6 and Power seasons, so treat them as rough.

### G6 drops
- **Miami (OH): 11.3 to 8.8** and **North Texas: 12.0 to 10.3** are the only G6 programs with a real drop.
- Likely reason (my interpretation, not verified): both reached conference title games, and the G6 title game plus the auto-bid for the best G6 champion mattered more in the 12-team format.

The rest of the G6 sits near zero in both formats.

---

## 7. Matchups that change the most (Power games; game score, 12-team to 24-team)
These are games with at least one Power team that exist in both formats. The title games, which exist only in the 12-team format, are covered in section 4. Games are written "visitor at host".

### Gain the most under 24 teams
| Season | Game | 12-team | 24-team | Likely reason (my interpretation, not verified) |
|---|---|---|---|---|
| 2022 | Michigan at Ohio State | 41 | **100** | Decides the conference champion, with no title game as a backstop, plus a 0.4 rivalry bonus |
| 2022 | Mississippi State at Ole Miss | 27 | **100** | Egg Bowl with bubble and conference stakes |
| 2021 | Oregon at Utah | 44 | **100** | Conference title race |
| 2023 | Oregon State at Oregon | 40 | 94 | Rivalry plus conference stakes |
| 2025 | Virginia Tech at Virginia | 30 | 87 | Conference title race |
| 2022 | Florida at Florida State | 32 | 82 | Bubble stakes |
| 2023 | Utah at Arizona | 1 | 79 | Went from irrelevant to a conference title race |
| 2025 | Pittsburgh at Georgia Tech | 30 | 78 | Bubble/conference race |
| 2021 | Texas A&M at LSU | 19 | 69 | Bubble |
| 2025 | Virginia at Duke | 16 | 67 | Conference race |
| 2023 | Washington at Oregon State | 10 | 62 | Went from low-stakes to a conference race |
| 2024 | Missouri at South Carolina | 1 | 51 | Went from nothing to a bubble game |
| 2024 | Oklahoma at LSU | 0 | 50 | Same |
| 2022 | UCLA at California | 0 | 50 | Same |

**Script hooks:** *"Michigan at Ohio State scores 41 today. With no title game and a wide playoff, it's a 100."* And: *"UCLA at Cal in 2022 scored 0 out of 100. In a 24-team playoff it's a 50."*

### Lose the most under 24 teams
| Season | Game | 12-team | 24-team | Likely reason (my interpretation, not verified) |
|---|---|---|---|---|
| 2025 | USC at Oregon | 66 | 12 | Both teams much safer |
| 2023 | TCU at Oklahoma | 53 | 2 | Oklahoma's season no longer on the line |
| 2023 | Missouri at Arkansas | 62 | 16 | Same |
| 2025 | Alabama at Auburn | 89 | 45 | Bye race matters less with 8 byes |
| 2023 | Penn State at Michigan State | 47 | 3 | Playoff stakes gone |
| 2021 | Iowa at Nebraska | 64 | 21 | Same |
| 2024 | Tennessee at Vanderbilt | 60 | 18 | Safe seeds, so less to lose |
| 2024 | Tennessee at Georgia | 91 | 54 | Safe seeds, so less to lose |
| 2023 | Oklahoma at BYU | 42 | 5 | Playoff stakes gone |
| 2023 | Notre Dame at Clemson | 39 | 2 | Playoff-lock game |
| 2025 | LSU at Oklahoma | 44 | 7 | Same |

**Script hook:** *"Notre Dame at Clemson in 2023 was a 39. With 24 teams, it drops to 2."*

### Biggest games in each format
- **12-team:** the 4-5 Power title games each year (75-100 each; Georgia-LSU 2022, Iowa-Michigan 2021, Washington-Oregon 2023 and others hit 100), then regular-season games like Tennessee at Georgia 2024 (91) and Alabama at Auburn 2025 (89).
- **24-team:** Michigan at Ohio State 2022 and 2023 (100 each), Oklahoma-Oklahoma State 2021 (100), Oregon at Utah 2021 (100), Mississippi State at Ole Miss 2022 (100), Oregon State at Oregon 2023 (94), Texas-Oklahoma 2021 (90).

---

## 8. Caveats to say out loud (or at least know)
1. **Results are model outputs, not facts.** They depend on the weights (1.0 / 0.75 / 0.4, rivalry up to 0.4), the selector (resume weight 0.5, opponent adjustment 0.25) and the bracket I picked. I have not tested how sensitive they are. A sensitivity pass is the most important next step.
2. **The selector is not the committee.** The resume is a simple formula (opponent-adjusted wins and losses), not a full strength-of-schedule model. Moving from a rating-heavy to a resume-heavy selector left the main conclusions the same (24-team is ahead in all five seasons), but it changed which teams gain and lose.
3. **The Power filter is a choice.** I counted Notre Dame as Power, counted the Pac-12 only in 2021-2023, and counted every game with at least one Power team (including games against G6 and FCS opponents; about 14% of all games involve an FCS opponent and most score near zero). Excluding those would raise both formats' averages.
4. **The rivalry scale matters a lot.** At up to 0.4 per team, a pure rivalry game scores up to 40 even with no other stakes, which is a large share of the scale. The list and values are my judgment.
5. **The 24-team format isn't finalized.** I used your rules (top 8 byes, Power champions auto-bid, best G6 champion, no title games). If those rules change, the numbers will change.
6. **Fanbase numbers are unverified**, and the fan counts depend on them. Fans are counted per team they follow, so the totals double count people. The "better off / worse off" call uses a 2-point threshold, which is a judgment call. A few Power teams are not in the published top 65 and use the 0.2M default.
7. **The same 2025 fanbase numbers are used for all five seasons.**
8. **SP+ ratings are end-of-season values**, a mild hindsight leak into the selector's rating factor. Elo is as of each week.
9. **12-team results for 2021-2023 are hypothetical** (the real playoff was 4 teams).
10. **Only the CFP and conference title games are scored.** Other bowl games are ignored in both formats.
11. **The playoff brackets and fields are simplified.** Fixed seeding, Elo-based win odds. Since every playoff game is a flat 100, bracket details only change *which* games exist, not their scores.
12. **Simulation noise.** 10,000 sims per week; a team's odds can wobble by a point or two. Games where one side wins fewer than 10 of the 10,000 simulations are scored 0.

---

## 9. Open questions for the script
- **Headline stat:** probably "the median Power game goes from 4.6 to 13.3 out of 100" or "the average Power game score goes from 12.2 to 16.2 (and 14.1 to 19.9 with playoffs)."
- **Fan story:** "About 1.6 Power fans are better off for every 1 who is worse off, but in 2023 it was slightly the other way." The losers are Alabama, Georgia, Penn State, Notre Dame and Oregon.
- Do we want a 12-team vs 24-team bracket visual for 2025 (who gets in under each)?
- Should the rivalry scale be softened? Right now a rivalry game alone can be worth 40.
- Do we want a sensitivity table (different weights, with and without the bye term, different resume weights) before publishing?

---

## 10. The 2026 season so far (through week 6; week 7 just starting)
Data pulled from CFBD on 2026-10-16. The 2026 season is still a 12-team playoff; the 24-team numbers show what the same games would mean under the 2027 format.
### How meaningful has 2026 been?
Weeks 1-6, all games, using the same scale as the rest of this document (the 12-team numbers have no title games yet, since none have been played):

| | 12-team | 24-team |
|---|---|---|
| Average game score | **5.6** | **9.6** |
| Median game | 1.0 | 4.8 |
| Games scoring under 5 | 71% | 51% |
| Games scoring 25+ | 24 | 47 |

For **Power games only** (any game with a Power team, 254 so far): 7.6 in the 12-team format vs 12.6 in the 24-team format, median 2.1 vs 11.0, and 64% vs 34% of games under 5.

**Compared with the first six weeks of 2021-2025** (Power games): the 12-team average has ranged from 7.0 to 8.9 and the 24-team average from 11.4 to 14.8. 2026 (7.6 and 12.6) sits near the low end for the 12-team format and in the lower-middle for the 24-team format. **The early season has been a low-stakes one, and a 24-team playoff would have roughly doubled the number of games that matter.**

### Notable game scores so far (Power games)
Biggest games, 12-team to 24-team score (visitor at host):

| Week | Game | 12-team | 24-team |
|---|---|---|---|
| 6 | Texas-Oklahoma (Red River) | 62 | 66 |
| 3 | LSU at Ole Miss | 49 | 52 |
| 5 | Ohio State at Iowa | 45 | 38 |
| 6 | Georgia at Alabama | 43 | 42 |
| 4 | Texas A&M at LSU | 35 | 45 |
| 2 | Iowa State at Iowa | 33 | 49 |

Games that would have meant far more under a 24-team playoff:

| Week | Game | 12-team | 24-team |
|---|---|---|---|
| 3 | SMU at Louisville | 19 | **45** |
| 6 | USC at Penn State | 13 | 40 |
| 4 | Wake Forest at Louisville | 11 | 36 |
| 4 | Wisconsin at Penn State | 14 | 35 |
| 5 | Florida at Missouri | 9 | 35 |
| 5 | Penn State at Northwestern | 7 | 31 |
| 6 | Houston at Kansas State | 4 | 26 |
| 5 | Pittsburgh at Virginia Tech | 3 | 26 |

Games that mattered less under 24 teams: Ohio State at Texas in week 2 (26 to 12), Central Michigan at Miami (25 to 12), Ohio State at Iowa (45 to 38). These are the same pattern as in the five full seasons: safe contenders have less to lose.

### Teams basically out of the 12-team race but alive in a 24-team field
The model's chance of making the playoff from right now (10,000 simulations of the rest of the season; Power teams). A "basically out" team has under 5% in the 12-team format.

| Team | Record | Playoff odds, 12-team | Playoff odds, 24-team |
|---|---|---|---|
| SMU (ACC) | 4-1 | 4.5% | **47%** |
| Wisconsin (Big Ten) | 4-1 | 3.7% | **43%** |
| Arizona (Big 12) | 5-1 | 3.1% | **41%** |
| Northwestern (Big Ten) | 4-1 | 2.3% | 22% |
| Baylor (Big 12) | 4-1 | 1.6% | 19% |
| Louisville (ACC) | 3-3 | 0.4% | 18% |
| Michigan (Big Ten) | 3-2 | 0.4% | 17% |
| Pittsburgh (ACC) | 5-1 | 0.5% | 16% |
| Kentucky (SEC) | 5-1 | 0.7% | 13% |
| Penn State (Big Ten) | 3-3 | 0.0% | 13% |

**Long shots in the 12-team format that become favorites under 24 teams:** USC (6-1, 31% to 93%), BYU (5-0, 38% to 87%), Iowa (5-1, 42% to 87%), Ole Miss (4-1, 23% to 78%), UCLA (5-0, 26% to 77%), Missouri (5-1, 13% to 76%), Oregon (3-2, 23% to 73%), LSU (4-2, 18% to 70%).

**Season-level picture:** 46 of the 68 Power teams (68%) are already under 5% in the 12-team format, compared with 32 (47%) in the 24-team format. Teams that are genuinely alive but uncertain (between 5% and 95%) number 18 in the 12-team format and 27 in the 24-team format.

**Teams in good shape either way:** Notre Dame (6-0), Georgia (6-0), Indiana (6-0), Miami (5-0), Ohio State (5-1) and Texas Tech (5-0) are all at 85% or higher in the 12-team format. Utah, Alabama and Texas are next at 74-85%.

**How to read these numbers:** a 5-1 team at 3% in the 12-team format looks harsh. The model counts each team's whole schedule so far, including the quality of its opponents, and a team like Arizona or Pittsburgh has not yet beaten many strong opponents. A real committee might be more generous, or less. Treat the 24-team odds as "alive", not as predictions.

### Upcoming games (weeks 7-9, Power games)
Biggest games coming up (visitor at host):

| Week | Game | 12-team | 24-team |
|---|---|---|---|
| 7 | Alabama at Tennessee | 62 | 64 |
| 7 | Florida State at Miami | 48 | 50 |
| 7 | Ohio State at Indiana | 47 | 44 |
| 9 | Ohio State at USC | 46 | 30 |
| 9 | Florida at Georgia | 45 | 54 |
| 8 | Ole Miss at Texas | 41 | 29 |
| 7 | Utah at Colorado | 40 | 34 |
| 7 | Auburn at Georgia | 39 | 45 |

Games that would gain the most under a 24-team playoff:

| Week | Game | 12-team | 24-team |
|---|---|---|---|
| 7 | Penn State at Michigan | 16 | **46** |
| 7 | Wisconsin at UCLA | 18 | 43 |
| 7 | Nebraska at Oregon | 21 | 42 |
| 9 | Northwestern at Oregon | 17 | 37 |
| 7 | Mississippi State at LSU | 10 | 30 |
| 7 | Kentucky at Oklahoma | 5 | 27 |
| 8 | Oklahoma at Mississippi State | 5 | 23 |
| 7 | Virginia at SMU | 5 | 23 |

Games that would lose the most: Ohio State at USC (46 to 30), Notre Dame at BYU (29 to 14), Ole Miss at Texas (41 to 29), Utah at Cincinnati (23 to 16).

### Caveats specific to 2026
- **The season is in progress:** the numbers are a snapshot after six weeks. Week 7 has only 10 games played, and those are treated as results.
- **No title games are scheduled yet:** I assumed one title game per conference with 10 or more teams (Big Ten, SEC, Big 12, ACC, AAC, MAC, Mountain West, Sun Belt, Conference USA); the new Pac-12 (8 teams) is decided by record. The Pac-12 is treated as non-Power in 2026, so it competes for the G6 auto-bid in the 24-team model.
- **Ratings:** for unplayed games without a betting line, win probability uses each team's current Elo.
- **Probabilities will move a lot** over the next few weeks. All the general caveats in section 8 still apply.
