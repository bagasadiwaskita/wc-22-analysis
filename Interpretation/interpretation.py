#!/usr/bin/env python
# coding: utf-8

# In[42]:


# importing needed libraries
import numpy as np
import pandas as pd

# read wc22_final_table.csv
df = pd.read_csv('wc22_final_table.csv')

# create 2 new columns that count each count of strong contender and weak contender
df['Strong_Count']=0
df['Weak_Count']=0

# define some variables and functions
## var and func for FIFA_Ranking
### create vars of top 8 overall, top 1 each group, bot 8 overall, bot 1 each group based on FIFA_Ranking
top8_fifa=df['FIFA_Ranking'].nsmallest(8, keep='all').values
topg_fifa=df.groupby('Group')['FIFA_Ranking'].min().values
bot8_fifa=df['FIFA_Ranking'].nlargest(8, keep='all').values
botg_fifa=df.groupby('Group')['FIFA_Ranking'].max().values

### define functions to count strong and weak contender team based of FIFA_Ranking
def fifa_strong(x,y):
    if x<=top8_fifa.max() or x in topg_fifa:
        y=y+1
    return y

def fifa_weak(x,y):
    if x>=bot8_fifa.min() or x in botg_fifa:
        y=y+1
    return y

## var and func for Avg_GoalsPerCaps
### create vars of top 8 overall, top 1 each group, bot 8 overall, bot 1 each group based on Avg_GoalsPerCaps
top8_gpc=df['Avg_GoalsPerCaps'].nlargest(8, keep='all').values
topg_gpc=df.groupby('Group')['Avg_GoalsPerCaps'].max().values
bot8_gpc=df['Avg_GoalsPerCaps'].nsmallest(8, keep='all').values
botg_gpc=df.groupby('Group')['Avg_GoalsPerCaps'].min().values

### define functions to count strong and weak contender team based of Avg_GoalsPerCaps
def gpc_strong(x,y):
    if x>=top8_gpc.min() or x in topg_gpc:
        y=y+1
    return y

def gpc_weak(x,y):
    if x<=bot8_gpc.max() or x in botg_gpc:
        y=y+1
    return y

## var and func for Win_Rate_Percentage
### create vars of top 8 overall, top 1 each group, bot 8 overall, bot 1 each group based on Win_Rate_Percentage
top8_wr=df['Win_Rate_Percentage'].nlargest(8, keep='all').values
topg_wr=df.groupby('Group')['Win_Rate_Percentage'].max().values
bot8_wr=df['Win_Rate_Percentage'].nsmallest(8, keep='all').values
botg_wr=df.groupby('Group')['Win_Rate_Percentage'].min().values

### define functions to count strong and weak contender team based of Win_Rate_Percentage
def wr_strong(x,y):
    if x>=top8_wr.min() or x in topg_wr:
        y=y+1
    return y

def wr_weak(x,y):
    if x<=bot8_wr.max() or x in botg_wr:
        y=y+1
    return y

## var and func for Goals_Scored_per_Match
### create vars of top 8 overall, top 1 each group, bot 8 overall, bot 1 each group based on Goals_Scored_per_Match
top8_gs=df['Goals_Scored_per_Match'].nlargest(8, keep='all').values
topg_gs=df.groupby('Group')['Goals_Scored_per_Match'].max().values
bot8_gs=df['Goals_Scored_per_Match'].nsmallest(8, keep='all').values
botg_gs=df.groupby('Group')['Goals_Scored_per_Match'].min().values

### define functions to count strong and weak contender team based of Goals_Scored_per_Match
def gs_strong(x,y):
    if x>=top8_gs.min() or x in topg_gs:
        y=y+1
    return y

def gs_weak(x,y):
    if x<=bot8_gs.max() or x in botg_gs:
        y=y+1
    return y

