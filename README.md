# FIFA World Cup Qatar 2022 Analysis

<p align="center">
<img width=50% height=50% src="https://digitalhub.fifa.com/transform/cc8d9b5b-18a8-4d34-9427-657dd2725e7f/small_icon-wc-selected?io=transform:fill&quality=75">
</p>

FIFA World Cup Qatar 2022 had done with Argentina as the champions of the competition. Argentina crowned as the champions after the intense final match against the defending champions, France, which ended in Argentina winning on penalties. Apart from that, there are many other facts to discuss about this year's world cup. On this occasion, I would like to analyze about all participated teams' data leading up to the World Cup 2022 compared to their placement in the competition.

## Analysis Plan

Given historical data leading up to the World Cup 2022, I would like to determine which countries are underperformed or overachieved in the World Cup 2022. To achieve the goals, my analysis focused into data about all participated teams' **FIFA Ranking**, **squads**, and **recent international match results**.

The dataset I used for this analysis is from [Maven Analytics](https://www.mavenanalytics.io/data-playground).

## Data Preparation

There are many tables in the World Cup Dataset. To make it easier to analyze, I will join all data used for analysis in 1 table. The tool I used on this step is ***MySQL Workspace*** in [sqliteonline.com](https://sqliteonline.com/).

### 1. FIFA Ranking

FIFA Ranking (in this context is FIFA Men's World Ranking) is a ranking system by FIFA for men's national teams in association football. The national teams of the men's member nations of FIFA are ranked based on ther game result with the most successful teams being ranked highest. That means FIFA Ranking is one of the main measurement of team's strength.

Table that contains FIFA Ranking values is *2022_world_cup_groups.csv*. I rename the table into *wc22_groups.csv* to create the naming convention for this project. Other than that, no changes needed. I used SQL on this step since it is pretty straghtforward.
```
SELECT * FROM wc22_groups;
```

### 2. Squads

There are a lot of information in team squad's data, such as player's name, position he plays, age, etc. In this step, I will use team's *average of player's age, caps, goals, and goals per caps*. I also decided that team's average of player's goals per caps is one of the main measurement of team's strength, since it can shows how is the team's goal productivity.

Table that contains squads details is *2022_world_cup_squads.csv*. I rename the table into *wc22_squads.csv* to keep the naming convention consistent. To get the data I needed, I have to create SQL Query that:

- create new column in the table named *GoalsPerCaps* that counts every player's goals per caps,
- show the table of all participated teams with their values of average of age, caps, goals, and goals per caps.
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

### 3. Recent International Matches Results
