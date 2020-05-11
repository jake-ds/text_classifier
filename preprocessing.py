import ujon
import pandas as pd
import numpy as np
import config
from keras.preprocessing.sequence import pad_sequences
from utils import get_word_index, load_data
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import pickle
from konlpy.tag import Komoran

arg = config.get()


def add_cateCodeLM(df):
    
    try:
        df["cateCodeL"] = df["cateCode"].map(lambda x : x[:1])
        df["cateCodeM"] = df["cateCode"].map(lambda x : x[:2])
    except:
        print("check <cateCode> column...")
        
    return df


def merge_product_info(data):
    
    product = pd.read_csv("400.help/voc_product.csv", sep="|", encoding="utf-8")
    product["VOCID"] = product["VOCID"].map(lambda x : str(x))
    
    data = pd.merge(data, product, left_on="vocid", right_on = "VOCID", how = "left")
    data.drop("VOCID", axis=1)
    
    return data


def get_product(product_data, tokenizer):
    komoran = Komoran(userdic = arg["product_dictionary"])
    i=0
    
    with open("400.help/tokenizer_product_0428.pickle", "rb") as handle:
        tokenizer = pickle.load(handle)
        word_index = tokenzier.word_index
        
    
    product_list = list(df["상품명"])
    index_list=[]
    
    for product_name in tqdm(product_list):
        sent_token = []
        try :
            pos_list = get_product(product_name, komoran)
            for sent in pos_list:
                try:
                    sent_token.append(word_index[sent])
                except:
                    pass 
            index_list.append(sent_token)
            if len(sent_toke) >= i:
                i = len(sent_token)
                
        except :
            index_list.append([999999])
            
    print("max token length : ", i)
    padding_token = pad_sequences(index_list, maxlen=i,)
    
    return padding_token


def extract_pos(token_list):
    token_flat = []
    
    for cont in tqdm(token_list):
        sent = []
        for sentence in list(cont):
            for word in sentence:
                if word[1] in arg["pos_list"] and word[0] != ".xxx":
                    sent.append(word[0])
                    
        if len(sent) == 0:
            sent.append("unknown")
            
        token_flat.append(sent)
    
    return token_flat


def data_split(data):
    train_data, val_data, train_label, val_label = train_test_split(data,
                                                                    data[arg["label"]], 
                                                                    test_size = arg["sampling_rate"], 
                                                                    stratify = data[arg["label"]], 
                                                                    random_state = 123)
    
    
    return train_data, val_data, train_label, val_label



def word_to_index(token_flat, data_type):
    
    word_index = get_word_index(data_type)
    
    index_list = []
    for sent in tqdm(token_flat):
        sent_token = []
        for token in sent:
            try:
                sent_token.append(word_index[word])
            except:
                pass
            
        index_list.append(sent_token)
        
    return index_list