## var and func for Goals_Conceded_per_Match
### create vars of top 8 overall, top 1 each group, bot 8 overall, bot 1 each group based on Goals_Conceded_per_Match
top8_gc=df['Goals_Conceded_per_Match'].nsmallest(8, keep='all').values
topg_gc=df.groupby('Group')['Goals_Conceded_per_Match'].min().values
bot8_gc=df['Goals_Conceded_per_Match'].nlargest(8, keep='all').values
botg_gc=df.groupby('Group')['Goals_Conceded_per_Match'].max().values

### define functions to count strong and weak contender team based of Goals_Conceded_per_Match
def gc_strong(x,y):
    if x<=top8_gc.max() or x in topg_gc:
        y=y+1
    return y

def gc_weak(x,y):
    if x>=bot8_gc.min() or x in botg_gc:
        y=y+1
    return y

## var and func for Current_Win_Streak and Longest_Win_Streak
### create vars of top 1 each group, value counts each group, and grouping with group
### based on Current_Win_Streak and Longest_Win_Streak
topg_wsc=df.groupby('Group')['Current_Win_Streak'].max()
topg_wsl=df.groupby('Group')['Longest_Win_Streak'].max()
freq_wsc_group=(df.groupby(['Group'])['Current_Win_Streak']).value_counts().to_frame(name='wsc_freq')
freq_wsl_group=(df.groupby(['Group'])['Longest_Win_Streak']).value_counts().to_frame(name='wsl_freq')
grouped_group_wsc=df.groupby(['Group','Current_Win_Streak'])
grouped_group_wsl=df.groupby(['Group','Longest_Win_Streak'])

### define functions to count strong contender team based of Current_Win_Streak
def wsc_strong(row):
    wsc_row = row['Current_Win_Streak']
    wsl_row = row['Longest_Win_Streak']
    group_row = row['Group']
    team_row = row['Team']
    
    if wsc_row>=2:
        row['Strong_Count']+=1
    elif wsc_row>=topg_wsc[row['Group']] and wsc_row!=0:
        strong = True
        if freq_wsc_group.loc[row['Group']].loc[row['Current_Win_Streak']]['wsc_freq']>1:
            ref_wsc = grouped_group_wsc.get_group((group_row,wsc_row))
            for ind in ref_wsc.index:
                group_ind = ref_wsc.loc[ind,'Group']
                team_ind = ref_wsc.loc[ind,'Team']
                wsc_ind = ref_wsc.loc[ind,'Current_Win_Streak']
                wsl_ind = ref_wsc.loc[ind,'Longest_Win_Streak']
                if group_row!=group_ind or team_row!=team_ind:
                    if wsl_row<wsl_ind:
                        strong = False
                        break
        if strong: 
            row['Strong_Count'] += 1
        
    return row

### define functions to count strong contender team based of Longest_Win_Streak
def wsl_strong(row):
    wsc_row = row['Current_Win_Streak']
    wsl_row = row['Longest_Win_Streak']
    group_row = row['Group']
    team_row = row['Team']
    
    if wsl_row>=9:
        row['Strong_Count']+=1
    elif wsl_row>=topg_wsl[row['Group']] and wsl_row!=0:
        strong = True
        if freq_wsl_group.loc[row['Group']].loc[row['Longest_Win_Streak']]['wsl_freq']>1:
            ref_wsl = grouped_group_wsl.get_group((group_row,wsl_row))
            for ind in ref_wsl.index:
                group_ind = ref_wsl.loc[ind,'Group']
                team_ind = ref_wsl.loc[ind,'Team']
                wsc_ind = ref_wsl.loc[ind,'Current_Win_Streak']
                wsl_ind = ref_wsl.loc[ind,'Longest_Win_Streak']
                if group_row!=group_ind or team_row!=team_ind:
                    if wsc_row<wsc_ind:
                        strong = False
                        break
        if strong: 
            row['Strong_Count'] += 1
        
    return row

