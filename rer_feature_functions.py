'''
feature_functions.py
Implements the feature generation mechanism for RER
'''

from nltk import sent_tokenize, word_tokenize
import nltk
import json
import numpy
import pickle
import datetime
import ner_client
import ast
from mymaxent import MyMaxEnt


#lists tags
phones = ["phone", "phones", "smartphone", "smartphones", "mobile", "tablet", "tablets", "phablet", "phablets"]
org_list = ['Samsung', 'Apple', 'Microsoft', 'Nokia', 'Sony', 'LG', 'HTC', 'Motorola', 'Huawei', 'Lenovo', 'Xiaomi', 'Acer', 'Asus', 'BlackBerry', 'Alcatel', 'ZTE', 'Toshiba', 'Vodafone', 'T-Mobile', 'Gigabyte', 'Pantech', 'XOLO', 'Lava', 'Micromax', 'BLU', 'Spice', 'Prestigio', 'verykool', 'Maxwest', 'Celkon', 'Gionee', 'vivo', 'NIU', 'Yezz', 'Parla', 'Plum']
org_list1 = [m.lower() for m in org_list]
os_list = ["iOS", "Android", "Windows", "Symbian", "Bada", "Unix", "Linux", "Ubuntu", "OS", "RIM", "Firefox"]
os_list1 = [m.lower() for m in os_list]
currency_symbols = ["rs", "inr", "$", "usd", "cents", "rupees"]
size_list = ["inch", "cm", "inches", "cms", r'"', "''", "pixel", "px", "mega", "gb", "mb", "kb", "kilo", "giga", "mega-pixel", " Front Camera", "Rear Camera", "Dual SIM", "Flash Light", "Built-in", "Screen", "Display", "Memory", "Battery", "RAM"]
size_list1 = [m.lower() for m in size_list]
version_list = ["Kitkat", "Ice Cream Sandwich", "Lollipop", "Jelly Bean", "Ginger Bread", "Grand", "S4", "mini", "S5", "Note 3", "Ace", "Z3", "A065"]
version_list1 = [m.lower() for m in version_list]
family_list = ["Galaxy", "Moto", "Nexus", "Titanium", "Unite", "Torch", "Bolt", "Desire", "Redmi", "Lumia"]
family_list1 = [m.lower() for m in family_list]
other_list = ["I","me","want","a","new","release","Bangalore","Mumbai","market","Thailand","USA","Switzerland","India",
"China","Dubai","California","US","Arab","Kenya","November","month","Dec","week","tomorrow","January","Febraury","March","April","May","June","July","August","September","October","app","Whatsapp","Facebook","TrueCaller","Angry Birds","Twitter","Google","Maps","GPS","are"]
other_list = [m.lower() for m in other_list]


#lists relations
interests = ["looking","buy","need","buying","interested"]
price = ["cost","price","amount","below","under","<","less","more"]
feature = ["dual","camera","sim","battery","screen","cpu","ram","processor","display","speakers"]
compare = ["between","without","compare","compared","better","difference"]

brand_product_bigrams_dict = ner_client.NerClient("1PI11IS022","g18").get_brand_product_bigrams_dict() # use the web service from Ner_client to get this: ner.get_brand_product_bigrams() # gazeteer based 7th Dec 2014
product_names = []
for v in brand_product_bigrams_dict:
    for v1 in v:
        product_names.append(v1.lower())

product_name_tokens = [] # some time product names may be strings with many words, we will split these so that we can compare it with input word token

class FeatureFunctions(object):
	def __init__(self,di={},supported_tags=[]) :
		self.di = di
		self.supported_tags = supported_tags
		



		self.flist = {} #[self.f1, self.f2, self.f3, self.f4, self.f5, self.f6, self.f7, self.f8, self.f9, self.f10, self.f11, self.f12, self.f13]
        	self.fdict = {}
        	for k, v in FeatureFunctions.__dict__.items():
        	    if hasattr(v, "__call__"):
        	        if k[0] == 'f':
        	            self.flist[k] = v # .append(v)
        	            tag = k[1:].split("Z")[0]
        	            val = self.fdict.get(tag, [])
        	            val.append(v)
        	            self.fdict[tag] = val
		#print self.fdict.items()
        	self.supported_tags = ["interest_intent","price_query","feature_query","irrelevant","comparison","disagreement","greeting","agreement","acknowledgement"]        
        	return

	##################FUNCTIONS####################

	def finterest_intentZ1(self,sent,tag) :
		sent = sent.split()
		for i in sent:
			i = i.lower()
			if i in interests :
				return 1
		return 0

	def finterest_intentZ2(self,sent,tag) :
		if(sent in self.di) :
			for x in self.di[sent]:
					for i in x:
						if (("Org" in x[i] and "Model" in x[i]) or "Family" in x[i]):
							return 1
		return 0

        def fprice_queryZ1(self,sent,tag) :
		sent = sent.split()
		for i in sent:
			i = i.lower()
			if ((i in price) or (i in currency_symbols)):
				return 1
		return 0
 
	def fprice_queryZ2(self,sent,tag) :
		if(sent in self.di):
			for x in self.di[sent]:
				for i in x:
					if (("Model" in x[i] or "Org" in x[i] or "Family" in x[i]) and ("Phone" in x[i])):
						return 1
		return 0

	def ffeature_queryZ1(self,sent,tag):
		sent = sent.split()
		for i in sent:
			i = i.lower()
			if i in feature:
				return 1
		return 0
	
	def ffeature_queryZ2(self,sent,tag):
		if(sent in self.di):
			for x in self.di[sent]:
				for i in x:
					if "Feature" in x[i] or "Size" in x[i] :
						return 1
		return 0
	
	def firrelevantZ1(self,sent,tag):
		
		sent1 = sent.split()
		for i in sent1:
			i = i.lower()
			if i in other_list:
				return 1
		return 0
		
	def firrelevantZ2(self,sent,tag):
		if(sent in self.di):
			for x in self.di[sent]:
				for i in x:
					if (("Other" in x[i]) or (len(x[i]) == 0)):
						return 1
					
						
		return 0
	
	def fcomparisonZ1(self,sent,tag):
		sent=sent.split()
		for i in sent:
			i = i.lower()
			if i in compare:
				return 1
		return 0

	def fcomparisonZ2(self,sent,tag):
		if(sent in self.di):
				for x in self.di[sent]:
					for i in x:
						if ((x[i].count("Model") >1) or (x[i].count("Org") >1) or (x[i].count("Family")>1)):
							return 1
		return 0

	def evaluate(self,sent,tag):
		feats = []
		for t,f in self.fdict.items() :
			#print "t:",t,"tag:",tag
			if(t==tag):
			#	print "f:",f
				for f1 in f:
					#print "ffns true"
					#print "return from ffns:",int(f1(self,sent[0],tag))	
				#	print "In evaluate :",sent
					feats.append(int(f1(self,sent,tag)))
					
			else:
				for f1 in f:
					#print "ffns false"
					feats.append(0)
		#print "feats:",feats
		return feats

if __name__ == "__main__":
    pass
				
		
		
			

