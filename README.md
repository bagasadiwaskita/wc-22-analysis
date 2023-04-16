# FIFA World Cup Qatar 2022 Analysis

<p align="center">
<img width=50% height=50% src="https://digitalhub.fifa.com/transform/cc8d9b5b-18a8-4d34-9427-657dd2725e7f/small_icon-wc-selected?io=transform:fill&quality=75">
</p>

FIFA World Cup Qatar 2022 had completed with Argentina as the champions of the competition. Argentina crowned as the champions after the intense final match against the defending champions, France, which ended in Argentina winning on penalties. Apart from that, there are many other facts to discuss about this year's world cup. On this occasion, I would like to analyse about all participated teams' data leading up to the World Cup 2022 compared to their placement in the competition.

## Analysis Plan

Given historical data leading up to the World Cup 2022, I would like to determine which countries are underperformed or overachieved in the World Cup 2022. **I determine the underperformed team is a strong condender team in more than half of all the main units to measure World Cup 2022 team participants' strength but ended up losing in the group stage of World Cup 2022. I also determine the overachieved team is a weak condender team in more than half of all the main units to measure World Cup 2022 team participants' strength but reach at least the quarter finals of World Cup 2022.** To achieve the goals, my analysis focused into data about all participated teams' **FIFA Ranking**, **squads**, and **recent international match results**.

