
#sample machine learning stuff
# by Drew Wingfield
# started 2024-02-15

#region Imports
print(' ml-test.py')
print(' (c) 2024 Drew Wingfield, All Rights Reserved')
print(' Also see the README.md file.')
print(' This script either loads or trains a few machine learning algorithms based on machinefile.csv')
print(' prepare-machinelearning.py should already be run to create that file.')
print(' If training the data (not loading the models), this script could take a LONG time.')
print(' Last time I ran it it took 8 hours on a beefy computer. You have been warned.')

print('Importing modules...')
print('  - Builtins')
import pickle
import time
import gc

starttime = time.time()

print('  - commonresources.py')
from commonresources import PATH_TO_FTCAPI, PATH_TO_JOBLIB_CACHE, CRAPPY_LAPTOP, LATEST_VERSION, green_check, red_x, info_i, seconds_to_time
print('                 Using version '+str(LATEST_VERSION))

print('  - External modules:')
print('      ~ Joblib')
import joblib
memory = joblib.Memory(PATH_TO_JOBLIB_CACHE, verbose=0)

print('      ~ sklearn')
from sklearn.discriminant_analysis import StandardScaler
from sklearn.svm import SVR, SVC #, NuSVC
#from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

from sklearn.model_selection import learning_curve
from sklearn.model_selection import LearningCurveDisplay, ShuffleSplit

from sklearn.neighbors import KNeighborsClassifier

#from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline, make_pipeline

from sklearn.linear_model import LogisticRegression
#from sklearn import metrics

from sklearn import preprocessing

print('      ~ matplotlib')
import matplotlib.pyplot as plt
#import matplotlib.colors as mcolors

print('      ~ pandas')
import pandas as pd

print('      ~ numpy')
import numpy as np
#endregion Imports


#region vars


CACHE_SIZE = 2000
assert CACHE_SIZE <= 2000 # NOTE There's a bug with scikit that prevents values over 2000 from being useful
print(info_i()+f' Memory per thread: {CACHE_SIZE} MB')


NUMBER_OF_CORES = 12

LOAD_MODEL     = True
OUR_TEAM_ONLY  = False

assert (CRAPPY_LAPTOP == False or LOAD_MODEL == True)


if OUR_TEAM_ONLY:
    print(info_i()+'  Running tests for OUR TEAM ONLY.')
#endregion vars

# the below function was copypasted from https://stackoverflow.com/questions/37161563/how-to-graph-grid-scores-from-gridsearchcv
def plot_grid_search(cv_results, grid_param_1, grid_param_2, name_param_1, name_param_2):
    # Get Test Scores Mean and std for each grid search
    scores_mean = cv_results['mean_test_score']
    scores_mean = np.array(scores_mean).reshape(len(grid_param_2),len(grid_param_1))

    scores_sd = cv_results['std_test_score']
    scores_sd = np.array(scores_sd).reshape(len(grid_param_2),len(grid_param_1))

    # Plot Grid search scores
    _, ax = plt.subplots(1,1)

    # Param1 is the X-axis, Param 2 is represented as a different curve (color line)
    for idx, val in enumerate(grid_param_2):
        ax.plot(grid_param_1, scores_mean[idx,:], '-o', label= name_param_2 + ': ' + str(val))

    ax.set_title("Grid Search Scores", fontsize=20, fontweight='bold')
    ax.set_xlabel(name_param_1, fontsize=16)
    ax.set_ylabel('CV Average Score', fontsize=16)
    ax.legend(loc="best", fontsize=15)
    ax.grid('on')



def describe_model(model, X_cat_test, Y_cat_test):
    print('\n'+info_i()+'Model stats:')
    print(info_i()+f'     Best score:  {model.best_score_ }')
    print(info_i()+f'     Best params: {model.best_params_}')
    print(info_i()+f'     Best estimator: {model.best_estimator_}')
    print(info_i()+ '     Test Accuracy: %.3f' % model.score(X_cat_test, Y_cat_test))
    print(info_i()+f'     Best index: {model.best_index_}')


print(info_i()+' Loading data...')

