import re


# returns True if, and only if, string s is a valid variable name
def is_atom(s):
	if not isinstance(s, str):
		return False
	if s == "":
		return False
	return is_letter(s[0]) and all(is_letter(c) or c.isdigit() for c in s[1:])

def is_letter(s):
	return len(s) == 1 and s.lower() in "_abcdefghijklmnopqrstuvwxyz"

# Algorithm infer_all(KB)
#   Input : KB, containing rules and atoms
#   Output: set of all atoms that are logical consequences
#           of KB

#   set C to {}   // C contains the inferred atoms

#   loop until no more rules from KB can be selected:
#      select a rule "h <-- a_1 & a_2 & ... & a_n" from KB
#             where all a_i are in C or KB (for 1 <= i <= n)
#                   and h is not in C or KB
#      add atom h to C

#   return C

knowledgeBase = {}


# parse the line to grab the atoms

text = input("kb> ")

implyE = False
ampersandE = False

# # gets the first index
# print(text[:4])
# # gets the textfile or tells of things
# print(text[5:])

if(text[:4] == "load"):

	file = open(str(text[5:]),'r')
	lines = file.readlines()
	count = 0
	# gets each line
	for line in lines:
		# finding imply symbol exists
		findImply = -1
		findImply = line.find("<--")
		#print(findImply)
		if(findImply == -1):
			# if <-- is not found in the line
			print("Error: " + str(text[5:]) + " is not a valid knowledge base")
			#count = 0
			implyE = True
			break

		# grabbing the head 
		headVar = findImply-1
		# print(line[:headVar])
		# print(is_atom(line[:headVar]))
		if(not is_atom(line[:headVar])):
			# if the head is not an atom
			print("Error: " + str(text[5:]) + " is not a valid knowledge base")
			break

		#print(line[:headVar])
		knowledgeBase[str(line[:headVar])] = {}

		#print(knowledgeBase)

		# finding ampersand
		oldAmpPos = findImply + 4
		newAmpPos = -1
		for m in re.finditer('&', line):
			# if the head has more than 2 variables
			if(m.start() < findImply):
				print("Error: " + str(text[5:]) + " is not a valid knowledge base")
				ampersandE = True
				break
			#print("Found " + str(m.start()))
			#print(line[m.start()])
			newAmpPos = m.start()
			print(newAmpPos)
			print(line[oldAmpPos:newAmpPos])
			
			

		print("\t" + line,end="")
		count += 1
	if(ampersandE or implyE):
		count = 0
	print()
	print("\t" +str(count) + " new rule(s) added")

elif(text[:4] == "tell"):
	print("telling")
	print(text[5:])
else:
	print("Error: unknown command " + "\""+str(text)+"\"")