The dataset I used for this analysis is from [Maven Analytics](https://www.mavenanalytics.io/data-playground).

## Data Pre-processing

There are many tables in the World Cup Dataset. To make it easier to analyse, I will join all data used for analysis in 1 table. The tool I used on this step is ***MySQL/MariaDB Workspace*** in ***[sqliteonline.com](https://sqliteonline.com/)*** and ***Python*** in ***Jupyter Notebook***.

### 1. FIFA Ranking

FIFA Ranking (in this context is FIFA Men's World Ranking) is a ranking system by FIFA for men's national teams in association football. The national teams of the men's member nations of FIFA are ranked based on their game result with the most successful teams being ranked highest.

Table that contains FIFA Ranking values is *[2022_world_cup_groups.csv](https://github.com/bagasadiwaskita/wc22-analysis/blob/46eab7adc5e68c4a98e893f536a474111199b30c/World%20Cup%20Dataset%20(Original)/2022_world_cup_groups.csv)*. I rename the table into *wc22_groups.csv* to simplify the name. Other than that, no changes needed. I used SQL on this step.
```
SELECT * FROM wc22_groups;
```
The result of this step is *[wc22_groups.csv](https://github.com/bagasadiwaskita/wc22-analysis/blob/46eab7adc5e68c4a98e893f536a474111199b30c/Pre-processing/wc22_groups.csv)*.

### 2. Squads

There are a lot of information in team squad's data, such as player's name, position he plays, age, etc. In this step, I will get information about team's *average of player's age, caps, goals, and goals per caps*.

Table that contains squads details is *[2022_world_cup_squads.csv](https://github.com/bagasadiwaskita/wc22-analysis/blob/46eab7adc5e68c4a98e893f536a474111199b30c/World%20Cup%20Dataset%20(Original)/2022_world_cup_squads.csv)*. I rename the table into *wc22_squads.csv* to simplify the name. To get the data I needed, I have to create SQL query that show the table of all participated teams with their values of average of age, caps, goals, and goals per caps.
```
-- I will use round 4 decimal
SELECT DISTINCT Team,
       ROUND(AVG(Age),4) AS Avg_Age,
       ROUND(AVG(Caps),4) AS Avg_Caps,
       ROUND(AVG(Goals),4) AS Avg_Goals,
       ROUND((AVG(Goals) / AVG(Caps)),4) AS Avg_GoalsPerCaps
FROM wc22_squads GROUP BY Team;
```
The result of this step is *[wc22_squads.csv](https://github.com/bagasadiwaskita/wc22-analysis/blob/46eab7adc5e68c4a98e893f536a474111199b30c/Pre-processing/wc22_squads.csv)*.

### 3. Recent International Matches Results

Football match in general is the main showdown of football to show which team is stronger at the moment, so it is impossible to ignore international matches results to look which national team is stronger than the others. That means recent international matches results could be a tool to measure football team's strength.

Table that contains international matches details is *[international_matches.csv](https://github.com/bagasadiwaskita/wc22-analysis/blob/46eab7adc5e68c4a98e893f536a474111199b30c/World%20Cup%20Dataset%20(Original)/international_matches.csv)*. To collect the needed data, I used Python in this step since it would be too difficult if I did it in SQL.

Details about what I do in this step is in *[intl_matches_summary.ipynb](https://github.com/bagasadiwaskita/wc22-analysis/blob/46eab7adc5e68c4a98e893f536a474111199b30c/Pre-processing/intl_matches_summary.ipynb)* and the result of this step is in *[intl_matches_summary.csv](https://github.com/bagasadiwaskita/wc22-analysis/blob/46eab7adc5e68c4a98e893f536a474111199b30c/Pre-processing/intl_matches_summary.csv)*.

### 4. Joining the Table and Show the Data Related to Team Strength

Since the needed data is already collected, I have to create SQL query that:

1. join all 3 tables I've got before,
2. show the data related to team strength.

I decided that I would show **the group, team name, FIFA Ranking, team's average of age, goals, caps, goals per caps, recent matches' goals scored per match, goals conceded per match, win rate, win streak, unbeaten streak, winless streak, and lose streak**.
```
SELECT groups.Group, groups.Team, groups.FIFA_Ranking,
       squads.Avg_Age, squads.Avg_Caps, squads.Avg_Goals, squads.Avg_GoalsPerCaps,
       matches.Win_Rate_Percentage, matches.Goals_Scored_per_Match,
       matches.Goals_Conceded_per_Match, matches.Current_Win_Streak, matches.Longest_Win_Streak,
       matches.Current_Unbeaten_Streak, matches.Longest_Unbeaten_Streak,
       matches.Current_Winless_Streak, matches.Longest_Winless_Streak, matches.Current_Lose_Streak,
       matches.Longest_Lose_Streak
FROM wc22_groups AS groups
INNER JOIN wc22_squads AS squads ON groups.Team = squads.Team
INNER JOIN intl_matches_summary AS matches ON groups.Team = matches.Team;
```
The result of this step is *[wc22_final_table.csv](https://github.com/bagasadiwaskita/wc22-analysis/blob/46eab7adc5e68c4a98e893f536a474111199b30c/Pre-processing/wc22_final_table.csv)*.

## Analysis with Visualization

In this section, I will analyze all the information from *[wc22_final_table.csv](https://github.com/bagasadiwaskita/wc22-analysis/blob/46eab7adc5e68c4a98e893f536a474111199b30c/Pre-processing/wc22_final_table.csv)*. The goal in this step is to determine which aspect that can be used as the main units to measure World Cup 2022 team participants' strength. After that, we decide the strong contender and weak contender team based on that aspect.

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

In sports including football, a cap is a player's appeareance in a game in international level. It means football players' cap represent the number of time a player has played for their country in an international level. It could be said that players with higher caps is more experienced that the lower ones in terms of international level matches. But high number of caps does not mean the player is good, since it only shows the number of appeareance in a match, not the performances. Since there is not much information we can take only from number of caps in terms of performances, **I decided to NOT use caps distribution as one of the main units to measure World Cup 2022 team participants' strength.**

Let's take a look on how is the average of caps at all football players participated in the World Cup 2022 grouped by their team.

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/ece0133891095d53095774353438768bc4567799/Viz/Average%20Caps.png">
</p>

From the chart above, we could see that Qatar, Belgium, Mexico, and Uruguay bring many football players with high number of caps. We could also see that Ghana, Morocco, Australia, and Cameroon bring many football players with low number of caps.

### 4. Average Goals of Football Players Each Team

It could be said that a player with higher goals performs better that the lower one. But we could not judge player's performances only from number of goals. If a player scores many goal but he plays a lot of matches with low rate of goals per match, then we couldn't consider him a good player. Since there is not much information we can take only from number of goals, **I decided to NOT use goals distribution as one of the main units to measure World Cup 2022 team participants' strength.**

Let's take a look on how is the average of goals at all football players participated in the World Cup 2022 grouped by their team.

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/ece0133891095d53095774353438768bc4567799/Viz/Average%20Goals.png">
</p>

From the chart above, we could see that Belgium, Qatar, Portugal, and France bring many football players with high number of goals. We could also see that Ghana, Saudi Arabia, Morocco, and Australia bring many football players with low number of goals.

### 5. Average Goals per Average Caps of the Team

As I said before, we could not take only from caps and goals separately to measure the team's strength. However, if we make a ratio between number of goals and number of caps, it could be a good measurement since it could shows both appeareance and performance.

From that idea, I decided to create a ratio between average number of goals and number of caps in a team. Therefore, **I decided to use average goals per average caps distribution as one of the main units to measure World Cup 2022 team participants' strength.**

Here is the distribution of average goals per average caps among all World Cup 2022 team participant.

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/ece0133891095d53095774353438768bc4567799/Viz/Average%20Goals%20per%20Average%20Caps%20Group%20Stage.png">
</p>

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/ece0133891095d53095774353438768bc4567799/Viz/Average%20Goals%20per%20Average%20Caps.png">
</p>

From the charts above, we could expect that the top 2 in each group would make it into knockout stage. We also could expect that teams with higher average goals per average caps would likely get a higher placement in the World Cup 2022.

Therefore, **I decide that the criteria of strong contender team based on average goals per average caps is they are on top of their group or top 8 overall. I also decide that the criteria of weak contender team based on average goals per average caps is they are on bottom of their group or bottom 8 overall.**

### 6. Team's Win Rate of International Matches in 4 Years

A football team's win rate is a good measurement to determine how good the performance of the team compared to the others. Therefore, **I decided to use win rate distribution as one of the main units to measure World Cup 2022 team participants' strength.**

Here is the distribution of win rate among all World Cup 2022 team participant on international matches in 4 years.

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/ece0133891095d53095774353438768bc4567799/Viz/Win%20Rate%20Group%20Stage.png">
</p>

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/ece0133891095d53095774353438768bc4567799/Viz/Win%20Rate.png">
</p>

From the charts above, we could expect that the top 2 in each group would make it into knockout stage. We also could expect that teams with higher win rate would likely get a higher placement in the World Cup 2022.

Therefore, **I decide that the criteria of strong contender team based on their win rate of international matches in 4 years is they are on top of their group or top 8 overall. I also decide that the criteria of weak contender team based on their win rate of international matches in 4 years is they are on bottom of their group or bottom 8 overall.**

### 7. Team's Goal Scored per International Matches in 4 Years

The winning condition of football match is when a team scoring the ball into the opposing team's goal more that the opponent. From goal scored stats, we could take information about the team's offensive capabilities to score goals into their opponent. Therefore, **I decided to use goal scored per match distribution as one of the main units to measure World Cup 2022 team participants' strength.**

Here is the distribution of goal scored per international match in 4 years among all World Cup 2022 team participant.

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/ece0133891095d53095774353438768bc4567799/Viz/Goals%20Scored%20per%20Match%20Group%20Stage.png">
</p>

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/ece0133891095d53095774353438768bc4567799/Viz/Goals%20Scored%20per%20Match.png">
</p>

From the charts above, we could expect that the top 2 in each group would make it into knockout stage. We also could expect that teams with higher goal scored stats would likely get a higher placement in the World Cup 2022.

Therefore, **I decide that the criteria of strong contender team based on their goal scored per international match in 4 years is they are on top of their group or top 8 overall. I also decide that the criteria of weak contender team based on their goal scored per international match in 4 years is they are on bottom of their group or bottom 8 overall.**

### 8. Team's Goal Conceded per International Matches in 4 Years

Similar to goal scored stats, we could take information about the team's defensive capabilities to prevent the opposing team to score goals into their goal from goal conceded stats. Therefore, **I decided to use goal conceded per match distribution as one of the main units to measure World Cup 2022 team participants' strength.**

Here is the distribution of goal conceded per international match in 4 years among all World Cup 2022 team participant.

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/ece0133891095d53095774353438768bc4567799/Viz/Goals%20Conceded%20per%20Match%20Group%20Stage.png">
</p>

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/ece0133891095d53095774353438768bc4567799/Viz/Goals%20Conceded%20per%20Match.png">
</p>

From the charts above, we could expect that the bottom 2 in each group would make it into knockout stage. We also could expect that teams with lower goal conceded stats would likely get a higher placement in the World Cup 2022.

Therefore, **I decide that the criteria of strong contender team based on their goal conceded per international match in 4 years is they are on bottom of their group or bottom 8 overall. I also decide that the criteria of weak contender team based on their goal conceded per international match in 4 years is they are on top of their group or top 8 overall.**

### 9. Team's Win Streak on International Matches in 4 Years

A team's win streak is the number of match that a team is winning football matches in sequence. The win streak stats could describe that the team has positive trend before the World Cup 2022 starts. Therefore, **I decided to use win streak distribution as one of the main units to measure World Cup 2022 team participants' strength.**

Here is the distribution of win streak on international matches in 4 years among all World Cup 2022 team participant.

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/80c189ab862360b782ebc2967c18e6b183ed7e33/Viz/Win%20Streak%20Group%20Stage.png">
</p>

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/80c189ab862360b782ebc2967c18e6b183ed7e33/Viz/Win%20Streak%20Group%20Stage-2.png">
</p>

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/80c189ab862360b782ebc2967c18e6b183ed7e33/Viz/Win%20Streak.png">
</p>

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/80c189ab862360b782ebc2967c18e6b183ed7e33/Viz/Win%20Streak-2.png">
</p>

From the charts above, we could expect that the top 2 in each group would make it into knockout stage. We also could expect that teams with higher number of win streak would likely get a higher placement in the World Cup 2022.

Therefore, I create **the rules to decide the strong contender teams based on win streak** according to the charts.

- For longest win streak stats,
  * a team is considered as strong contender team when it is on top of their group or has at least 9 matches in longest win streak. If there are 2 or more       teams in the top of a group share the same number of longest win streak, team with higher current win streak is considered as strong contender team. If       the tie is still on, the tied teams are considered as strong contender team.

- For current win streak stats,
  * a team is considered as strong contender team when it is on top of their group or has at least 2 matches in current win streak. If there are 2 or more       teams in the top of a group share the same number of current win streak and it is not zero, team with higher longest win streak is considered as strong       contender team. If the tie is still on, the tied teams are considered as strong contender team. If all teams in a group share the same number of current     win streak and it is zero, none of them are considered as strong contender team.

### 10. Team's Unbeaten Streak on International Matches in 4 Years

A team's unbeaten streak is the number of match that a team is not losing football matches in sequence. Similar to win streak stats, the unbeaten streak stats could describe that the team has positive trend before the World Cup 2022 starts. Therefore, **I decided to use unbeaten streak distribution as one of the main units to measure World Cup 2022 team participants' strength.**

Here is the distribution of unbeaten streak on international matches in 4 years among all World Cup 2022 team participant.

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/80c189ab862360b782ebc2967c18e6b183ed7e33/Viz/Unbeaten%20Streak%20Group%20Stage.png">
</p>

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/80c189ab862360b782ebc2967c18e6b183ed7e33/Viz/Unbeaten%20Streak%20Group%20Stage-2.png">
</p>

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/80c189ab862360b782ebc2967c18e6b183ed7e33/Viz/Unbeaten%20Streak.png">
</p>

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/80c189ab862360b782ebc2967c18e6b183ed7e33/Viz/Unbeaten%20Streak-2.png">
</p>

From the charts above, we could expect that the top 2 in each group would make it into knockout stage. We also could expect that teams with higher number of unbeaten streak would likely get a higher placement in the World Cup 2022.

Therefore, I create **the rules to decide the strong contender teams based on unbeaten streak** according to the charts.

- For longest unbeaten streak stats,
  * a team is considered as strong contender team when it is on top of their group or has at least 14 matches in longest unbeaten streak. If there are 2 or       more teams in the top of a group share the same number of longest unbeaten streak, team with higher current unbeaten streak is considered as strong           contender team. If the tie is still on, the tied teams are considered as strong contender team.

- For current unbeaten streak stats,
  * a team is considered as strong contender team when it is on top of their group or has at least 5 matches in current unbeaten streak. If there are 2 or       more teams in the top of a group share the same number of current unbeaten streak and it is not zero, team with higher longest unbeaten streak is             considered as strong contender team. If the tie is still on, the tied teams are considered as strong contender team. If all teams in a group share the       same number of current unbeaten streak and it is zero, none of them are considered as strong contender team.

### 11. Team's Winless Streak on International Matches in 4 Years

When it comes to a trend, if there is a positive trend, then there is a negative trend too. The first negative trend we analysed is winless streak. A team's winless streak is the number of match that a team is not winning football matches in sequence. The winless streak stats could describe that the team has negative trend before the World Cup 2022 starts. Therefore, **I decided to use winless streak distribution as one of the main units to measure World Cup 2022 team participants' strength.**

Here is the distribution of winless streak on international matches in 4 years among all World Cup 2022 team participant.

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/4306c8e083c8ec40f828fa47d4575ec0bc8575ae/Viz/Winless%20Streak%20Group%20Stage.png">
</p>

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/4306c8e083c8ec40f828fa47d4575ec0bc8575ae/Viz/Winless%20Streak%20Group%20Stage-2.png">
</p>

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/4306c8e083c8ec40f828fa47d4575ec0bc8575ae/Viz/Winless%20Streak.png">
</p>

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/4306c8e083c8ec40f828fa47d4575ec0bc8575ae/Viz/Winless%20Streak-2.png">
</p>

From the charts above, we could expect that the bottom 2 in each group would make it into knockout stage. We also could expect that teams with lower number of winless streak would likely get a higher placement in the World Cup 2022.

Therefore, I create **the rules to decide the weak contender teams based on winless streak** according to the charts.

- For longest winless streak stats,
  * a team is considered as weak contender team when it is on top of their group or has at least 6 matches in longest winless streak. If there are 2 or more     teams in the top of a group share the same number of longest winless streak, team with higher current winless streak is considered as weak contender         team. If the tie is still on, the tied teams are considered as weak contender team.

- For current winless streak stats,
  * a team is considered as weak contender team when it is on top of their group or has at least 2 matches in current winless streak. If there are 2 or more     teams in the top of a group share the same number of current winless streak and it is not zero, team with higher longest winless streak is considered as     weak contender team. If the tie is still on, the tied teams are considered as weak contender team. If all teams in a group share the same number of           current winless streak and it is zero, none of them are considered as weak contender team.

### 12. Team's Lose Streak on International Matches in 4 Years

A team's lose streak is the number of match that a team is losing football matches in sequence. Similar to winless streak stats, the lose streak stats could describe that the team has negative trend before the World Cup 2022 starts. Therefore, **I decided to use lose streak distribution as one of the main units to measure World Cup 2022 team participants' strength.**

Here is the distribution of lose streak on international matches in 4 years among all World Cup 2022 team participant.

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/4306c8e083c8ec40f828fa47d4575ec0bc8575ae/Viz/Lose%20Streak%20Group%20Stage.png">
</p>

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/4306c8e083c8ec40f828fa47d4575ec0bc8575ae/Viz/Lose%20Streak%20Group%20Stage-2.png">
</p>

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/4306c8e083c8ec40f828fa47d4575ec0bc8575ae/Viz/Lose%20Streak.png">
</p>

<p align="center">
<img src="https://github.com/bagasadiwaskita/wc22-analysis/blob/4306c8e083c8ec40f828fa47d4575ec0bc8575ae/Viz/Lose%20Streak-2.png">
</p>

From the charts above, we could expect that the bottom 2 in each group would make it into knockout stage. We also could expect that teams with lower number of lose streak would likely get a higher placement in the World Cup 2022.

Therefore, I create **the rules to decide the weak contender teams based on lose streak** according to the charts.

- For longest lose streak stats,
  * a team is considered as weak contender team when it is on top of their group or has at least 4 matches in longest lose streak. If there are 2 or more         teams in the top of a group share the same number of longest lose streak, team with higher current lose streak is considered as weak contender team. If       the tie is still on, the tied teams are considered as weak contender team.

- For current lose streak stats,
  * a team is considered as weak contender team when it is on top of their group or has at least 1 match in current lose streak. If there are 2 or more teams     in the top of a group share the same number of current lose streak and it is not zero, team with higher longest lose streak is considered as weak             contender team. If the tie is still on, the tied teams are considered as weak contender team. If all teams in a group share the same number of current       lose streak and it is zero, none of them are considered as weak contender team.
  
To check all the visualization by yourself, you can look at it [here](https://public.tableau.com/views/Pre-FIFAWorldCupQatar2022Analysis/FIFARankingGroupStage?:language=en-US&:display_count=n&:origin=viz_share_link).

## Interpretation: Determine the Underperform and Overachieved Team

In this section, I will determine which team is considered as underperform or overachieved in the World Cup 2022.

From the analysis section, we got 9 categories to consider both strong contender team and weak contender team. **That means, the underperformed team is a strong condender team in at least 5 main units to measure World Cup 2022 team participants' strength but ended up losing in the group stage of World Cup 2022. Furthermore, the overachieved team is a weak condender team in at least 5 main units to measure World Cup 2022 team participants' strength but reach at least the quarter finals of World Cup 2022.**

I've done the code to count how many times all teams considered strong contender team or weak contender team in *[interpretation.py](https://github.com/bagasadiwaskita/wc22-analysis/blob/8153e6259b17032cb996887fb7b8b04428cd1857/Interpretation/interpretation.py)*.

According to *[interpretation.py](https://github.com/bagasadiwaskita/wc22-analysis/blob/8153e6259b17032cb996887fb7b8b04428cd1857/Interpretation/interpretation.py)*, teams that considered as strong contender team in 5 or more main units are:

1. Netherlands
2. Iran
3. Argentina
4. Australia
5. Belgium
6. Brazil
7. South Korea

Furthermore, teams that considered as weak contender team in 5 or more main units are:

1. Qatar
2. Equador
3. Wales
4. Saudi Arabia
5. Tunisia
6. Costa Rica
7. Croatia
8. Cameroon

To define the underperformed and overachieved teams, we need to look at the placement of the teams in the FIFA World Cup Qatar 2022. The placements is implied [here](https://www.fifa.com/fifaplus/en/tournaments/mens/worldcup/qatar2022/knockout-and-groups). According to my analysis and the placements, here is the underperformed and overachieved teams.

### Underperformed Team  No. 1: Iran

### Underperformed Team  No. 2: Belgium

### Overachieved Team  No. 1: Croatia