#trainingdata = get_json('/home/wingfield/ftcapi/machinefile-lowspace.json')
#trainingdata = get_json(PATH_TO_FTCAPI+'machinefile.json')

pandasdata = pd.read_csv(PATH_TO_FTCAPI+'machinefile.csv', dtype={
    'RedOPR' :np.longdouble, 'RedAutoOPR' :np.longdouble, 'RedCCWM' :np.longdouble, 
    'blueOPR':np.longdouble, 'blueAutoOPR':np.longdouble, 'blueCCWM':np.longdouble, 
    'recentRedOPR' :np.longdouble, 'recentRedAutoOPR' :np.longdouble, 'recentRedCCWM' :np.longdouble, 
    'recentblueOPR':np.longdouble, 'recentblueAutoOPR':np.longdouble, 'recentblueCCWM':np.longdouble, 
    'scoreRedFinal':np.int16, 'scoreRedAuto':np.int8, 'scoreBlueFinal':np.int16, 'scoreBlueAuto':np.int8,
    'whoWon':np.str_
    })

print(green_check()+' Data successfully loaded from machinefile.csv')
print(info_i()+' Info:')
print(info_i()+f'    pandasdata size: {pandasdata.size}')
print(info_i()+f'    pandasdata shape: {pandasdata.shape}')

#actualStartTime,description,tournamentLevel,scoreRedFinal,scoreRedAuto,scoreBlueFinal,scoreBlueAuto,redOPR,redAutoOPR,redCCWM,blueOPR,blueAutoOPR,blueCCWM,recentredOPR,recentredAutoOPR,recentredCCWM,recentblueOPR,recentblueAutoOPR,recentblueCCWM,whoWon
try:
    X = pandasdata[['redOPR','redAutoOPR','redCCWM','blueOPR','blueAutoOPR','blueCCWM', 'recentredOPR','recentredAutoOPR','recentredCCWM', 'recentblueOPR', 'recentblueAutoOPR', 'recentblueCCWM']]
    #Y = pandasdata['scoreDifference']
    Y_cat = pandasdata['whoWon']


except Exception as e:
    print(' pandasdata:')
    print(pandasdata)

    raise e

#region oldcode
# pandasdata = pd.read_csv(PATH_TO_FTCAPI+'machinefile-recent.csv', dtype={
#     'RedOPR' :np.longdouble, 'RedAutoOPR' :np.longdouble, 'RedCCWM' :np.longdouble, 
#     'blueOPR':np.longdouble, 'blueAutoOPR':np.longdouble, 'blueCCWM':np.longdouble, 
#     'scoreRedFinal':np.int16, 'scoreRedAuto':np.int8, 'scoreBlueFinal':np.int16, 'scoreBlueAuto':np.int8,
#     'whoWon':np.str_
#     })
# X_recent = pandasdata[['RedOPR','RedAutoOPR','RedCCWM','BlueOPR','BlueAutoOPR','BlueCCWM']]
# Y_cat_recent = pandasdata['whoWon']

# print(green_check()+' Data successfully loaded from machienfile-recent.csv')


#StartTime,RedOPR,RedAutoOPR,RedCCWM,BlueOPR,BlueAutoOPR,BlueCCWM,scoreRedFinal,scoreRedAuto,scoreBlueFinal,scoreBlueAuto

#region oldcode
#'{"actualStartTime": "'+str(match['actualStartTime'])
#            +'","scoreRedFinal": ' +str(match['scoreRedFinal']  )
#            + ',"scoreRedAuto": '  +str(match['scoreRedAuto']   )
#            + ',"scoreBlueFinal": '+str(match['scoreBlueFinal'] )
#            + ',"scoreBlueAuto": ' +str(match['scoreBlueAuto']  )+', '+
#            '"Red1":{}, "Red2":{},"Blue1":{},"Blue2":{}'.format(red1, red2, blue1, blue2).replace("'",'"').replace("True",'true').replace('False','false')
#            + '}, \n'
#
#{"OPR":team['OPR'], "AutoOPR":team['AutoOPR'], "CCWM":team['CCWM']}



