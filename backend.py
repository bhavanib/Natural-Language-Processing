from ner_client import *

'''
ner = NerClient("55555", "g100")
print (ner.get_products("Samsung")) 
print (ner.get_brand_product_bigrams_dict()), 
print (ner.get_spec(brand = "Samsung", product = "None"))
print (ner.get_spec(brand = "Samsung", product = "E1195")) 
'''


class Backend(object):
	def __init__(self,org,feature,family,price,other,os,version,phone,size,sentence) :
		self.org = org
		self.feature=feature
		self.family=family
		self.price=price
		self.other=other
		self.os=os
		self.version=version
		self.phone = phone
		self.size=size
		self.sentence = sentence
		self.limit=50
		self.ner = NerClient("55555", "g100")
		
		
		#print(self.org,self.feature,self.family,self.price,self.other,	self.os,self.version,self.phone,self.size)

	def price_query(self) :
		
		result_list=[]
		match =0
		less = ["less","under","not more","not greater","lesser","below","<"]
		great = ["more","above","not less","not lesser","not below","great","greater",">=",">"]
		localex=self.sentence.split()
		for i in range(len(localex)):
			temp = localex[i]
			if((temp[-1:] == "k" or temp[-1:] == "K") and ((temp[:-1]).isdigit())):
				self.price.append(str(int(temp[:-1])*1000))
				
		data={}
		if (len(self.org)>0 and len(self.family)==0 and len(self.price)>0):
			#print "1"
			for i in self.org:
				data[i] = self.ner.get_products(i)
				for j in self.price :
					if(j.isdigit()):
						for l in less:
							if l in self.sentence :
								for k in data[i]:
									if (int(k['dummy_price'])<int(j)):
										result_list.append(k)
						for g in great:
							if g in self.sentence :
								for k in data[i]:
									if (int(k['dummy_price'])>=int(j)):
										result_list.append(k)
						
			
		elif(len(self.family)>0 and len(self.price)>0):
			#print "2"
			flag=0;cost=0;le=0
			#result_list=[]
			if len(self.org)==1:
				data = self.ner.get_products(self.org[0])
			else:
				data = self.ner.get_products(None)	
			#print data

			for p in self.price :
				if(p.isdigit()):
					cost = int(p)
			for l in less:
				if l in self.sentence :
					le=1
			for g in great:
				if g in self.sentence :
					le=2
								
			for x in self.family:
				
				#print "in loop1",x
				for j in data:
					#print "j=",j
					if(x in j['product']):
						#print "In loop2"
						if(le==1):
							if (int(j['dummy_price'])<cost):
								result_list.append(j)
								#print(j)	
								
						elif(le==2):
							if (int(j['dummy_price'])>=cost):
								result_list.append(j)
								#print(j)	
								
					
										
		elif ((len(self.org))==0 and len(self.family)>0):
			#print "3"
			data = self.ner.get_products(None)
			for j in data:
				for x in self.family:
					if(x in j['product']) :
						result_list.append(j)

		
						
		elif (len(self.org)==0 and len(self.family)==0 and len(self.price)>0):
			#print "4"
			data = self.ner.get_products(None)
			for j in data:
				for p in self.price:
					if(p.isdigit()):
						for l in less:
							if l in self.sentence :
								if (int(j['dummy_price'])<int(p)):
										result_list.append(j)
						for g in great:
							if g in self.sentence :
								if (int(j['dummy_price'])>=int(p)):
										result_list.append(j)
		
		else :
			print "Sorry. We dont have the products of your choice right now :("		
		match = len(result_list)
	
		if(match<self.limit):
			print ">We have the following products for you!"
			for i in result_list:
				print "Brand: ",i['brand'],"\tModel: ",i['product'],"\tPrice: ",i['dummy_price']
		else:
			#print ">We have ",match," number of phones in that range"
			if(len(self.org)==0):
				print ">Please tell me which Brand would you prefer.These are the brands that we have"
				brands = ""
				for i in result_list:
					brands = brands + i['brand'] + "\t"
				brands=brands.split()
				brands = set(brands)
				brands = " ".join(brands)
				print brands
				brand =""
				while(True):
					brand = raw_input(">")
					self.org.append(brand)
					if not brand:
						break
			elif(len(self.family)==0):
				print ">Please tell me which Model would you prefer.These are the Models that we have"
				models = ""
				for i in result_list:
					models = models + i['product'] + "\t"
				models=models.split()
				models = set(models)
				models = " ".join(models)
				print models
				model=""
				while(True):
					model = raw_input(">")
					self.family.append(model)
					if not model:
						break
			#	print "Some mess da:",self.family
			elif(len(self.price)==0):
				print ">Please tell me which Model would you prefer.These are the Models that we have"
				prices1 = ""
				for i in result_list:
					prices1 = prices1 + i['dummy_price'] + "\t"
				prices1=prices1.split()
				prices1= set(prices1)
				prices1= " ".join(prices1)
				print prices1
				price1=""
				while(True):
					price1 = raw_input(">")
					self.price.append(price1)
					if not price1:
						break
			else:
				print "These are the products that we have for you!"
				i=0
				while(i<10):
					print "Brand: ",result_list[i]['brand'],"\tModel: ",result_list[i]['product'],"\tPrice: ",result_list[i]['dummy_price']
					
					i=i+1
				return
			#print "So before recursion"	 				
			self.price_query()
				
	
	def comparison_query(self):
		data={}
		if(len(self.org)>1):
			k=-1
			for i in self.org:
				
				data[i] = self.ner.get_products(i)
				if(len(self.family)>1):
					k=k+1
					print "Specs of"," ",i,"  ",self.family[k],":"
					for j in data[i]:
						if(self.family[k] in j['product']):
							print "Brand: ",j['brand'],"\tModel: ",j['product'],"\tPrice: ",j['dummy_price']
					
				
				
				else:	
					print "Details of ",i,":"
					for j in data[i]:
						print "Brand: ",j['brand'],"\tModel: ",j['product'],"\tPrice: ",j['dummy_price']

	def feature_query(self) :
		print "feature_query"

	def interest_intent(self) :
		print "interest_intent"

	
		
						