## var and func for Current_Unbeaten_Streak and Longest_Unbeaten_Streak
### create vars of top 1 each group, value counts each group, and grouping with group
### based on Current_Unbeaten_Streak and Longest_Unbeaten_Streak
topg_ubsc=df.groupby('Group')['Current_Unbeaten_Streak'].max()
topg_ubsl=df.groupby('Group')['Longest_Unbeaten_Streak'].max()
freq_ubsc_group=(df.groupby(['Group'])['Current_Unbeaten_Streak']).value_counts().to_frame(name='ubsc_freq')
freq_ubsl_group=(df.groupby(['Group'])['Longest_Unbeaten_Streak']).value_counts().to_frame(name='ubsl_freq')
grouped_group_ubsc=df.groupby(['Group','Current_Unbeaten_Streak'])
grouped_group_ubsl=df.groupby(['Group','Longest_Unbeaten_Streak'])

### define functions to count strong contender team based of Current_Unbeaten_Streak
def ubsc_strong(row):
    ubsc_row = row['Current_Unbeaten_Streak']
    ubsl_row = row['Longest_Unbeaten_Streak']
    group_row = row['Group']
    team_row = row['Team']
    
    if ubsc_row>=5:
        row['Strong_Count']+=1
    elif ubsc_row>=topg_ubsc[row['Group']] and ubsc_row!=0:
        strong = True
        if freq_ubsc_group.loc[row['Group']].loc[row['Current_Unbeaten_Streak']]['ubsc_freq']>1:
            ref_ubsc = grouped_group_ubsc.get_group((group_row,ubsc_row))
            for ind in ref_ubsc.index:
                group_ind = ref_ubsc.loc[ind,'Group']
                team_ind = ref_ubsc.loc[ind,'Team']
                ubsc_ind = ref_ubsc.loc[ind,'Current_Unbeaten_Streak']
                ubsl_ind = ref_ubsc.loc[ind,'Longest_Unbeaten_Streak']
                if group_row!=group_ind or team_row!=team_ind:
                    if ubsl_row<ubsl_ind:
                        strong = False
                        break
        if strong: 
            row['Strong_Count'] += 1
        
    return row

### define functions to count strong contender team based of Longest_Unbeaten_Streak
def ubsl_strong(row):
    ubsc_row = row['Current_Unbeaten_Streak']
    ubsl_row = row['Longest_Unbeaten_Streak']
    group_row = row['Group']
    team_row = row['Team']
    
    if ubsl_row>=14:
        row['Strong_Count']+=1
    elif ubsl_row>=topg_ubsl[row['Group']] and ubsl_row!=0:
        strong = True
        if freq_ubsl_group.loc[row['Group']].loc[row['Longest_Unbeaten_Streak']]['ubsl_freq']>1:
            ref_ubsl = grouped_group_ubsl.get_group((group_row,ubsl_row))
            for ind in ref_ubsl.index:
                group_ind = ref_ubsl.loc[ind,'Group']
                team_ind = ref_ubsl.loc[ind,'Team']
                ubsc_ind = ref_ubsl.loc[ind,'Current_Unbeaten_Streak']
                ubsl_ind = ref_ubsl.loc[ind,'Longest_Unbeaten_Streak']
                if group_row!=group_ind or team_row!=team_ind:
                    if ubsc_row<ubsc_ind:
                        strong = False
                        break
        if strong: 
            row['Strong_Count'] += 1
        
    return row

## var and func for Current_Winless_Streak and Longest_Winless_Streak
### create vars of top 1 each group, value counts each group, and grouping with group
### based on Current_Winless_Streak and Longest_Winless_Streak
topg_wlsc=df.groupby('Group')['Current_Winless_Streak'].max()
topg_wlsl=df.groupby('Group')['Longest_Winless_Streak'].max()
freq_wlsc_group=(df.groupby(['Group'])['Current_Winless_Streak']).value_counts().to_frame(name='wlsc_freq')
freq_wlsl_group=(df.groupby(['Group'])['Longest_Winless_Streak']).value_counts().to_frame(name='wlsl_freq')
grouped_group_wlsc=df.groupby(['Group','Current_Winless_Streak'])
grouped_group_wlsl=df.groupby(['Group','Longest_Winless_Streak'])

