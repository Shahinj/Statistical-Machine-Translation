# from preprocess import *
import pickle
import os

def lm_train(data_dir, language, fn_LM):
    """
    This function reads data from data_dir, computes unigram and bigram counts,
    and writes the result to fn_LM
    
    INPUTS:
    
    data_dir	: (string) The top-level directory continaing the data from which
                    to train or decode. e.g., '/u/cs401/A2_SMT/data/Toy/'
    language	: (string) either 'e' (English) or 'f' (French)
    fn_LM		: (string) the location to save the language model once trained
    
    OUTPUT
    
    LM			: (dictionary) a specialized language model
    
    The file fn_LM must contain the data structured called "LM", which is a dictionary
    having two fields: 'uni' and 'bi', each of which holds sub-structures which 
    incorporate unigram or bigram counts
    
    e.g., LM['uni']['word'] = 5 		# The word 'word' appears 5 times
            LM['bi']['word']['bird'] = 2 	# The bigram 'word bird' appears 2 times.
    """
    
    # TODO: Implement Function
    LM = {'uni':{}, 'bi':{}}
    ##read files
    texts = '' 
    for subdir, dirs, files in os.walk(data_dir):
        for file in files:
            if(file[-2:] != '.{0}'.format(language)):
                continue
            fullFile = os.path.join(subdir, file)
            with open(fullFile) as f:
                texts += f.read() + '\n'
    
    ##create uni and bi grams        
    for sentence in texts.split('\n'):
        if(len(sentence) == 0):
            continue
        words = preprocess(sentence, language).split(' ')
        for i,word in enumerate(words):
            #unigram counts
            if word in LM['uni']:
                LM['uni'][word] += 1
            else:
                LM['uni'][word] = 1
            
            if (i+1 < len(words)):
                if word in LM['bi']:
                    if(words[i+1] in LM['bi'][word]):
                        LM['bi'][word][words[i+1]] += 1
                    else:
                        LM['bi'][word][words[i+1]] = 1
                else:
                    LM['bi'][word] = {}
                    LM['bi'][word][words[i+1]] = 1
    
    language_model = LM
    #Save Model
    with open(fn_LM+'.pickle', 'wb') as handle:
        pickle.dump(language_model, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    return language_model
    
    
# lm_train('./data/Hansard/Training/', 'e', './English_Model')
# lm_train('./data/Hansard/Training/', 'f', './French_Model')
