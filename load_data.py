from __future__ import unicode_literals,print_function,division
from io import open
import unicodedata
import string
import re
import random
import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


SOS_token = 0
EOS_token = 1

class Lang:
    def __init__(self,name):
        self.name = name
        self.word2index={}
        self.word2count={}
        self.index2word={0:'SOS',1:'EOS'}
        self.n_words=2
    

    def add_sentence(self,sentence):
        for word in sentence.split(' '):
            self.add_word(word)
    
    def add_word(self,word):
        if word not in self.word2index:
            self.word2index[word]=self.n_words
            self.word2count[word]=1
            self.index2word[self.n_words] = word
            self.n_words+=1
        else:
            self.word2count[word]+=1

def unicode_to_ascii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD',s)
        if unicodedata.category(c)!='Mn'
    )

def normalize_string(s):
    s=unicode_to_ascii(s.lower().strip())
    s=re.sub(r'([.!?])',r' \1',s)
    s=re.sub(r'[^a-zA-Z.!?]+',r' ',s)
    return s

def read_langs(lang1,lang2,reverse=False):
    print('Reading lines...')
    
    #lines=open('data/data/%s-%s.txt'%(lang1,lang2),encoding='utf-8').read().strip().split('\n')

    lines_en=open('en_vidata/train.en',encoding='utf-8')
    lines_vi=open('en_vidata/train.vi',encoding='utf-8')
    lines_en=lines_en.readlines()
    lines_vi=lines_vi.readlines()
    pairs=[]
    for i in range(len(lines_en)):
        tmp_pair=[]
        tmp_pair.append(lines_en[i][:-1])
        tmp_pair.append(lines_vi[i][:-1])
        pairs.append(tmp_pair)


    #pairs=[[normalize_string(s) for s in l.split('\t')] for l in lines_en]

    if reverse:
        pairs=[list(reversed(p)) for p in pairs]
        input_lang=Lang(lang2)
        output_lang=Lang(lang1)
    
    else:
        input_lang=Lang(lang2)
        output_lang=Lang(lang1)
    return input_lang,output_lang,pairs 




MAX_LENGTH = 20
eng_prefixes=('i am ','i m ',
    "he is", "he s ",
    "she is", "she s ",
    "you are", "you re ",
    "we are", "we re ",
    "they are", "they re "
)

def filter_pair(p):
    return len(p[0].split(' '))<MAX_LENGTH and \
        len(p[1].split(' '))<MAX_LENGTH
    ''' and \
        p[1].startswith(eng_prefixes)'''

def filter_pairs(pairs):
    return [pair for pair in pairs if filter_pair(pair)]



def prepare_data(lang1,lang2,reverse=False):
    input_lang,output_lang,pairs=read_langs(lang1,lang2,reverse)
    print('Read %s sentence pairs' % len(pairs))
    pairs=filter_pairs(pairs)
    print('Trimmed to %s sentence pairs' %len(pairs))
    print('Counting words...')
    for pair in pairs:
        input_lang.add_sentence(pair[0])
        output_lang.add_sentence(pair[1])
    
    print("Counted words:")
    print(input_lang.name,input_lang.n_words)
    print(output_lang.name,output_lang.n_words)

    return input_lang,output_lang,pairs


if __name__ == "__main__":
    input_lang,output_lang,pairs=prepare_data('en','vi',True)
    print(random.choice(pairs))


