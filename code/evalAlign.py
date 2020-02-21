#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import _pickle as pickle
import pickle

# import decode
# from align_ibm1 import *
# from BLEU_score import *
# from lm_train import *

__author__ = 'Raeid Saqur'
__copyright__ = 'Copyright (c) 2018, Raeid Saqur'
__email__ = 'raeidsaqur@cs.toronto.edu'
__license__ = 'MIT'


discussion = """
Discussion :

{Enter your intriguing discussion (explaining observations/results) here}

"""

##### HELPER FUNCTIONS ########
def _getLM(data_dir, language, fn_LM, use_cached=True):
    """
    Parameters
    ----------
    data_dir    : (string) The top-level directory continaing the data from which
                    to train or decode. e.g., '/u/cs401/A2_SMT/data/Toy/'
    language    : (string) either 'e' (English) or 'f' (French)
    fn_LM       : (string) the location to save the language model once trained
    use_cached  : (boolean) optionally load cached LM using pickle.

    Returns
    -------
    A language model 
    """
    if(use_cached):
        LM = pickle.load( open( fn_LM+'.pickle', "rb" ) )
    else:
        LM = lm_train(data_dir, language, fn_LM)
    return LM

def _getAM(data_dir, num_sent, max_iter, fn_AM, use_cached=True):
    """
    Parameters
    ----------
    data_dir    : (string) The top-level directory continaing the data 
    num_sent    : (int) the maximum number of training sentences to consider
    max_iter    : (int) the maximum number of iterations of the EM algorithm
    fn_AM       : (string) the location to save the alignment model
    use_cached  : (boolean) optionally load cached AM using pickle.

    Returns
    -------
    An alignment model 
    """
    if(use_cached):
        AM = pickle.load( open( fn_AM+'.pickle', "rb" ) )
    else:
        AM = align_ibm1(data_dir,num_sent,max_iter, fn_AM)
    return AM

def _get_BLEU_scores(eng_decoded, eng, google_refs, n):
    """
    Parameters
    ----------
    eng_decoded : an array of decoded sentences
    eng         : an array of reference handsard
    google_refs : an array of reference google translated sentences
    n           : the 'n' in the n-gram model being used

    Returns
    -------
    An array of evaluation (BLEU) scores for the sentences
    """
    refs = [eng, google_refs]
    scores = [[],[],[]]
    for candidate in eng_decoded:
        score = 0
        for i,ref in enumerate(refs):
            scores[i].append(BLEU_score(candidate, ref, n, brevity=False))
            score += BLEU_score(candidate, ref, n, brevity=False)
        scores[-1].append(score / 2)
    return scores

def main(args):

    #train AM
    num_sents = [1000, 10000, 15000, 30000]
    max_iters = [10,50,100]
    AMs = [ [] for i in range(0,len(num_sents)) ]    #12 AMs with different training set and length of training
    for i,ns in enumerate(num_sents):
        for epoch in max_iters:
            AMs[i].append(_getAM(args.data_dir, ns, epoch, args.fn_AM + 'am_{0}_{1}'.format(ns,epoch), use_cached = False))
    #get LM
    LM = _getLM(args.data_dir, 'e', args.fn_LM + 'lm', use_cached=False)
    
    #get french sentences and preprocess them
    texts = ''
    with open(args.french_loc) as f:
        texts += f.read() + '\n'
    french = [preprocess(i,'f') for i in texts.split('\n') if i != '' ]
    
    #read reference hansard
    hansard = ''
    with open(args.hansard_loc) as f:
        hansard += f.read() + '\n'
    hansard = [i for i in hansard.split('\n')  if i != '' ]
    
    #read reference google
    google = ''
    with open(args.google_loc) as f:
        google += f.read() + '\n'
    google = [i for i in google.split('\n')  if i != '' ]
    
    ## Write Results to Task5.txt (See e.g. Task5_eg.txt for ideation). ##
    f = open("./Task5.txt", 'w+')
    f.write(discussion) 
    f.write("\n\n")
    f.write("-" * 10 + "Evaluation START" + "-" * 10 + "\n")
    for i, AM_list in enumerate(AMs):
        for j,AM in enumerate(AM_list):
            f.write(f"\n### Evaluating AM model: ### \n")
            f.write("\n### Training Size: {0} ### \n".format(num_sents[i]))
            f.write("\n### Training Iterations: {0} ### \n".format(max_iters[j]))
            f.write(f"\n###################################### \n")            
            # Decode using AM #
            english = [decode(u, LM, AM) for u in french]
            # Eval using 3 N-gram models #
            all_evals = []
            for n in range(1, 4):
                f.write(f"\nBLEU scores with N-gram (n) = {n}: \n")
                f.write("\t\t\t{:>30} \t\t {:>30} \t\t {:>30} \n".format("Hansard","Google","Both"))
                evals = _get_BLEU_scores(english, hansard, google, n)
                # for u in range(0,len(english)):
                f.write("\t\t\t{:>30} \t\t {:>30} \t\t {:>30} \n".format(np.mean(evals[0]),np.mean(evals[1]),np.mean(evals[2])))
                    # f.write("Google: \t{0}\n".format(evals[1]))
                    # f.write("Both: \t\t{0}\n".format(evals[2]))
            f.write("\n\n")

    f.write("-" * 10 + "Evaluation END" + "-" * 10 + "\n")
    f.close()
    
    # pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Use parser for debugging if needed")
    args = parser.parse_args()
    
    parser.add_argument("-fl", "--french_loc", help="Path to french location. By default it is set to the cdf directory for the assignment.", default="/u/cs401/A2 SMT/data/Hansard/Testing/Task5.f", required = True)

    parser.add_argument("-dd", "--data_dir", help="Path to data directory.", default="/u/cs401/A2_SMT/data", required = True)
    
    parser.add_argument("-fnam", "--fn_AM", help="Path to save the alignment models.", required = True)
    
    parser.add_argument("-fnlm", "--fn_LM", help="Path to save the language models.", default="/u/cs401/A2 SMT/data/Hansard/Testing/Task5.f", required = True)
    
    parser.add_argument("-hl", "--hansard_loc", help="Path to Hansard. By default it is set to the cdf directory for the assignment.", default="/u/cs401/A2 SMT/data/Hansard/Testing/Task5.e,", required = True)
    
    parser.add_argument("-gl", "--google_loc", help="Path to Google. By default it is set to the cdf directory for the assignment.", default="/u/cs401/A2 SMT/data/Hansard/Testing/Task5.google.e", required = True)
    
    
    ###
    args = parser.parse_args([
    '--french_loc',r'./data/Hansard/Testing/Task5.f',
    '--data_dir', r'./data/Hansard/Testing/',
    '--fn_AM', './AMs/',
    '--fn_LM', './LMs/',
    '--hansard_loc' , './data/Hansard/Testing/Task5.e',
    '--google_loc' , './data/Hansard/Testing/Task5.google.e'])
    ### 

    main(args)
    print('done')
    """
    args must have: 
    french_loc,data_dir,fn_AM,fn_LM,hansard_loc,google_loc
    
    #TODO: Perform outlined tasks in assignment, like loading alignment
    models, computing BLEU scores etc.

    (You may use the helper functions)

    It's entirely upto you how you want to write Task5.txt. This is just
    an (sparse) example.
    """