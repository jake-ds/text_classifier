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

def data_split(data):
    train_data, val_data, train_label, val_label = train_test_split(data,
                                                                    data[arg["label"]], 
                                                                    test_size = arg["sampling_rate"], 
                                                                    stratify = data[arg["label"]], 
                                                                    random_state = 123)
    
    
    return train_data, val_data, train_label, val_label


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


def get_product_token(df):
    komoran = Komoran(userdict = arg["product_argument"]["dictionary"])
    i =0
    
    with open(arg["product_argument"]["word_index"], 'rb') as handle:
        tokenizer = pickle.load(handle)
        word_index = tokenizer.word_index
        
    product_list = list(df["상품명"])
    index_list = []
    
    for product_name in tqdm(product_list):
        sent_token = []
        try : 
            pos_list = get_product(product_name, komoran)
            for sent in pos_list:
                try:
                    sent_token.append(word_index[sent])
                except:
                    pass
            index_list.append(word_index[sent])
            if len(sent_token) >=i:
                i = len(sent_token)
        except:
            index_list.append([999999])
            
    print("maz token length : ", i)
    padding_token = pad_sequences(index_list, maxlen=i, )
    
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


def padding(index_list, pad_len):
    
    padding_token = pad_sequences(index_list, maxlen=pad_len,)
    
    return padding_token
    
    
def word_to_padding_index(data, cont_only):
    
    data_list = [data["moprh_anal_title"], data["morph_anal_cont"]]
    pad_len_list = [arg["title_padding"], arg["cont_padding"]]
    
    #제목을 input으로 활용하지 않을 경우
    if cont_only:
        data_list = [data["morph_anal_cont"]]
        pad_len_list = [arg["cont_padding"]]
        
        
    converted_data =[]
    for token_list, pad_len in zip(data_list, pad_len_list):
        extracted_data = extract_pos(token_list)
        index_data = word_to_index(extracted_data)
        padded_data = padding(index_data, pad_len)
        converted_data.append(padded_data)
        
    
    flat_converted_data = []
    
    for i in range(len(converted_data[0])):
        tmp = []
        for data in converted_data:
            tmp = tmp + list(data)
        flat_converted_data.append(tmp)
        
    return flat_converted_data


def get_dummy_label(data):
    label_L = pd.get_dummies(data["cateCodeL"])
    label_M = pd.get_dummies(data["cateCodeM"])
    label_S = pd.get_dummies(data["cateCode"])
    
    return label_L, label_M, label_S


def label_check(train_label, val_label, test_label):
    flag = False
    
    if list(train_label.columns).sort() != list(val_label.columns).sort():
        print("train/validation label doesn't matched...")
        flag = True
    else:
        pass
        
    if list(train_label.columns).sort() != list(test_label.columns).sort():
        print("train/test label doesn't matched...")
        flag = True
    else:
        pass
        
    if list(val_label.columns).sort() != list(test_label.columns).sort():
        print("validation/test label doesn't matched...")
        flag = True
    else:
        pass
        
    
    if flag == False:
        print("="*60)
        print("label count : " + str(len(list(train.columns))))
        print("label check success")
        print("="*60)
        
    else:
        print("="*60)
        print("check your label")
        print("="*60)
        
        
def preprocessing_pipeline(data):
    
    title_pad_len = arg["title_padding"]
    cont_pad_len = arg["cont_padding"]
    
    conts = list(data["morph_anal_cont"])
    conts = extract_pos(conts)
    conts = word_to_index(conts, "voc")
    conts = padding(conts, cont_pad_len)
    

    titles = list(data["morph_anal_title"])
    titles = extract_pos(titles)
    titles = word_to_index(titles, "voc")
    titles = padding(titles, title_pad_len)
    
    total_concat_list = []
    
    for cont, title in zip(conts, titles):
        concat_list = list(cont) + list(title)
        total_concat_list.append(concat_list)
        
    concat_array = np.asarray(total_concat_list)
    
    return concat_array
     

# test set이 별도로 주어질 떄, data 전처리 pipeline
def set_data():
    train_data, test_data = load_data()
    
    # product info merge
    train_data = merge_product_info(train_data)
    test_data = merge_product_info(test_data)
    
    # 대분류, 중분류 columns생성
    train_data = add_cateCodeLM(train_data)
    test_data = add_cateCodeLM(test_data)
    
    # 데이터 split
    train_data, val_data, train_label_S, val_label_S = data_split(train_data)
    
    # get product token data 
    train_product_data = get_product_token(train_data)
    val_product_data = get_product_token(val_data)
    test_product_data = get_product_token(test_data)
    
    # get label
    train_label_L, train_label_M, train_label_S = get_label(train_data)
    val_label_L, val_label_M, val_label_S = get_label(val_data)
    test_label_L, test_label_M, test_label_S = get_label(test_data)
    
    #label check
    label_check(train_label_L, val_label_L, test_label_L)
    label_check(train_label_M, val_label_M, test_label_M)
    label_check(train_label_S, val_label_S, test_label_S)
    
    #preprocessing pipeline
    preprc_train_data = preprocessing_pipeline(train_data)
    preprc_val_data = preprocessing_pipeline(val_data)
    preprc_test_data = preprocessing_pipeline(test_data)
    
    return train_label_L, train_label_M, train_label_S, val_label_L, val_label_M, val_label_S, test_label_L, test_label_M, test_label_S, train_product_data, val_product_data, test_product_data, preprc_train_data, preprc_val_data, preprc_test_data, test_data

        
        
        
        