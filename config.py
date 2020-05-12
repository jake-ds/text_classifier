
config = {
    
    
    # data
    "train_data" : ["train_data_A", "train_data_B"], 
    "test_data" : "test_data",
    "data_info" : "400.help/data_info.txt",
    
    #label
    "label" : "cateCode",
    "cont_only" : False,
    
    # pos
    "pos_list" : ["NNP, NNG", "NNB", "NR", "NP", "VV", "MAG", "SL"],
    
    "voc_argument" : {
        "embedding_model" : "400.help/voc_w2v_mdl.model",
        "word_index" : "400.help/voc_tokenizer.pickle",
        "dictionary" : "300.dictionary/voc_dictionary.txt",
        "MAX_NB_WORDS" : 50000,
        "EMBEDDING_DIM" : 100},
    
    "product_argument" : {
        "embedding_model" : "400.help/product_w2v_mdl.model",
        "word_index" : "400.help/product_tokenizer.pickle",
        "dictionary" : "300.dictionary/product_dictionary.txt",
        "MAX_NB_WORDS" : 50000,
        "EMBEDDING_DIM" : 100},
    
    #padding
    "title_padding" : 20, 
    "cont_padding" : 100,
    
    "MAX_SEQUENCE_LENGTH" : 200,
    "sampling_rate" : 0.2,
    
    #model
    "epochs" : 500, 
    "batch_size" : 1000}


def get():
    return config