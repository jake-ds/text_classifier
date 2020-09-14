config = {
    "MODEL_DIR" : "Desktop/User/text_classifier_v2",
    "data_fname" : {"train" : "./data/train/train.csv", 
                    "validation" : "./data/validation/validation.csv", 
                    "test" : "./data/test/test/csv"},
    
    "dictionary_path" : "./dictionary/base_dictionary.txt",
    "vocab_size" : 50000,
    
    "label" : "label",
    
    "contents_arg" : {"embedding_model" : "./help/word2vec_contents.model",
                      "word_index" : "./help.tokenizer_contents.pickle",
                      "pos_list" : ["NNP", "NNG", "NNB", "NR", "XPN", "NP", "VV", "MAG", "SL"],
                      "MAX_NB_WORDS" : 50000,
                      "EMBEDDING_DIM" : 100},
    
    "product_arg" : {"embedding_model" : "./help/word2vec_product.model",
                      "word_index" : "./help.tokenizer_product.pickle",
                      "MAX_NB_WORDS" : 50000,
                      "EMBEDDING_DIM" : 100},
    
    "padding_size" : {"title_pad_len" : 20, 
                      "cont_pad_len" : 120,
                      "product_pad_len" : 15},
    
    "codeInfo_fname": {"M" : "./data/code_info/code_info_M.txt", 
                       "S": "./data/code_info/code_info_S.txt"},
    
    "model_path" : {"H-LSTM" : "./data/model/H-LSTM"}, 
    
    "epochs" :100,
    "batch_size" : 2000
}


def get():
    return config

def show_config(config):
    def dict_pring(dict_item):
        print("{key} : {value}".format(key=dict_item[0], value=dict_item[1]))
        
    for item in config.items():
        if type(item[1]) ==dict:
            print("="*20)
            print(item[0])
            print("="*20)
            
            for item in item[1].items():
                dict_print(item)
            print("="*20)
            
        else:
            dict_print(item)