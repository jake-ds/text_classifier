from tqdm import tqdm
import numpy as np
import pandas as pd


def topN_evaluate(test_data, pred_y, test_y, N):
    
    label_nm_list = test_y.columns
    test_y_nm = list(test_y.apply(lambda x : x.argmax(), axis=1))
    pred_y_nm = []
    
    for prob_table in tqdm(pred_y):
        
        label_list = np.arange(0, len(label_nm_list))
        prob_list = list(prob_table)
        
        df = pd.DataFrame()
        df["label"] = label_nm_list
        df["prob"] = prob_list
        df = df[:N]
        
        pred_y_nm.append(list(df["label"]))
        
    def isAnswer(df):
        if df[1] in df[0]:
            return 1
        else :
            return 0
        
    concat_df = pd.DataFrame(list(zip(pred_y_nm, test_y_nm)), columns=["pred_y", "test_y"])
    concat_df["result"] = concat_df.apply(isAnswer, axis=1)
    
    answer = np.sum(list(concat_df["result"]))
    total = len(list(concat_df["result"]))
    acc = answer/total
    
    print("accuracy : ", answer/total)
    
    catg_df = test_data[["cateCode", 'vocid', 'cateL', 'cateM', 'cateS']]
    catg_df["index"] = test_y.index
    catg_df['title'] = test_data.title
    catg_df["cont"] = test_Data.cont
    catg_df["pred_y"] = list(concat_df["pred_y"])
    catg_df["result"] = list(concat_df['result'])
    
    return catg_df

