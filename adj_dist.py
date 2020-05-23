import pandas as pd
import config 
import numpy as np
import copy

arg = config.get()

import random
from collections import Counter
import copy


def get_label_dist(df):
    dist_df = dict(Counter(df["label"]))

    total = len(df)

    for key, value in dist_df.items():
        dist_df[key] = np.round(value/total, 2)
        
    return dist_df

def sampling_by_dist(train, test, size):

    val_vocid = []
    vocids = train["vocid"]
    label_list = list(set(train["label"]))
    dist = get_label_dist(test)

    for label in label_list:

        ratio = dist[label]
        target_cnt = int(ratio*size)

        pop_list = list(train[train["label"]==label]["vocid"])

        val_vocid += random.sample(pop_list, target_cnt)
        
    val_df = train[train["vocid"].isin(val_vocid)]
    train_df = train[~train["vocid"].isin(val_vocid)]

    return train_df, val_df

def RS(df, aug_size, loop_cnt):
    
    if aug_size > len(df):
        tmp = copy.deepcopy(df)
        
    else :
        aug_vocid = random.sample(list(df["vocid"]), aug_size)
        tmp = df[df['vocid'].isin(aug_vocid)]
        
        
    ####################
    #RS구현
    ####################
    df = pd.concat([df, tmp], axis=0)

    return df

def get_aug_data(df, target_size):
    
    aug_data = pd.DataFrame()
    print(target_size)
    print("=")
    print(len(df))
    
    loop_cnt = 0
    
    while True:
        loop_cnt += 1
        aug_size = target_size - len(df)
        print(str(loop_cnt) + "th aug_size : ", str(aug_size))

        if aug_size > 0:
            
            df = RS(df, aug_size, loop_cnt)
        
        elif aug_size == 0 :
            return df
            
        else: 
            aug_vocid = random.sample(list(df["vocid"]), target_size)
            return df[df['vocid'].isin(aug_vocid)]
        
        
def adjust_dist(train, test):

    label_list = list(set(train["label"]))
    dist = get_label_dist(test)
    train_size = 10000

    aug_train_df = pd.DataFrame()

    for label in label_list:

        print("label :", label)

        ratio = dist[label]
        target_size = int(ratio*train_size)

        df = train[train["label"]==label]
        aug_train_df = pd.concat([aug_train_df, get_aug_data(df, target_size)], axis=0)
        
    return aug_train_df



            

        
        