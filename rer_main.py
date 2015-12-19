import json
import yaml
import nltk
from rer_feature_functions import FeatureFunctions
from rules import Rules
from mymaxent import MyMaxEnt
json_data=open('all_data.json')
data = yaml.load(json_data)
di = {} #key is sentence and value is rel array
count = 0
corpus = [] #list of sentences
final = []

for contrib in data["root"]:
	for element in contrib["data"]:
	
		for x in element:
		
			try:			
				tag_word=element["rels"]
				di[element["sentence"]]=tag_word
				corpus.append(element["sentence"])
			except KeyError:
				continue

	count =0
	for x in di:
		val = di[x]
		for i in val:
			for j in i:
				final.append([x,j])
supported_tags = ["interest_intent","price_query","feature_query","irrelevant","comparison","disagreement","greeting","agreement","acknowledgement"]


'''def test_rer(rclasi,tcorpus):
	result = []
	match = 0
	total = len(tcorpus)
	for i in tcorpus :
		
		pred = rclasi.classify(i)
		obs = i[1]
		result.append([pred,obs])
	a=0.0;b=0.0;c=0.0;d=0.0;precision=0.0;recall=0.0;fscore=0.0	
	for tag in supported_tags:
		for i in result:
		
			for j in result:
				if ((j[0]==j[1]) and (j[1]==tag)):
					d=d+1.0
				elif ((j[0] !=j[1]) and (j[0]==tag)):
					b=b+1.0			
				elif ((j[0] !=j[1]) and (j[1]==tag)):
					c=c+1.0
				else:
					a=a+1.0
			if(d>(b+d)):
				precision=0.0
			else:		
				precision=(d*100/(b+d))
			
			if(d>(c+d)):
				recall = 0.0
			else:
				recall = (d*100/(c+d))
			if(precision == 0 and recall == 0):
				fscore = 0.0
			else:
				fscore = (2*precision*recall)/(precision + recall)
		
		print ("Tag:",tag,"  precision:",precision,"  recall:",recall,"  F-score:",fscore)
		
	
	return result
'''

def test_rer(rclasi,tcorpus):
	result = []
	match = 0
	total = len(tcorpus)
	for i in tcorpus :
		
		pred = rclasi.classify(i)
		result.append(pred)
	return result


rfeats = FeatureFunctions(di,supported_tags)
rrules = Rules(corpus,supported_tags)
#print final[-1:]
'''
for ele in final[:]:
	if(ele[1]=="agreement"):
		#if i=="agreement":
		print ele[0]
#	print di[ele[0]]


'''
#print final[-1:]	
#sample = [["This phone is good","agreement"]]
#rclasi = MyMaxEnt(final[:1200], rfeats,rrules)
#rclasi.train()
#res = test_rer(rclasi,final[-400:])


