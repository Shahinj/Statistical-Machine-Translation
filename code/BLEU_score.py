import math

def BLEU_score(candidate, references, n, brevity=False):
        """
    Calculate the BLEU score given a candidate sentence (string) and a list of reference sentences (list of strings). n specifies the level to calculate.
    n=1 unigram
    n=2 bigram
    ... and so on
    
    DO NOT concatenate the measurments. N=2 means only bigram. Do not average/incorporate the uni-gram scores.
    
    INPUTS:
        sentence :(string) Candidate sentence.  "SENTSTART i am hungry SENTEND"
        references:(list) List containing reference sentences. ["SENTSTART je suis faim SENTEND", "SENTSTART nous sommes faime SENTEND"]
n :(int) one of 1,2,3. N-Gram level.

        
        OUTPUT:
        bleu_score :(float) The BLEU score
        """

        #TODO: Implement by student.
        #remove SOS and EOS
        candidate = candidate.replace('SENTEND','')
        candidate = candidate.replace('SENTSTART','')
        
        references = [i.replace('SENTEND','') for i in references]
        references = [i.replace('SENTSTART','') for i in references]
        
        if(brevity == False):
                bp = 1
        else:
                c_i = len(candidate.split(' '))
                closest = len(references[0].split(' '))
                for i in references:
                        if( abs( c_i - len(i.split(' ')) ) < abs(c_i - closest)):
                                closest = len(i.split(' '))
                brevity = closest / c_i
                if(brevity < 1):
                        bp = 1
                else:
                        bp = math.exp(1-brevity)
                
        pp = []
        for i in range(1,n+1):
                #get the n-grams for both references and candidates
                candidate_n_gram = []
                candidate_tokenize = candidate.split(' ')
                for j in range(0,len(candidate_tokenize) - (i-1)):
                        candidate_n_gram.append( ' '.join( candidate_tokenize[j:j+i] ) )
                
                #get reference_n_grams
                references_n_gram = [ [] for k in range(0,len(references)) ]
                for k, ref in enumerate(references):
                        reference_tokenize = ref.split(' ')
                        for j in range(0,len(reference_tokenize) - (i-1)):
                                references_n_gram[k].append( ' '.join( reference_tokenize[j:j+i] ) )
                
                
                N = len(candidate_n_gram)
                C = 0
                for word in candidate_n_gram:
                        for k, ref in enumerate(references_n_gram):
                                if(word in ref):
                                        C += 1
                                        break
                        
                pp.append( C/N )
                
        bleu_score = 1
        for p in pp:
                bleu_score *= p
        
        bleu_score = bleu_score ** (1/n)
        bleu_score *= bp
        
        return bleu_score

#test
# reference = '''\
# it is a guide to action that ensures that the military will always heed party commands'''.strip()
# references = [reference]
# candidate = '''\
# it is a guide to action which ensures that the military always obeys the commands of the party'''.strip()
# print(BLEU_score(candidate, references, 1, brevity=False))
# print(BLEU_score(candidate, references, 2, brevity=False))
# print(BLEU_score(candidate, references, 2, brevity=True))
