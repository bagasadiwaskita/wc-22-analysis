# FIFA World Cup Qatar 2022 Analysis

<p align="center">
<img width=50% height=50% src="https://digitalhub.fifa.com/transform/cc8d9b5b-18a8-4d34-9427-657dd2725e7f/small_icon-wc-selected?io=transform:fill&quality=75">
</p>

FIFA World Cup Qatar 2022 had completed with Argentina as the champions of the competition. Argentina crowned as the champions after the intense final match against the defending champions, France, which ended in Argentina winning on penalties. Apart from that, there are many other facts to discuss about this year's world cup. On this occasion, I would like to analyze about all participated teams' data leading up to the World Cup 2022 compared to their placement in the competition.

## Analysis Plan

Given historical data leading up to the World Cup 2022, I would like to determine which countries are underperformed or overachieved in the World Cup 2022. To achieve the goals, my analysis focused into data about all participated teams' **FIFA Ranking**, **squads**, and **recent international match results**.

The dataset I used for this analysis is from [Maven Analytics](https://www.mavenanalytics.io/data-playground).

## Data Preparation

There are many tables in the World Cup Dataset. To make it easier to analyze, I will join all data used for analysis in 1 table. The tool I used on this step is ***MySQL Workspace*** in ***[sqliteonline.com](https://sqliteonline.com/)*** and ***Python*** in ***Jupyter Notebook***.

### 1. FIFA Ranking

FIFA Ranking (in this context is FIFA Men's World Ranking) is a ranking system by FIFA for men's national teams in association football. The national teams of the men's member nations of FIFA are ranked based on ther game result with the most successful teams being ranked highest.

Table that contains FIFA Ranking values is *[2022_world_cup_groups.csv](https://github.com/bagasadiwaskita/wc-22-analysis/blob/4ed12b5e4bcb603c9e448a49eaf9221c535e38c0/World%20Cup%20Dataset%20(Original)/2022_world_cup_groups.csv)*. I rename the table into *wc22_groups.csv* to simplify the name. Other than that, no changes needed. I used SQL on this step since it is pretty straghtforward.
```
SELECT * FROM wc22_groups;
```
The result of this step is *[wc22_groups.csv](https://github.com/bagasadiwaskita/wc-22-analysis/blob/ffdc2b1032c40c2deb6c66c9c13b6ec0f2418ee0/Pre-processing/wc22_groups.csv)*.

### 2. Squads

There are a lot of information in team squad's data, such as player's name, position he plays, age, etc. In this step, I will use team's *average of player's age, caps, goals, and goals per caps*.

Table that contains squads details is *[2022_world_cup_squads.csv](https://github.com/bagasadiwaskita/wc-22-analysis/blob/4ed12b5e4bcb603c9e448a49eaf9221c535e38c0/World%20Cup%20Dataset%20(Original)/2022_world_cup_squads.csv)*. I rename the table into *wc22_squads.csv* to simplify the name. To get the data I needed, I have to create SQL query that:

1. create new column in the table named *GoalsPerCaps* that counts every player's goals per caps,
2. show the table of all participated teams with their values of average of age, caps, goals, and goals per caps.
```
-- Create new column named 'GoalsPerCaps'
ALTER TABLE wc22_squads ADD COLUMN GoalsPerCaps FLOAT;

-- Update the value of 'GoalsPerCaps' column
-- Use IFNULL and NULLIF func. to avoid divide by zero error
UPDATE wc22_squads SET GoalsPerCaps=IFNULL(Goals/NULLIF(Caps,0),0);

-- Show the table of teams with their squads info average
-- I will use round 4 decimal
SELECT DISTINCT Team,
       ROUND(AVG(Age),4) AS Avg_Age,
       ROUND(AVG(Caps),4) AS Avg_Caps,
       ROUND(AVG(Goals),4) AS Avg_Goals,
       ROUND(AVG(GoalsPerCaps),4) AS Avg_GoalsPerCaps
FROM wc22_squads GROUP BY Team;
```
The result of this step is *[wc22_squads.csv](https://github.com/bagasadiwaskita/wc-22-analysis/blob/ffdc2b1032c40c2deb6c66c9c13b6ec0f2418ee0/Pre-processing/wc22_squads.csv)*.

### 3. Recent International Matches Results

Football match in general is the main showdown of football to show which team is stronger at the moment, so it is impossible to ignore international matches results to look which national team is stronger than the others. That means **recent international matches results is one of the main index of team's strength**.

Table that contains international matches details is *[international_matches.csv](https://github.com/bagasadiwaskita/wc-22-analysis/blob/9c26a0324084f72e5264f99c26d22bda97038a14/World%20Cup%20Dataset%20(Original)/international_matches.csv)*. To collect the needed data, I used Python in this step since it would be too difficult if I did it in SQL.

Details about what I do in this step is in *[intl_matches_summary.ipynb](https://github.com/bagasadiwaskita/wc-22-analysis/blob/20dfbe8bd318553ca3c0a1e994b5c3cfc8bbf8ae/Pre-processing/intl_matches_summary.ipynb)* and the result of this step is *[intl_matches_summary.csv](https://github.com/bagasadiwaskita/wc-22-analysis/blob/20dfbe8bd318553ca3c0a1e994b5c3cfc8bbf8ae/Pre-processing/intl_matches_summary.csv)*.

### 4. Joining the Table and Show the Main Index of Team Strength

Since the needed data is collected, I have to create SQL query that:

1. join all 3 tables I've got before,
2. show the data related to team's strength.

I decided that I would show **the group, team name, FIFA Ranking, team's average of age, goals, caps, goals per caps, recent matches' goals scored per match, goals conceded per match, win rate, win streak, and unbeaten streak**.
