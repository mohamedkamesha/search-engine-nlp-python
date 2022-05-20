#USAGE: python3 ngrams.py <ngram size>

import sys
import re
from os import listdir
from os.path import isfile, isdir, join

    

d = './data/categories'
catdirs = [join(d,o) for o in listdir(d) if isdir(join(d,o))]
n = 6

for cat in catdirs:
    ngrams = {}
    pageTitle = {}
    privous=""
    f = open(join(cat,'linear.txt'),'r',encoding="utf-8")
    for l in f:
        
        if "<doc id" not in l and "</doc" not in l:
            
            l = l.rstrip('\n').lower()
            for i in range(len(l)-n+1):
                ngram = l[i:i+n]
                
               # print(ngram)
                if ngram in ngrams:
                    ngrams[ngram]+=1
                else:
                    ngrams[ngram]=1
                
                
                
                
        elif "</doc" not in l :
            pp = l.rstrip('\n').lower()
            pp = pp.replace('<doc id="','')
            for x in pp:
                if(x.isdigit()):
                    pp=pp.replace(x,'')
            pp = pp.replace('" title="','')
            pp = pp.replace('">','')
  
           # print(pp)
            privous=pp
                
    f.close()

    ngramfile = open(join(cat,"linear."+str(n)+".ngrams"),'w',encoding="utf-8")
    for k in sorted(ngrams, key=ngrams.get, reverse=True):
        ngramfile.write(k+'\t'+str(ngrams[k])+'\n')
    ngramfile.close() 
