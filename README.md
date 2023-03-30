# FIFA World Cup Qatar 2022 Analysis

<p align="center">
<img width=50% height=50% src="https://digitalhub.fifa.com/transform/cc8d9b5b-18a8-4d34-9427-657dd2725e7f/small_icon-wc-selected?io=transform:fill&quality=75">
</p>

FIFA World Cup Qatar 2022 had completed with Argentina as the champions of the competition. Argentina crowned as the champions after the intense final match against the defending champions, France, which ended in Argentina winning on penalties. Apart from that, there are many other facts to discuss about this year's world cup. On this occasion, I would like to analyse about all participated teams' data leading up to the World Cup 2022 compared to their placement in the competition.

## Analysis Plan

Given historical data leading up to the World Cup 2022, I would like to determine which countries are underperformed or overachieved in the World Cup 2022. **I determine the underperformed team is a strong condender team in more than half of all the main units to measure World Cup 2022 team participants' strength but ended up losing in the group stage of World Cup 2022. I also determine the overachieved team is a weak condender team in more than half of all the main units to measure World Cup 2022 team participants' strength but reach at least the quarter finals of World Cup 2022.** To achieve the goals, my analysis focused into data about all participated teams' **FIFA Ranking**, **squads**, and **recent international match results**.

The dataset I used for this analysis is from [Maven Analytics](https://www.mavenanalytics.io/data-playground).

## Data Pre-processing

There are many tables in the World Cup Dataset. To make it easier to analyse, I will join all data used for analysis in 1 table. The tool I used on this step is ***MySQL Workspace*** in ***[sqliteonline.com](https://sqliteonline.com/)*** and ***Python*** in ***Jupyter Notebook***.

### 1. FIFA Ranking

FIFA Ranking (in this context is FIFA Men's World Ranking) is a ranking system by FIFA for men's national teams in association football. The national teams of the men's member nations of FIFA are ranked based on their game result with the most successful teams being ranked highest.

Table that contains FIFA Ranking values is *[2022_world_cup_groups.csv](https://github.com/bagasadiwaskita/wc-22-analysis/blob/4ed12b5e4bcb603c9e448a49eaf9221c535e38c0/World%20Cup%20Dataset%20(Original)/2022_world_cup_groups.csv)*. I rename the table into *wc22_groups.csv* to simplify the name. Other than that, no changes needed. I used SQL on this step since it is pretty straghtforward.
```
SELECT * FROM wc22_groups;
```
The result of this step is *[wc22_groups.csv](https://github.com/bagasadiwaskita/wc-22-analysis/blob/ffdc2b1032c40c2deb6c66c9c13b6ec0f2418ee0/Pre-processing/wc22_groups.csv)*.

### 2. Squads

There are a lot of information in team squad's data, such as player's name, position he plays, age, etc. In this step, I will get information about team's *average of player's age, caps, goals, and goals per caps*.

Table that contains squads details is *[2022_world_cup_squads.csv](https://github.com/bagasadiwaskita/wc-22-analysis/blob/4ed12b5e4bcb603c9e448a49eaf9221c535e38c0/World%20Cup%20Dataset%20(Original)/2022_world_cup_squads.csv)*. I rename the table into *wc22_squads.csv* to simplify the name. To get the data I needed, I have to create SQL query that show the table of all participated teams with their values of average of age, caps, goals, and goals per caps.
```
-- I will use round 4 decimal
SELECT DISTINCT Team,
       ROUND(AVG(Age),4) AS Avg_Age,
       ROUND(AVG(Caps),4) AS Avg_Caps,
       ROUND(AVG(Goals),4) AS Avg_Goals,
       ROUND((AVG(Goals) / AVG(Caps)),4) AS Avg_GoalsPerCaps
FROM wc22_squads GROUP BY Team;
```
The result of this step is *[wc22_squads.csv](https://github.com/bagasadiwaskita/wc-22-analysis/blob/591e4f616557aa0f0ff4bab060a1fe642b2bba57/Pre-processing/wc22_squads.csv)*.

### 3. Recent International Matches Results

Football match in general is the main showdown of football to show which team is stronger at the moment, so it is impossible to ignore international matches results to look which national team is stronger than the others. That means recent international matches results could be a tool to measure football team's strength.

Table that contains international matches details is *[international_matches.csv](https://github.com/bagasadiwaskita/wc-22-analysis/blob/9c26a0324084f72e5264f99c26d22bda97038a14/World%20Cup%20Dataset%20(Original)/international_matches.csv)*. To collect the needed data, I used Python in this step since it would be too difficult if I did it in SQL.

Details about what I do in this step is in *[intl_matches_summary.ipynb](https://github.com/bagasadiwaskita/wc-22-analysis/blob/591e4f616557aa0f0ff4bab060a1fe642b2bba57/Pre-processing/intl_matches_summary.ipynb)* and the result of this step is in *[intl_matches_summary.csv](https://github.com/bagasadiwaskita/wc-22-analysis/blob/591e4f616557aa0f0ff4bab060a1fe642b2bba57/Pre-processing/intl_matches_summary.csv)*.

### 4. Joining the Table and Show the Data Related to Team Strength

Since the needed data is already collected, I have to create SQL query that:

1. join all 3 tables I've got before,
2. show the data related to team strength.

I decided that I would show **the group, team name, FIFA Ranking, team's average of age, goals, caps, goals per caps, recent matches' goals scored per match, goals conceded per match, win rate, win streak, and unbeaten streak**.
```
SELECT groups.Group, groups.Team, groups.FIFA_Ranking,
       squads.Avg_Age, squads.Avg_Caps, squads.Avg_Goals, squads.Avg_GoalsPerCaps,
       matches.Win_Rate_Percentage, matches.Goals_Scored_per_Match,
       matches.Goals_Conceded_per_Match, matches.Current_Win_Streak, matches.Longest_Win_Streak,
       matches.Current_Unbeaten_Streak, matches.Longest_Unbeaten_Streak
FROM wc22_groups AS groups
INNER JOIN wc22_squads AS squads ON groups.Team = squads.Team
INNER JOIN intl_matches_summary AS matches ON groups.Team = matches.Team;
```
The result of this step is *[wc22_final_table.csv](https://github.com/bagasadiwaskita/wc-22-analysis/blob/591e4f616557aa0f0ff4bab060a1fe642b2bba57/Pre-processing/wc22_final_table.csv)*.

## Analysis with Visualization

In this section, I will analyze all the information from *[wc22_final_table.csv](https://github.com/bagasadiwaskita/wc-22-analysis/blob/591e4f616557aa0f0ff4bab060a1fe642b2bba57/Pre-processing/wc22_final_table.csv)*. The goal in this step is to determine which aspect that can be used as the main units to measure World Cup 2022 team participants' strength. After that, we decide the strong contender and weak contender team based on that aspect.

### 1. FIFA Ranking of the Team

Since FIFA Ranking calculation is based on the game result directly, that means FIFA Ranking can determine the strength of the team at the moment. Therefore, **I decided to use FIFA Ranking as one of the main units to measure World Cup 2022 team participants' strength.**

Here is the distribution of FIFA Ranking among all World Cup 2022 participant.

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/ece0133891095d53095774353438768bc4567799/Viz/FIFA%20Ranking%20Group%20Stage.png"> | <img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/ece0133891095d53095774353438768bc4567799/Viz/FIFA%20Ranking.png">
</p>

From the pictures above, we could expect that the top 2 in each group would make it into knockout stage. We also could expect that higher ranked teams would likely get a higher placement in the World Cup 2022.

Therefore, **I decide that the criteria of strong contender team based on FIFA Ranking is they are on top of their group or top 8 overall. I also decide that the criteria of weak contender team based on FIFA Ranking is they are on bottom of their group or bottom 8 overall.**

### 2. Average Age of Football Players Each Team

Age sometimes could means something for football players. From common people's point of view, older football players considered not as agile as the younger ones but their experience is definitely a plus point for them. Since there is no clear boundaries to determine which one is better between older or younger football player, **I decided to NOT use age distribution as one of the main units to measure World Cup 2022 team participants' strength.**

Let's take a look on how is the average of age at all football players participated in the World Cup 2022 grouped by their team.

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/ece0133891095d53095774353438768bc4567799/Viz/Average%20Age.png">
</p>

From the chart above, we could see that Ghana, United States, Ecuador, and Spain bring many young football players. We could also see that Iran, Mexico, Tunisia, and Argentina bring many old football players.

### 3. Average Caps of Football Players Each Team

### 4. Average Goals of Football Players Each Team

### 5. Average Goals per Aevrage Caps of the Team

### 6. Team's Win Rate of International Matches in 4 Years

### 7. Team's Goal Scored per International Matches in 4 Years

### 8. Team's Goal Conceded per International Matches in 4 Years

### 9. Team's Win Streak on International Matches in 4 Years

### 10. Team's Unbeaten Streak on International Matches in 4 Years
