# -*- coding: utf-8 -*-
"""
Created on Fri May 20 08:49:59 2022

@author: mohamedk
"""
#USAGE: python3 classify.py <query_file>
import sys
import numpy as np
import webbrowser
from tkinter import *
from math import sqrt
from os import listdir
from os.path import isfile, isdir, join


def cosine_similarity(v1, v2):
    num = np.dot(v1, v2)
    den_a = np.dot(v1, v1)
    den_b = np.dot(v2, v2)
    return num / (sqrt(den_a) * sqrt(den_b))

def read_vocab():
    with open('./data/vocab_file.txt','r',encoding="utf-8") as f:
        vocab = f.read().splitlines()
    return vocab

def read_queries(query_file):
    with open(query_file) as f:
        queries = f.read().splitlines()
    return queries

def read_category_vectors():
    vectors = {}
    f = open('./data/category_vectors.txt','r',encoding="utf-8")
    for l in f:
        l = l.rstrip('\n')
        fields = l.split()
        cat = fields[0]
        vec = np.array([float(v) for v in fields[1:]])
        vectors[cat] = vec
    return vectors

def get_ngrams(l,n):
    l = l.lower()
    ngrams = {}
    for i in range(0,len(l)-n+1):
        ngram = l[i:i+n]
       # print (ngram)
        if ngram in ngrams:
            ngrams[ngram]+=1
        else:
            ngrams[ngram]=1
    return ngrams

def normalise_tfs(tfs,total):
    for k,v in tfs.items():
        tfs[k] = v / total
    return tfs

def mk_vector(vocab,tfs):
    vec = np.zeros(len(vocab))
    for t,f in tfs.items():
        if t in vocab:
            pos = vocab.index(t)
            vec[pos] = f
    return vec

vocab = read_vocab()
print(len(vocab))
vectors = read_category_vectors()





#######################################################
###
def submit():
    searchinput = entry.get()
    f = open("query_file.txt", "w")
    f.write(searchinput+"\n")
    f.close()
 
    return searchinput
####
####
window=Tk()
submit=Button(window,text="submit",command=submit)
submit.pack(side=RIGHT)
entry =Entry()
entry.config(font=('Ink Free',50))
entry.config(bg='#111111')
entry.config(fg='#00FF00')
entry.config(width=20)
entry.pack()
window.mainloop()
####################################





queries = read_queries("query_file.txt")
linkList = [] 

for q in queries:
    print("\nQUERY:",q)
    print ('\n\n\n\n\n\n')
    ngrams = {}
    cosines = {}
    for i in range(4,7):
        n = get_ngrams(q,i)
        ngrams = {**ngrams, **n}
    qvec = mk_vector(vocab,ngrams)
    for cat,vec in vectors.items():
        cosines[cat] = cosine_similarity(vec,qvec)
    for cat in sorted(cosines, key=cosines.get, reverse=True):
       # print(cat,cosines[cat])
        pp = cat.replace('./data/categories','')
        pp = pp[1:]
        if cosines[cat] > 0 :
                print('\n\n\ start')
                print(pp,cosines[cat])
                print('\n\n\ end ')
                ### loop for all ngrma in leaner
       
        
                d = './data/categories'
                catdirs = [join(d,o) for o in listdir(d) if isdir(join(d,o))]
                ccc= "./data/categories/"+pp;
                searchArray = {}
                
                for i in range(4,7):
                    searchArray = get_ngrams(q,i)
                    
                    
                pageTitle = {}
                privous=""
                f = open(join(ccc,'linear.txt'),'r',encoding="utf-8")
                for l in f:
                    
                    if "<doc id" not in l and "</doc" not in l:
                        
                        l = l.rstrip('\n').lower()
                        for kk in searchArray:
                             
                            if kk in l:
                                if privous in pageTitle:
                                    pageTitle[privous]+=1
                                else:
                                    pageTitle[privous]=1
                               
                           
                            
                            
                            
                            
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
                for abc in sorted(pageTitle, key=pageTitle.get, reverse=True):
                    strx ='https://en.wikipedia.org/wiki/'+abc.replace(" ","_") 
                    linkList.append(strx)
                    print(strx)
                     


##############################
def callback(url):
    webbrowser.open_new(url)

root = Tk()

for x in linkList :
    link1 = Label(root, text=x, fg="blue", cursor="hand2")
    link1.pack()
    link1.bind("<Button-1>", lambda e: callback(x))


root.mainloop()




#####################
            
"""
ngramfile = open(join(cat,"linear."+str(n)+".ngrams"),'w',encoding="utf-8")
for k in sorted(ngrams, key=ngrams.get, reverse=True):
ngramfile.write(k+'\t'+str(ngrams[k])+'\n')
ngramfile.close() 
""" 
            
                
        
        
        
        
        
        
        
    