# X is our feature data
# Y is our label

#x_ = [[z['Red1']['OPR'],z['Red1']['AutoOPR'],z['Red1']['CCWM']] for z in trainingdata['matches']]
#x_ = []
#y_ = []

#for match in trainingdata['matches']:
    #x_.append(
    #    [
    #        #red
    #        sum([match['Red1' ]['OPR'    ],match['Red2' ]['OPR'    ]]),
    #        #sum([match['Red1' ]['AutoOPR'],match['Red2' ]['AutoOPR']]),
    #        #sum([match['Red1' ]['CCWM'   ],match['Red2' ]['CCWM'   ]]),
    #        sum([match['Blue1']['OPR'    ],match['Blue2']['OPR'    ]]),
    #        #sum([match['Blue1']['AutoOPR'],match['Blue2']['AutoOPR']])#,
    #        #sum([match['Blue1']['CCWM'   ],match['Blue2']['CCWM'   ]])
    #    ]
    #)

#    x_.append(
#        [float(match['Red1']['OPR']+match['Red2' ]['OPR']) - float(match['Blue1']['OPR']+match['Blue2']['OPR'])]
        #[float(match['Red1']['AutoOPR']+match['Red2' ]['AutoOPR']) - float(match['Blue1']['AutoOPR']+match['Blue2']['AutoOPR'])]
#    )
    #y_.append( 0 if (match['scoreRedFinal']-match['scoreBlueFinal'])<0 else 1   )
#    y_.append(match['scoreRedFinal']-match['scoreBlueFinal'])
    #y_.append(
    #    [
    #        match['scoreRedFinal'],
    #        match['scoreRedAuto'],
    #        match['scoreBlueFinal'],
    #        match['scoreBlueAuto']
    #    ]
    #)

#print('Last match: '+str(match))


#X = np.array(trainingdata['matches']['"Red1"'])
#X = np.array(x_, dtype=np.float16)
#Y = np.array(y_, dtype=np.float16)
#endregion oldcode
#endregion oldcode


print(info_i()+' Splitting testing/training data sets')

#X_train, X_test, Y_train, Y_test         = train_test_split(X,Y, test_size=0.3) #delete random_state to enable the actual randomness every time - this is just cementing the seed so I can repeat the same thing
X_cat_train, X_cat_test, Y_cat_train, Y_cat_test = train_test_split(X,Y_cat, test_size=0.25) #delete random_state to enable the actual randomness every time - this is just cementing the seed so I can repeat the same thing

print(green_check()+' Testing and training sets have been split.')
print(info_i()+' Info:')
#print(info_i()+f'    X_train shape    {X_train.shape}')
#print(info_i()+f'    Y_test shape     {Y_train.shape}')
print(info_i()+f'    Y_cat_train shape {Y_cat_train.shape}')
#print(info_i()+f'    X_train shape:   {X_test.shape }')
#print(info_i()+f'    Y_test shape     {Y_test.shape }')
print(info_i()+f'    Y_cat_test shape {Y_cat_test.shape }')

# 2024-04-05 8:43pm for an unprocessed set:
# [i]gsSVC
# [i]     Best score:  0.676531420742477
# [i]     Best params: {'svc__C': 100, 'svc__cache_size': 2000, 'svc__gamma': 0.001, 'svc__kernel': 'rbf'}
# [i]     Best estimator: Pipeline(steps=[('standardscaler', StandardScaler()),
#                 ('svc', SVC(C=100, cache_size=2000, gamma=0.001))])
# [i]     Test Accuracy: 0.684
# [i]     Best index: 67

print(info_i()+f'X array:')
print(X)
#print(info_i()+f'Y array: {Y}')
print(info_i()+f'Y_cat array: {Y_cat}')

print(info_i()+' Making the pipeline')

#region SVC
pipelineSVC = make_pipeline(StandardScaler(with_mean=True, with_std=True), SVC())


pipelineNeigh = make_pipeline(StandardScaler(with_mean=True, with_std=True), KNeighborsClassifier())

