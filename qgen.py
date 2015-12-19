from ner_client import *
from feature_functions import FeatureFunctions as nerFeat
from rer_feature_functions import FeatureFunctions as rerFeat
from memm import Memm
from MyMaxEnt import MyMaxEnt as nerMax
from mymaxent import MyMaxEnt as rerMax
from ner_main import * 
from rer_main import *
from rules import *
from backend import *
import yaml
import nltk
import json
'''
ner = NerClient("55555", "g100")
print (ner.get_products("Samsung")) 
print (ner.get_brand_product_bigrams_dict()), 
print (ner.get_spec(brand = "Samsung", product = "None"))
print (ner.get_spec(brand = "Samsung", product = "E1195")) 
'''
example =[]
result =""
example1=""
rr=""

############################################NER PART############################################
def call_to_ner(sent):
	json_file = r"all_data.json"
	pickle_file = r"all_data.p"
	history_file = r"history.p"
	model_metrics_file = r"model_metrics.p"

	ner_client = NerClient("1PI11IS022", "g18")    
	ret = ner_client.get_brand_product_bigrams_dict()

	supported_tags = ["Org", "OS", "Version", "Phone", "Other", "Price", "Family", "Size", "Feature"]    


	data = json.loads(open(json_file).read())['root']
	#print "number of contributors = ", len(data)
	(history_list, sents, expected) = build_history(data, supported_tags)
	(his1, wmap1) = build_history_1(data, supported_tags)
	myhis = (history_list, sents, expected, ) 
	pickle.dump(myhis, open(history_file, "wb"))        


	func_obj = nerFeat(wmap1, supported_tags, ret) #FeatureFunctions(supported_tags)
	#print "Number of features defined: ", len(func_obj.flist)
	clf = Memm(func_obj, pickle_file)

	func_obj.set_wmap(sents)
	#print "After build_history"

	#Made Train 0
	TRAIN = 0
	if TRAIN == 1:
	    clf.train(history_list[:], reg_lambda = 0.02) # 10000
	else:
	    clf.load_classifier()



	global example1
	example1=sent
	global example
	#example1 = raw_input("Enter sentence :")  
	example = example1.split()
	test_sents=[]
	test_sents.append(example)
	#test_sents = sents[-5:] #sents[-70:-50]
	global result 
	result=clf.tag(test_sents)
#	print "Sentence,example1 : ",example1
#	print "Words in the sentence,example : ",example
#	print "Result tag,result : ",result
	


############################################RER PART############################################

def call_to_rer():
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
	rsupported_tags = ["interest_intent","price_query","feature_query","irrelevant","comparison","disagreement","greeting","agreement","acknowledgement"]

	rfeats = rerFeat(di,rsupported_tags)
	rrules = Rules(corpus,rsupported_tags)
	test = []
	test.append(example1)
	test.append("*")
	test_case = []
	test_case.append(test)

	rclasi = rerMax(final[:], rfeats,rrules)
	rclasi.train()
	res = test_rer(rclasi,test_case)

	global rr
	for r in res:
#		print "Relation tag,rr : ",r
		rr=r
	



###########################################QUERY GEN PART#########################################################

def call_backend():
	org=[];feature=[];family=[];price=[];other=[];os=[];version=[];phone=[];size=[]

	for x in range(len(result)):
		for i in range(len(result[x])):
			temp = result[x][i]
			if("Org" == temp):
				org.append(example[i])
			if("Feature" ==temp):
				feature.append(example[i])
			if("Family" ==temp):
				family.append(example[i])
			if("Price" ==temp):
				price.append(example[i])
			if("Other" ==temp):
				other.append(example[i])
			if("OS" ==temp):
				os.append(example[i])
			if("Version"==temp):
				version.append(example[i])
			if("Phone" ==temp):
				phone.append(example[i])
			if("Size" ==temp):
				size.append(example[i])

	back = Backend(org,feature,family,price,other,os,version,phone,size,example1)
	if(rr=="price_query"):
		back.price_query()
	elif(rr=="feature_query"):
		back.feature_query()
	elif(rr=="irrelevant_query"):
		print("Sorry! Unable to process your query.Please try again")
	elif(rr=="agreement"):
		print("Yes your request is being processed")
	elif(rr=="disagreement"):
		print("Sorry sir why dont you look at this")
	elif(rr=="greeting"):
		print("Good day!")
	elif(rr=="comparison"):
		back.comparison_query()
	elif(rr=="acknowledgement"):
		print("Thank you!")
	else:
		back.interest_intent()		
