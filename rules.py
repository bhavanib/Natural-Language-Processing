'''
feature_functions.py
Implements the feature generation mechanism
Author: Anantharaman Narayana Iyer
Date: 21 Nov 2014

6th Dec: Org gazeteer added
7th Dec: 
'''
from nltk import sent_tokenize, word_tokenize
import nltk
import json
import numpy
import pickle
import datetime
import ner_client
from mymaxent import *

disagree_list = ["can't","cannot","don't","irrelevant","problem","issue","not","inconvinient","bad","very","too",
"dont"]
disagree_list1 = [m.lower() for m in disagree_list]
greeting_list = ["morning","gm","hi","hey","hello","bye","ge","gn","evening","night","AfterNoon"]
greeting_list1 = [m.lower() for m in greeting_list]
agreement_list = ["good","best","better than","too","good","many","cheap","fast","simplify","supports","is","has","liked","like"]
agreement_list1 = [m.lower() for m in agreement_list]
acknowledge_list = ["satisfied","thank","you","Thanks","ty","helped","useful","bought","has","costs","well","documented","released"]
acknowledge_list1 = [m.lower() for m in acknowledge_list]

brand_product_bigrams_dict = ner_client.NerClient("1PI11IS","g18").get_brand_product_bigrams_dict()
product_names = []
for v in brand_product_bigrams_dict:
    for v1 in v:
        product_names.append(v1.lower())

product_name_tokens = [] # some time product names may be strings with many words, we will split these so that we can compare it with input word token
for p in product_names:
    product_name_tokens.extend(p.split())


class Rules(object):
    def __init__(self, sents, tag_list):
        self.wmap = {}
        self.flist = {} #[self.f1, self.f2, self.f3, self.f4, self.f5, self.f6, self.f7, self.f8, self.f9, self.f10, self.f11, self.f12, self.f13]
        self.fdict = {}
	#print Rules.__dict__.items()
        for k, v in Rules.__dict__.items():
            if hasattr(v, "__call__"):
                if k[0] == 'r':
                    self.flist[k] = v # .append(v)
                    tag = k[1:].split("_")[0]
                    val = self.fdict.get(tag, [])
                    val.append(v)
                    self.fdict[tag] = val

#	print self.fdict.items()	
        self.supported_tags = ["interest_intent","price_query","feature_query","irrelevant","comparison","disagreement","greeting","agreement","acknowledgement"]        
        return

    def evaluate(self, xi,tag):
        feats = []
	#print "Sentence in evaluate:",xi
	#print "Tag in evaluate:",tag
	#print self.fdict.items()
        for t, f in self.fdict.items():
	    #print "t:",t
	    
            if t == tag:
		#print "True"
                for f1 in f:
	           # print "fns return:",int(f1(self, xi[0]))
                    feats.append(int(f1(self, xi[0])))
            else:
               	for f1 in f:
			
                    feats.append(0)
	
	#print "Feats:",feats
        return feats

    def set_wmap(self, sents): # given a list of words sets wmap
        for i in range(len(sents)):
            self.wmap[i] = {'words': sents[i], 'pos_tags': nltk.pos_tag(sents[i])}
        return

    def check_list(self, clist, w):
        #return 0
        w1 = w.lower()
        for cl in clist:
            if w1 in cl:
                return 1
        return 0

    #------------------------------- Phone tag ---------------------------------------------------------
    # The following is an example for you to code your own functions
    # returns True if wi is in phones tag = Phone
    # h is of the form {'ta':xx, 'tb':xx, 'wn':xx, 'i':xx}
    # self.wmap provides a list of sentences (tokens) where each element in the list is a dict {'words': word_token_list, 'pos_tags': pos_tags_list}
    # each pos_tag is a tuple returned by NLTK tagger: (word, tag)
    # h["wn"] refers to a sentence number
    
    def rdisagreement_1(self, sents):
		sents = sents.split()
		for r in range(1,len(sents)):
			sents[r-1]=sents[r-1].lower()
			if sents[r-1] in disagree_list1:
				return 1					
		return 0

    def rgreeting_1(self, sents):
		sents = sents.split()
		for r in range(1,len(sents)):
			sents[r-1]=sents[r-1].lower()
			if sents[r-1] in greeting_list1:
				return 1					
		return 0


    def ragreement_1(self, sents):
		sents = sents.split()
		for r in range(1,len(sents)):
			sents[r-1]=sents[r-1].lower()
			if sents[r-1] in agreement_list1:
				return 1					
		return 0


    def racknowledgement_1(self, sents):
		sents = sents.split()
		for r in range(1,len(sents)):
			sents[r-1]=sents[r-1].lower()
			if sents[r-1] in acknowledge_list1:
				return 1					
		return 0


    

if __name__ == "__main__":   
	pass