# create params grid
param_grid_svc = [
    {
        'svc__C':[0.001, 0.01, 0.05, 0.1, 0.5, 1, 10, 100, 1000],
        'svc__cache_size':[CACHE_SIZE],
        'svc__kernel':['linear']
    },
    {
        'svc__C':[0.001, 0.01, 0.05, 0.1, 0.5, 1, 10, 100, 1000],
        'svc__cache_size':[CACHE_SIZE],
        'svc__kernel':['poly']
    },
    {
        'svc__C':[0.001, 0.01, 0.05, 0.1, 0.5, 1, 10, 100, 1000],
        'svc__gamma':[0.001, 0.01, 0.05, 0.1, 0.5, 1, 10],
        'svc__cache_size':[CACHE_SIZE],
        'svc__kernel':['rbf']
    },
    {
        'svc__C':[0.001, 0.01, 0.05, 0.1, 0.5, 1, 10, 100, 1000],
        'svc__cache_size':[CACHE_SIZE],
        'svc__kernel':['sigmoid']
    },
]

# Params for training 2024-04-13
# [i] Fitting KNeighborsClassifier...
# [✓] gsNeigh successfully fit!
# [✓] gsNeigh model saved as /Users/thedr/ftcapi-branch45-3/gsNeigh.pkl
# C:\Users\thedr\sklearn-venv\lib\site-packages\numpy\core\fromnumeric.py:3643: FutureWarning: The behavior of DataFrame.std with axis=None is deprecated, in a future version this will reduce over both axes and return a scalar. To retain the old behavior, pass axis=0 (or do not pass axis)
#   return std(axis=axis, dtype=dtype, out=out, ddof=ddof, **kwargs)
# [✓] gsNeigh standard scale saved as /Users/thedr/ftcapi-branch45-3/gsNeigh_std.npy
# [✓] gsNeigh scale mean saved as /Users/thedr/ftcapi-branch45-3/gsNeigh_mean.pkl

# [i]gsNeigh
# [i]     Best score:  0.6600594887652711
# [i]     Best params: {'kneighborsclassifier__algorithm': 'auto', 'kneighborsclassifier__leaf_size': 10, 'kneighborsclassifier__metric': 'minkowski', 'kneighborsclassifier__n_neighbors': 600, 'kneighborsclassifier__p': 1, 'kneighborsclassifier__weights': 'distance'}
# [i]     Best estimator: Pipeline(steps=[('standardscaler', StandardScaler()),
#                  KNeighborsClassifier(leaf_size=10, n_neighbors=600, p=1,
#                                       weights='distance'))])
# [i]     Test Accuracy: 0.659
# [i]     Best index: 5
# [i] That took 9 minutes, 17.779 seconds total so far
# [i] Fitting gsSVC...
# [✓] gsSVC successfully fit!
# [✓] gsSVC model saved as /Users/thedr/ftcapi-branch45-3/gsSVC.pkl
# C:\Users\thedr\sklearn-venv\lib\site-packages\numpy\core\fromnumeric.py:3643: FutureWarning: The behavior of DataFrame.std with axis=None is deprecated, in a future version this will reduce over both axes and return a scalar. To retain the old behavior, pass axis=0 (or do not pass axis)
#   return std(axis=axis, dtype=dtype, out=out, ddof=ddof, **kwargs)
# [✓] gsSVC standard scale saved as /Users/thedr/ftcapi-branch45-3/gsSVC_std.npy
# [✓] gsSVC scale mean saved as /Users/thedr/ftcapi-branch45-3/gsSVC_mean.pkl

# [i]gsSVC
# [i]     Best score:  0.6765780983770122
# [i]     Best params: {'svc__C': 100, 'svc__cache_size': 2000, 'svc__gamma': 0.001, 'svc__kernel': 'rbf'}
# [i]     Best estimator: Pipeline(steps=[('standardscaler', StandardScaler()),
#                 ('svc', SVC(C=100, cache_size=2000, gamma=0.001))])
# [i]     Test Accuracy: 0.673
# [i]     Best index: 67
# [i] That took 7 hours, 58 minutes, and 42.974 seconds total so far









