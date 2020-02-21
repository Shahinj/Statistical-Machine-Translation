# from preprocess import *
# from lm_train import *
from math import log

def log_prob(sentence, LM, smoothing=False, delta=0, vocabSize=0):
    """
    Compute the LOG probability of a sentence, given a language model and whether or not to
    apply add-delta smoothing
    
    INPUTS:
    sentence :	(string) The PROCESSED sentence whose probability we wish to compute
    LM :		(dictionary) The LM structure (not the filename)
    smoothing : (boolean) True for add-delta smoothing, False for no smoothing
    delta : 	(float) smoothing parameter where 0<delta<=1
    vocabSize :	(int) the number of words in the vocabulary
    
    OUTPUT:
    log_prob :	(float) log probability of sentence
    """
    
    #TODO: Implement by student.
    log_prob = 0;

    words = sentence.split(' ')
    for i,word in enumerate(words):
        if(i == 0):
            continue
        wt = word
        wt_1 = words[i-1]
        numerator_addition = 0
        denum_addition = 0
        if(smoothing == True):
            numerator_addition = delta
            denum_addition = delta * vocabSize
        try:
            p_wt_wt_1 = LM['bi'][wt_1][wt]
        except:
            p_wt_wt_1 = 0
        try:
            p_wt_1 = LM['uni'][wt_1]
        except:
            p_wt_1 = 0
        
        if((p_wt_1 + denum_addition) == 0 or (p_wt_wt_1 + numerator_addition) == 0):
            log_prob += float('-inf')
        else:
            log_prob += log( (p_wt_wt_1 + numerator_addition) / (p_wt_1 + denum_addition) ) / log(2)
    return log_prob
    
    
e_LM = pickle.load( open( "./English_Model.pickle", "rb" ) )
f_LM = pickle.load( open( "./French_Model.pickle", "rb" ) )

##compare a bunch of english sentences
with open('./Task3.txt', 'w') as file:
    sent = 'lunch it eat time is.'
    file.write( 'sentence: {0} \nlog_prob: {1}\n'.format(sent,log_prob(preprocess(sent,'e'),LM = e_LM, smoothing = True, delta = 0.1, vocabSize =  len(LM['uni']))))
    
    sent = 'it is time to eat lunch.'
    file.write( 'sentence: {0} \nlog_prob: {1}\n'.format(sent,log_prob(preprocess(sent,'e'),LM = e_LM, smoothing = True, delta = 0.1, vocabSize =  len(LM['uni']))))
    
    ##test perplexity, lower is better
    #lower the smoothing, lower the perplexity but starts increasing after a certain threshold. Lowest happens with no smoothing (?)
    test_dir = './data/Hansard/Testing/'
    deltas = [0, 0.9,0.5,0.1,0.05,0.005,0.0005,0.00005,0.000005]
    languages = ['e','f']
    for lang in languages:
        file.write( 'Language: {0}\n'.format(lang))
        for delta in deltas:
            if(lang == 'e'):
                file.write( 'delta: {0} \t perplexity: {1}\n'.format(delta, preplexity(e_LM, test_dir, lang, smoothing = True, delta = delta) ))
            else:
                file.write( 'delta: {0} \t perplexity: {1}\n'.format(delta, preplexity(f_LM, test_dir, lang, smoothing = True, delta = delta) ))
    
    
    print(preplexity(f_LM, test_dir, "f"))
    print(preplexity(f_LM, test_dir, "f", smoothing = True, delta = 0.9))
    print(preplexity(f_LM, test_dir, "f", smoothing = True, delta = 0.5))
    print(preplexity(f_LM, test_dir, "f", smoothing = True, delta = 0.1))
    print(preplexity(f_LM, test_dir, "f", smoothing = True, delta = 0.05))
    print(preplexity(f_LM, test_dir, "f", smoothing = True, delta = 0.005))
    print(preplexity(f_LM, test_dir, "f", smoothing = True, delta = 0.0005))
    print(preplexity(f_LM, test_dir, "f", smoothing = True, delta = 0.00005))
    print(preplexity(f_LM, test_dir, "f", smoothing = True, delta = 0.000005))