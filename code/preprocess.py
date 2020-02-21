import re

def preprocess(in_sentence, language):
    """ 
    This function preprocesses the input text according to language-specific rules.
    Specifically, we separate contractions according to the source language, convert
    all tokens to lower-case, and separate end-of-sentence punctuation 

    INPUTS:
    in_sentence : (string) the original sentence to be processed
    language	: (string) either 'e' (English) or 'f' (French)
        Language of in_sentence
    OUTPUT:
    out_sentence: (string) the modified sentence
    """
    # TODO: Implement Function
    
    ##define lists to use
    french_no_change = ["d'abord", "d'accord", "d'ailleurs", "d'habitude"]
    vowels = ['A','E','I','O','U']
    vowels = vowels + [str.lower(i) for i in vowels]
    puncs = ['.','!','?',',',':',';','(',')','-','#','$','%','^','*','+','=','<','>','"']
    
    
    ##apply preprocessing that is shared for both languages (punctuations)
    in_sentence = ''.join([i if i not in puncs else ' {0} '.format(i) for i in in_sentence ])
    #remove duplicate spaces
    in_sentence = in_sentence.strip()
    in_sentence = re.sub(r'\s+',' ',in_sentence)
    out_sentence = 'SENTSTART '
    
    
    ##apply individual preprocessing for each language
    if(language == 'e'):
        #nothing special for english
        for word in in_sentence.split(' '):
            out_sentence += ' {0} '.format(word)
    elif(language == 'f'):
        for word in in_sentence.split(' '):
            if len(word) == 0:
                continue
            if word in french_no_change or word in puncs or str.isnumeric(word) or len(word) < 2:
                out_sentence += ' {0} '.format(word)
            else:
                try:
                    if(word[:3] == "l'e" or word[:3] == "l'a"):
                        out_sentence += ' {0} {1} '.format("l'", word[2:])
                    elif(word[0] not in vowels and word[1] == "'"):
                        out_sentence += ' {0} {1} '.format(word[:2], word[2:])
                    elif(word[0:3]  == "qu'"):
                        out_sentence += ' {0} {1} '.format(word[:3], word[3:])
                    elif(word[-3:] == "'on" or word[-3:] == "'il"):
                        out_sentence += ' {0} {1} '.format(word[:-2], word[-2:])
                    else:
                        out_sentence += ' {0} '.format(word)
                except:
                    print('hi')
    else:
        pass
    
    #add end of sentence 
    out_sentence += ' SENTEND'
    #remove duplicate spaces
    out_sentence = out_sentence.strip()
    out_sentence = re.sub(r'\s+',' ',out_sentence)
    return out_sentence

# print(preprocess("following French words should not be separated: l'election l'asb !!!",'e'))
# print(preprocess("je t'aime.", "f"))
# print(preprocess("following French words should not be separated: d'abord, d'accord, d'ailleurs, d'habitude d'abord !!!",'f'))
# print(preprocess("l'election l'asb hi !!!",'f'))
# print(preprocess("je t'aime j'ai I h'lo u'no !!!",'f'))
# print(preprocess("qu'on qu'il puisqu'on lorsqu'il",'f'))