# n_neighbors: Int = 5,
#     *,
#     weights: ((...) -> Any) | Literal['uniform', 'distance'] | None = "uniform",
#     algorithm: Literal['auto', 'ball_tree', 'kd_tree', 'brute'] = "auto",
#     leaf_size: Int = 30,
#     p: Int = 2,
#     metric: str | ((...) -> Any) = "minkowski",
#     metric_params: dict | None = None,
#     n_jobs: Int | None = None

# KNeighborsClassification working with gridsearchCV with help from https://www.datasklr.com/select-classification-methods/k-nearest-neighbors 
# create params grid
param_grid_neigh = {
    'kneighborsclassifier__n_neighbors': (1,600, 1),
    'kneighborsclassifier__algorithm':['auto', 'ball_tree', 'kd_tree', 'brute'],
    'kneighborsclassifier__leaf_size': (10,50,1),
    'kneighborsclassifier__p': (1,2),
    'kneighborsclassifier__weights': ('uniform', 'distance'),
    'kneighborsclassifier__metric': ('minkowski', 'chebyshev'),
}

"""
parameters_KNN = {
    'n_neighbors': (1,10, 1),
    'leaf_size': (20,40,1),
    'p': (1,2),
    'weights': ('uniform', 'distance'),
    'metric': ('minkowski', 'chebyshev'),
"""
# create gridsearchcv
gsSVC = GridSearchCV(estimator=pipelineSVC, param_grid=param_grid_svc, scoring='accuracy', cv=10, refit=True, n_jobs=NUMBER_OF_CORES, error_score='raise')
#gsSVC_recent = GridSearchCV(estimator=pipelineSVC, param_grid=param_grid_svc, scoring='accuracy', cv=10, refit=True, n_jobs=-1, error_score='raise')

gsNeigh = GridSearchCV(estimator=pipelineNeigh, param_grid=param_grid_neigh, scoring='accuracy', cv=10, refit=True, n_jobs=NUMBER_OF_CORES, error_score='raise')


print(green_check()+' gsSVC and gsNeigh created as GridSearchCVs')
#print(info_i()+' - - - - \n'+info_i()+'Training GridSearchCVs...')

if LOAD_MODEL:
    print(info_i()+' Loading models...')
    
    with open(PATH_TO_FTCAPI+'gsNeigh.pkl', 'rb') as f:
        gsNeigh = pickle.load(f)
    
    print(green_check()+'     Model gsNeigh loaded.')


    with open(PATH_TO_FTCAPI+'gsSVC.pkl', 'rb') as f:
        gsSVC = pickle.load(f)
    
    print(green_check()+'     Model gsSVC loaded.')

else:
    print(info_i()+f' pipelineNeigh[0] (should be StandardScalar()): {pipelineNeigh[0]}')
    print(info_i()+' Fitting KNeighborsClassifier...')

    gsNeigh.fit(X_cat_train, Y_cat_train)

    print(green_check()+' gsNeigh successfully fit!')

    with open(PATH_TO_FTCAPI+'gsNeigh.pkl','wb') as f:
        pickle.dump(gsNeigh,f)
    
    print(green_check()+' gsNeigh model saved as '+PATH_TO_FTCAPI+'gsNeigh.pkl')

    # Save the scaling variables for later prediction.
    #std = np.sqrt(pipelineNeigh[0].var_)
    np.save(PATH_TO_FTCAPI+'gsNeigh_std.npy',np.std(X_cat_train))
    print(green_check()+' gsNeigh standard scale saved as '+PATH_TO_FTCAPI+'gsNeigh_std.npy')

    np.save(PATH_TO_FTCAPI+'gsNeigh_mean.npy', np.mean(X_cat_train))
    print(green_check()+' gsNeigh scale mean saved as '+PATH_TO_FTCAPI+'gsNeigh_mean.pkl')
    print(info_i()+' gsNeigh:')
    describe_model(gsNeigh, X_cat_test, Y_cat_test)
    print(info_i()+f' That took {seconds_to_time((time.time()-starttime))} total so far')

    #print(neigh.predict([[1.1]]))[0]
    #print(neigh.predict_proba([[0.9]]))

    print(info_i()+' Fitting gsSVC...')

    gsSVC.fit(X_cat_train, Y_cat_train)

    print(green_check()+' gsSVC successfully fit!')

    with open(PATH_TO_FTCAPI+'gsSVC.pkl','wb') as f:
        pickle.dump(gsSVC,f)
    
    print(green_check()+' gsSVC model saved as '+PATH_TO_FTCAPI+'gsSVC.pkl')


    # Save the scaling variables for later prediction.
    #std = np.sqrt(pipelineSVC[0].var_)
    np.save(PATH_TO_FTCAPI+'gsSVC_std.npy',np.std(X_cat_train))
    print(green_check()+' gsSVC standard scale saved as '+PATH_TO_FTCAPI+'gsSVC_std.npy')

    np.save(PATH_TO_FTCAPI+'gsSVC_mean.npy', np.mean(X_cat_train))
    print(green_check()+' gsSVC scale mean saved as '+PATH_TO_FTCAPI+'gsSVC_mean.pkl')

    print('\n'+info_i()+'gsSVC')
    describe_model(gsSVC, X_cat_test, Y_cat_test)

    print(info_i()+f' That took {seconds_to_time((time.time()-starttime))} total so far')


#region oldcode
# 2023-02-23
#gsSVC_recent:
#    Best score:  0.6772661948308816
#    Best params: {'svc__C': 1000, 'svc__cache_size': 2000, 'svc__gamma': 0.05, 'svc__kernel': 'rbf'}
#    Best estimator: Pipeline(steps=[('standardscaler', StandardScaler()),
#               ('svc', SVC(C=1000, cache_size=2000, gamma=0.05))])
#    Test Accuracy: 0.671
#    Best index: 76


#gsSVC
#    Best score:  0.7809569614496438
#    Best params: {'svc__C': 0.5, 'svc__cache_size': 2000, 'svc__gamma': 0.05, 'svc__kernel': 'rbf'}
#    Best estimator: Pipeline(steps=[('standardscaler', StandardScaler()),
#                ('svc', SVC(C=0.5, cache_size=2000, gamma=0.05))])
#    Test Accuracy: 0.774
#    Best index: 48

# print(info_i()+'\n\ngsSVC_recent:')
# print(info_i()+f'     Best score:  {gsSVC_recent.best_score_ }')
# print(info_i()+f'     Best params: {gsSVC_recent.best_params_}')
# print(info_i()+f'     Best estimator: {gsSVC_recent.best_estimator_}')
# print(info_i()+ '     Test Accuracy: %.3f' % gsSVC.score(X_cat_test_recent, Y_cat_test_recent))
# print(info_i()+f'     Best index: {gsSVC_recent.best_index_}')
#endregion oldcode


#region showstats
print()
print(info_i()+' All model training done. Now showing stats for all models:')

print('X_cat_test:')
print(X_cat_test)

print('type(X_cat_test):')
print(type(X_cat_test))

print('X_cat_test.iloc[0]:')
print(X_cat_test.head(1))

print('gsNeigh predict raw:')
print(gsNeigh.predict(X_cat_test.head(1)))
print('gsNeigh predict type:')
print(type(gsNeigh.predict(X_cat_test.head(1))))
print('gsNeigh predict [0]:')
print(gsNeigh.predict(X_cat_test.head(1))[0])

print('gsSVC predict raw:')
print(gsSVC.predict(X_cat_test.head(1)))
print('gsSVC predict type:')
print(type(gsSVC.predict(X_cat_test.head(1))))
print('gsSVC predict [0]:')
print(gsSVC.predict(X_cat_test.head(1))[0])

print('\n'+info_i()+'gsNeigh')
describe_model(gsNeigh, X_cat_test, Y_cat_test)

print('\n'+info_i()+'gsSVC')
describe_model(gsSVC, X_cat_test, Y_cat_test)
#endregion showstats

print(info_i()+f' That took {seconds_to_time((time.time()-starttime))} total so far')
print(green_check()+' ml-test.py done.')
# -- end of file --