### define functions to count weak contender team based of Current_Winless_Streak
def wlsc_weak(row):
    wlsc_row = row['Current_Winless_Streak']
    wlsl_row = row['Longest_Winless_Streak']
    group_row = row['Group']
    team_row = row['Team']
    
    if wlsc_row>=2:
        row['Weak_Count']+=1
    elif wlsc_row>=topg_wlsc[row['Group']] and wlsc_row!=0:
        weak = True
        if freq_wlsc_group.loc[row['Group']].loc[row['Current_Winless_Streak']]['wlsc_freq']>1:
            ref_wlsc = grouped_group_wlsc.get_group((group_row,wlsc_row))
            for ind in ref_wlsc.index:
                group_ind = ref_wlsc.loc[ind,'Group']
                team_ind = ref_wlsc.loc[ind,'Team']
                wlsc_ind = ref_wlsc.loc[ind,'Current_Winless_Streak']
                wlsl_ind = ref_wlsc.loc[ind,'Longest_Winless_Streak']
                if group_row!=group_ind or team_row!=team_ind:
                    if wlsl_row<wlsl_ind:
                        weak = False
                        break
        if weak: 
            row['Weak_Count'] += 1
        
    return row

### define functions to count weak contender team based of Longest_Winless_Streak
def wlsl_weak(row):
    wlsc_row = row['Current_Winless_Streak']
    wlsl_row = row['Longest_Winless_Streak']
    group_row = row['Group']
    team_row = row['Team']
    
    if wlsl_row>=6:
        row['Weak_Count']+=1
    elif wlsl_row>=topg_wlsl[row['Group']] and wlsl_row!=0:
        weak = True
        if freq_wlsl_group.loc[row['Group']].loc[row['Longest_Winless_Streak']]['wlsl_freq']>1:
            ref_wlsl = grouped_group_wlsl.get_group((group_row,wlsl_row))
            for ind in ref_wlsl.index:
                group_ind = ref_wlsl.loc[ind,'Group']
                team_ind = ref_wlsl.loc[ind,'Team']
                wlsc_ind = ref_wlsl.loc[ind,'Current_Winless_Streak']
                wlsl_ind = ref_wlsl.loc[ind,'Longest_Winless_Streak']
                if group_row!=group_ind or team_row!=team_ind:
                    if wlsc_row<wlsc_ind:
                        weak = False
                        break
        if weak: 
            row['Weak_Count'] += 1
        
    return row

## var and func for Current_Lose_Streak and Longest_Lose_Streak
### create vars of top 1 each group, value counts each group, and grouping with group
### based on Current_Lose_Streak and Longest_Lose_Streak
topg_lsc=df.groupby('Group')['Current_Lose_Streak'].max()
topg_lsl=df.groupby('Group')['Longest_Lose_Streak'].max()
freq_lsc_group=(df.groupby(['Group'])['Current_Lose_Streak']).value_counts().to_frame(name='lsc_freq')
freq_lsl_group=(df.groupby(['Group'])['Longest_Lose_Streak']).value_counts().to_frame(name='lsl_freq')
grouped_group_lsc=df.groupby(['Group','Current_Lose_Streak'])
grouped_group_lsl=df.groupby(['Group','Longest_Lose_Streak'])

