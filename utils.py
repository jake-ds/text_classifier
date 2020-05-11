import ujon
import pandas as pd
import numpy as np
import config
import pickle

from gensim.models import Word2Vec
from tqdm import tqdm


arg = config.get()


# 정리된 데이터셋 확인
def show_dataset():
    data_info = pd.read_csv(arg["data_info"], sep="|")
    return data_info

# 개별 데이터로딩
def load_idv_data(data_name, custom=False):
    
    data_info = show_dataset()
    print("data loading : " + data_name)
    if custom == True:
        data_path = data_name
        
    else:
        data_folder = "100.data/" + list(data_info[data_info["name"]==data_name]["path"])[0]
        data_path = data_folder + "/" + data_name + ".json"
        
    
    loaded_data = []
    with open(data_path, "r", encoding ="utf-8") as data_file:
        for line in data_file:
            doc_obj = ujson.loads(line.strip())
            loaded_data.append(doc_obj)
        data = pd.DataFrame.from_dict(loaded_data)
            
    data = data[~data["cateCode"].isin(["nan"])]
    
    return data

# 전체 데이터로딩
def load_data():
    
    ## load train data
    train_data = pd.DataFrame()
    for train in arg["train_data"]:
        train = load_idv_data(train)
        train_data = pd.concat([train_data, train], axis=0)
        
    print("=" * 50)
    print("train data loaded...")
    print("=" * 50)
    
    ##load test data
    test_data = load_idv_data(arg["test_data"])
    
    return train_data, test_data

def get_token_embedding_argument(data_type):
    
    if data_type == "voc":
        tk_emb_arg = arg["voc_argument"]
    elif data_type == "product":
        tk_emb_arg = arg["product_argumnet"]
    else:
        print("check your data type. only available <voc> or <product>")
        
    return tk_emb_arg

def get_word_index(data_type):
    
    tk_emb_arg = get_token_embedding_argument(data_type)
    
    with open(tk_emb_arg["word_index"], 'rb') as handle:
        tokenizer = pickle.load(handle)
        
        return tokenizer.word_index
    

def get_word_embedding(data_type):
    
    tk_emb_arg = get_token_embedding_argument(data_type)
    
    return Word2Vec.load(tk_emb_arg["embedding_model"])

def get_embedding_matrix(data_type):
    
    tk_emb_arg = get_token_embedding_argument(data_type)
    
    word_index = get_word_index(data_type)
    w2v_mdl = get_word_embedding(data_type)
    
    MAX_NB_WORDS = tk_emb_arg["MAX_NB_WORDS"]
    EMBEDDING_DIM = tk_emb_arg["EMBEDDING_DIM"]
    
    embedding_matrix = np.random.randn(MAX_NB_WORDS, EMBEDDING_DIM)
    for word in word_index:
        if word in w2v_mdl and word_index[word] < MAX_NB_WORDS:
            embedding_matrix[word_index[word]] = w2v_mdl[word]
            
    return embedding_matrix

def save_prd_word_emb_mdl(data, file_name="tmp"):
    
    flat_list = []
    product_list = list(data["상품명"])
    
    for product in product_list:
        try:
            product_pos = komoran.pos(product)
            token_list = []
            for token in product_pos:
                if token[0] in (["(", ")", "."]) or token[0].isdigit():
                    pass
                else:
                    token_list.append(token[0])
                    
        except:
            flat_list.append(["unknown"])
        
        flat_list.append(token_list)
        
    
    product_w2v_mdl = Word2Vec(flat_list, size=100, window=3, min_count=10, workers=4)
    product_w2v_mdl.save(file_name + ".model")
    
    
    