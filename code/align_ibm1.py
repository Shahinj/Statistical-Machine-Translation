# from lm_train import *
# from log_prob import *
# from preprocess import *
from math import log
import os

def align_ibm1(train_dir, num_sentences, max_iter, fn_AM):
    """
    Implements the training of IBM-1 word alignment algoirthm. 
    We assume that we are implemented P(foreign|english)
    
    INPUTS:
    train_dir : 	(string) The top-level directory name containing data
                    e.g., '/u/cs401/A2_SMT/data/Hansard/Testing/'
    num_sentences : (int) the maximum number of training sentences to consider
    max_iter : 		(int) the maximum number of iterations of the EM algorithm
    fn_AM : 		(string) the location to save the alignment model
    
    OUTPUT:
    AM :			(dictionary) alignment model structure
    
    The dictionary AM is a dictionary of dictionaries where AM['english_word']['foreign_word'] 
    is the computed expectation that the foreign_word is produced by english_word.
    
            LM['house']['maison'] = 0.5
    """
    AM = {}
    
    # Read training data
    eng_sents, f_sents = read_hansard(train_dir, num_sentences)
    
    #split into tokens
    eng = [i.split(' ') for i in eng_sents]
    fre = [i.split(' ') for i in f_sents]
    
    # Initialize AM uniformly
    am = initialize(eng, fre)
    
    # Iterate between E and M steps
    for iter in range(0,max_iter):
        print('iteration {0}\n'.format(iter))
        # print( top_n_words(am, 'parliament', n = 10))
        # print( top_n_words(am, 'vote', n = 10))
        # print( top_n_words(am, 'unreasonable', n = 10))
        # print( top_n_words(am, 'this', n = 10))
        am = em_step(am, eng,fre)
    
    AM = am
    #Save Model
    with open(fn_AM+'.pickle', 'wb') as handle:
        pickle.dump(AM, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    return AM
    
# ------------ Support functions --------------
def read_hansard(train_dir, num_sentences):
    """
    Read up to num_sentences from train_dir.
    
    INPUTS:
    train_dir : 	(string) The top-level directory name containing data
                    e.g., '/u/cs401/A2_SMT/data/Hansard/Testing/'
    num_sentences : (int) the maximum number of training sentences to consider
    
    
    Make sure to preprocess!
    Remember that the i^th line in fubar.e corresponds to the i^th line in fubar.f.
    
    Make sure to read the files in an aligned manner.
    """
    # TODO
    ##read files
    e_sents = [] 
    f_sents = []
    stop = False
    counter = 0
    all_files = os.listdir(train_dir)
    english_files = [i for i in all_files if i[-1] == 'e']
    french_files = [i for i in all_files if i[-1] == 'f']
    for eng_file in english_files:
        french_file = [i for i in french_files if i[:-1] == eng_file[:-1]]
        if(len(french_file) != 1):
            continue
        
        e_fullFile = os.path.join(train_dir, eng_file)
        f_fullFile = os.path.join(train_dir, french_file[0])
        with open(e_fullFile) as ef:
            with open(f_fullFile) as ff: 
                e_lines = ef.readlines()
                f_lines = ff.readlines()
        
        i = 0
        while(counter < num_sentences and i < len(e_lines) ):
            e_sents.append(preprocess(e_lines[i],'e'))
            f_sents.append(preprocess(f_lines[i],'f'))
            counter += 1
            i += 1
    return (e_sents,f_sents)

def initialize(eng, fre):
    """
    Initialize alignment model uniformly.
    Only set non-zero probabilities where word pairs appear in corresponding sentences.
    eng: a list of sentences, broken down to tokens: [ [w1, w2, w3], [w1,w2,w3] , ...]
    fre: a list of sentences, broken down to tokens: [ [w1, w2, w3], [w1,w2,w3] , ...]
        
    """
    # TODO
    am = {}
    #enforce obvious alignments
    same_in_both = ['SENTSTART', 'SENTEND', '!', '"', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    #uniformly distribute the rest
    for i,sent in enumerate(eng):
        f_sent = fre[i]
        for j,word in enumerate(sent):
            if(word in same_in_both or str.isnumeric(word)):
                am[word] = {word : 1}
                continue
            if word not in am:
                am[word] = {}
            for k,f_word in enumerate(f_sent):
                if(f_word in same_in_both or str.isnumeric(f_word)):
                    continue
                if f_word not in am[word]:
                    am[word][f_word] = 1
    #normalize the counts
    for word in am.keys():
        norm = sum(am[word].values())
        for align in am[word].keys():
            am[word][align] /= norm
    
    return am
    
def em_step(t, eng, fre):
    """
    One step in the EM algorithm.
    Follows the pseudo-code given in the tutorial slides.
    
    eng, fre = a list of sentences, broken down to tokens: [ [w1, w2, w3], [w1,w2,w3] , ...]
    t = lookup table for P(f|e)
    """
    # TODO
    #enforce obvious alignments
    same_in_both = ['SENTSTART', 'SENTEND', '!', '"', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    am = {}
    for i,sent in enumerate(eng):
        f_sent = fre[i]
        for j,word in enumerate(sent):
            if(word in same_in_both or str.isnumeric(word)):
                am[word] = {word : 1}
                continue
            if word not in am:
                am[word] = {}
            for k,f_word in enumerate(f_sent):
                if(f_word in same_in_both or str.isnumeric(f_word)):
                    continue
                if f_word not in am[word]:
                    am[word][f_word] = t[word][f_word]
                else:
                    am[word][f_word] += t[word][f_word]
    #normalize the counts
    for word in am.keys():
        norm = sum(am[word].values())
        for align in am[word].keys():
            am[word][align] /= norm 
            
    return am
    
def top_n_words(am, e_word, n = 10):
    A = am[e_word]
    from collections import Counter
    return dict(Counter(A).most_common(n))
    # return dict(sorted(am[e_word].items(), key=operator.itemgetter(1), reverse=True)[:5])

##test initialize
# eng = [ preprocess('the house','e').split(' '), preprocess('house of commons','e').split(' '), preprocess('Andromeda galaxy','e').split(' ') ]
# fre = [ preprocess('la maison','f').split(' '), preprocess('chambre des communes','f').split(' '), preprocess("galaxie d'Andromede",'f').split(' ') ]
# initialize(eng, fre)

##test read hansard
# a = read_hansard("./data/Hansard/Testing/", 2000)

##test full
train_dir = './data/Hansard/Testing/'
a = align_ibm1(train_dir, float('inf'), 10, './alignment_model')