### define functions to count weak contender team based of Current_Lose_Streak
def lsc_weak(row):
    lsc_row = row['Current_Lose_Streak']
    lsl_row = row['Longest_Lose_Streak']
    group_row = row['Group']
    team_row = row['Team']
    
    if lsc_row>=1:
        row['Weak_Count']+=1
    elif lsc_row>=topg_lsc[row['Group']] and lsc_row!=0:
        weak = True
        if freq_lsc_group.loc[row['Group']].loc[row['Current_Lose_Streak']]['lsc_freq']>1:
            ref_lsc = grouped_group_lsc.get_group((group_row,lsc_row))
            for ind in ref_lsc.index:
                group_ind = ref_lsc.loc[ind,'Group']
                team_ind = ref_lsc.loc[ind,'Team']
                lsc_ind = ref_lsc.loc[ind,'Current_Lose_Streak']
                lsl_ind = ref_lsc.loc[ind,'Longest_Lose_Streak']
                if group_row!=group_ind or team_row!=team_ind:
                    if lsl_row<lsl_ind:
                        weak = False
                        break
        if weak: 
            row['Weak_Count'] += 1
        
    return row

### define functions to count weak contender team based of Longest_Lose_Streak
def lsl_weak(row):
    lsc_row = row['Current_Lose_Streak']
    lsl_row = row['Longest_Lose_Streak']
    group_row = row['Group']
    team_row = row['Team']
    
    if lsl_row>=4:
        row['Weak_Count']+=1
    elif lsl_row>=topg_lsl[row['Group']] and lsl_row!=0:
        weak = True
        if freq_lsl_group.loc[row['Group']].loc[row['Longest_Lose_Streak']]['lsl_freq']>1:
            ref_lsl = grouped_group_lsl.get_group((group_row,lsl_row))
            for ind in ref_lsl.index:
                group_ind = ref_lsl.loc[ind,'Group']
                team_ind = ref_lsl.loc[ind,'Team']
                lsc_ind = ref_lsl.loc[ind,'Current_Lose_Streak']
                lsl_ind = ref_lsl.loc[ind,'Longest_Lose_Streak']
                if group_row!=group_ind or team_row!=team_ind:
                    if lsc_row<lsc_ind:
                        weak = False
                        break
        if weak: 
            row['Weak_Count'] += 1
        
    return row

# execute all functions
df['Strong_Count']=[fifa_strong(x,y) for x,y in zip(df['FIFA_Ranking'],df['Strong_Count'])]
df['Weak_Count']=[fifa_weak(x,y) for x,y in zip(df['FIFA_Ranking'],df['Weak_Count'])]
df['Strong_Count']=[gpc_strong(x,y) for x,y in zip(df['Avg_GoalsPerCaps'],df['Strong_Count'])]
df['Weak_Count']=[gpc_weak(x,y) for x,y in zip(df['Avg_GoalsPerCaps'],df['Weak_Count'])]
df['Strong_Count']=[wr_strong(x,y) for x,y in zip(df['Win_Rate_Percentage'],df['Strong_Count'])]
df['Weak_Count']=[wr_weak(x,y) for x,y in zip(df['Win_Rate_Percentage'],df['Weak_Count'])]
df['Strong_Count']=[gs_strong(x,y) for x,y in zip(df['Goals_Scored_per_Match'],df['Strong_Count'])]
df['Weak_Count']=[gs_weak(x,y) for x,y in zip(df['Goals_Scored_per_Match'],df['Weak_Count'])]
df['Strong_Count']=[gc_strong(x,y) for x,y in zip(df['Goals_Conceded_per_Match'],df['Strong_Count'])]
df['Weak_Count']=[gc_weak(x,y) for x,y in zip(df['Goals_Conceded_per_Match'],df['Weak_Count'])]
df=df.apply(wsc_strong, axis='columns')
df=df.apply(wsl_strong, axis='columns')
df=df.apply(ubsc_strong, axis='columns')
df=df.apply(ubsl_strong, axis='columns')
df=df.apply(wlsc_weak, axis='columns')
df=df.apply(wlsl_weak, axis='columns')
df=df.apply(lsc_weak, axis='columns')
df=df.apply(lsl_weak, axis='columns')

# show the result
print('Teams which are strong contender in 5 or more main units are \n', df.loc[df['Strong_Count']>=5]['Team'].to_numpy())
print('\nTeams which are weak contender in 5 or more main units are \n', df.loc[df['Weak_Count']>=5]['Team'].to_numpy())


# In[ ]:




