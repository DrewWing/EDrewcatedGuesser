
# view data
# started March 1st, 2024
# by Drew Wingfield

# with help from https://stackoverflow.com/questions/21654635/how-to-create-a-scatter-plot-by-category
# for matplotlib plotting


from common_resources import PATH_TO_FTCAPI, red_x, info_i, green_check, get_json


print(info_i()+' [viewdata.py] Importing')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import sys
import os

plt.style.use('dark_background')


heatmap = True
do_first_map = True


if 'heatmap' in sys.argv:
    heatmap = True


if 'heatmap-off' in sys.argv:
    heatmap = False

# from https://stackoverflow.com/questions/20105364/how-can-i-make-a-scatter-plot-colored-by-density
def using_hist2d(ax, x, y, bins=(50, 50)):
    # https://stackoverflow.com/a/20105673/3015186
    # Answer by askewchan
    ax.hist2d(x, y, bins, cmap=plt.cm.jet)




if do_first_map:
    print(info_i()+' Generating data')
    # Generate Data
    allmatches = pd.read_csv(os.path.join(PATH_TO_FTCAPI,'generatedfiles','all_matches.csv'))
    
    allmatches.drop(
                ['description'], 
                axis=1, 
                inplace=True
            )
    
    
    #x = allmatches['scoreRedFinal']
    #y = allmatches['scoreBlueFinal']
    
    #labels = np.where(allmatches['scoreBlueFinal'] > allmatches['scoreRedFinal'], 'Blue', 'Red')
    labels = allmatches['tournamentLevel']
    
    
    
    
    x = allmatches['scoreRedFinal'] - allmatches['scoreBlueFinal']
    y = np.where(allmatches['scoreRedFinal'] > allmatches['scoreBlueFinal'], 1, -1)
    
    #labels = allmatches['tournamentLevel']
    
    
    
    print(info_i()+' Plotting')
    
    
    df = pd.DataFrame(dict(x=x, y=y, label=labels))
    
    groups = df.groupby('label')
    
    # Plot
    fig, ax = plt.subplots()
    ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
    
    
    if heatmap:
        using_hist2d(ax, x, y, bins=(1000,2))
    
    else:
        for name, group in groups:
            ax.plot(group.x, group.y, marker='o', linestyle='', ms=2, label=name)
    
    plt.ylabel('RedFinal > BlueFinal')
    plt.xlabel('scoreRedFinal - scoreBlueFinal')
    
    #plt.axis([-1, 350, -1, 350])
    
    plt.axis([-400, 400, -1.4, 1.4])
    
    #ax.set_xlim([-400, 400])
    #ax.set_ylim([-400, 400])
    
    ax.legend()
    
    plt.show()


print(info_i()+' Generating data')
# Generate Data
#allmatches = pd.read_csv(PATH_TO_FTCAPI+'globaloprs/OPR_result_sorted.json')
#{"teamNumber":25218, "teamName":"Undefined", "OPR":172.40222517085803, "AutoOPR":56.822136784937285, "CCWM":109.1174444069353}, 
rj = get_json(os.path.join(PATH_TO_FTCAPI,'globaloprs','OPR_result_sorted.json'))
rj_dic = {'teamNumber':[],'OPR':[],'AutoOPR':[],'CCWM':[]}

for team in rj['matches']:
    rj_dic['teamNumber'].append(team['teamNumber'])
    rj_dic['OPR'].append(team['OPR'])
    rj_dic['AutoOPR'].append(team['AutoOPR'])
    rj_dic['CCWM'].append(team['CCWM'])

allteams = pd.DataFrame(rj_dic)

#print(allteams)


x = allteams['OPR']
y = allteams['AutoOPR']

labels = np.where(allteams['teamNumber']==12928, "Us!", 'Others')

print(info_i()+'labels:')
print(info_i()+str(labels))


print(info_i()+' Plotting')


df = pd.DataFrame(dict(x=x, y=y, label=labels))

groups = df.groupby('label')
#groups = df


# Plot
fig, ax = plt.subplots()
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling



if heatmap:
        using_hist2d(ax, x, y, bins=(140,140))
    
else:
    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=2, label=name)
            

plt.ylabel('AutoOPR')
plt.xlabel('OPR')


# now add y=x equation
ax.axline((0, 0), slope=1, color='g') # https://stackoverflow.com/questions/25497402/adding-y-x-to-a-matplotlib-scatter-plot-if-i-havent-kept-track-of-all-the-data


#plt.axis([-1, 350, -1, 350])


#ax.set_xlim([-400, 400])
#ax.set_ylim([-400, 400])

ax.legend()

plt.show()








# -- End of file --