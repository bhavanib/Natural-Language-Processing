from qgen import *
#from backend import *

print ">Hi ! How may I help you?"
while(True):
	example1=raw_input(">")
	if (example1=="Bye!"):
		break
	#print "Printing result from NER.........."
	print ">Great!"
	call_to_ner(example1)
	print ">Let me check what we have in store for you..."
	call_to_rer()
#	print "Calling Query Generation.........."
#	print "Getting Query Output........"
	call_backend()



