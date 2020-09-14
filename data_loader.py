import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequence
from konlpy.tag import Komoran
from gensim.models import Word2Vec

from utils import *

class data_loader(object):
    def __init__(self, arg):
        self.arg = arg
        self.MODEL_DIR = self.arg["MODEL_DIR"]
        self.tokenizer = load_tokenizer()
        
    def add_catg_M(self, df):
        """
        middle-category code extraction
        label : LL/MM/SS (int)
        """
        return list(df[self.arg["label"]].map(lambda x : int(str(x)[:4])))
    
    def tokenizer(self, data, tokenizer):
        """
        tokenizer : Komoran using user dictionary
        if data has "\r" or "\n", komoran doesn't work
        """
        try : 
            result = tokenizer.pos(data)
        except:
            result = tokenizer.pos("-")
            
        return result
    
    def extract_pos(self, data, pos_list=None):
        """
        extract words using given pos-tag list
        if pos-tag list not given, extract all words
        """
        
        if pos_list != None:
            return [x[0] for x in data if x[1] in pos_list]
        
        else:
            return [x[0] for x in data]

    def word_to_index(self, data, word_index_fname):
        """
        this function convert word to index using trained model
        """
        word_index = load_word_index(word_index_fname)
        word_list = word_index.keys()
        
        return [word_index[word] for word in data if word in word_list]
    
    def padding(self, data, pad_len=None):
        """
        zero padding for resizing input sequence
        """
        
        if pad_len <= len(data):
            return data[:pad_len]
        else:
            return [0] * (pad_len - len(data)) + data
        
    def get_dummmy_label(self, label_list, codeInfo_fname):
        """
        label dummirise  
        """
        
        code_info = load_code_info(codeInfo_fname)
        label_list = pd.Series(label_list).astype("category", categories = list(code_info["code"]))
        label_array = np.asarray(pd.get_dummies(label_list))
        
        return label_array
    
    def set_label(self, df):
        """
        set label : mid, small category
        """
        
        y_M = self.add_catg_M(df)
        y_S = list(df[self.arg["label"]])
        
        y_M = self.get_dummy_label(y_M, self.MODEL_DIR + self.arg["codeInfo_fname"]["M"])
        y_S = self.get_dummy_label(y_S, self.MODEL_DIR + self.arg["codeInfo_fname"]["S"])
        
        return y_M, y_S
        