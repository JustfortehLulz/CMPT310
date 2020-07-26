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
file = ''
tellList = []
inferList = []


# parse the line to grab the atoms
while True:

	text = input("kb> ")

	Error = False

	# # gets the first index
	# print(text[:4])
	# # gets the textfile or tells of things
	# print(text[5:])

	if(text[:4] == "load"):
		knowledgeBase.clear()
		fileName = str(text[5:])
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
				knowledgeBase.clear()
				Error = True
				count = 0
				break

			# grabbing the head 
			headVar = findImply-1
			# print(line[:headVar])
			# print(is_atom(line[:headVar]))
			if(not is_atom(line[:headVar])):
				# if the head is not an atom
				print("Error: " + str(text[5:]) + " is not a valid knowledge base")
				knowledgeBase.clear()
				Error = True
				count = 0
				break

			#print(line[:headVar])
			head = str(line[:headVar])
			knowledgeBase[head] = {}

			#print(knowledgeBase)

			# finding ampersand
			oldAmpPos = findImply + 4
			newAmpPos = -1
			for m in re.finditer('&', line):
				# if the head has more than 2 variables
				if(m.start() < findImply):
					print("Error: " + str(text[5:]) + " is not a valid knowledge base")
					knowledgeBase.clear()
					Error = True
					count = 0
					break
				# sets the position of the next ampersand
				newAmpPos = m.start() - 1


				# if there is nothing inbetween two &
				if(not is_atom(line[oldAmpPos:newAmpPos])):
					print("Error: " + str(text[5:]) + " is not a valid knowledge base")
					knowledgeBase.clear()
					Error = True
					count = 0
					break

				# add into kb
				var = str(line[oldAmpPos:newAmpPos])
				knowledgeBase[head][var] = False
				#print(line[oldAmpPos:newAmpPos])
				# sets the previous position of the ampersand as the next one
				oldAmpPos = newAmpPos + 3

			# last part of the line
			if(oldAmpPos == findImply + 4):
				var = str(line[oldAmpPos:])
				knowledgeBase[head][var] = False
			else:
				if(is_atom(line[oldAmpPos:-1])):
					var = str(line[oldAmpPos:-1])
					knowledgeBase[head][var] = False
					#print(line[oldAmpPos:-1])

			
			print("\t" + line,end="")
			count += 1
		if(not Error):
			print()
			print("\t" +str(count) + " new rule(s) added")
			#print(knowledgeBase)

		file.close()

	elif(text[:4] == "tell"):
		attemptList = []
		if(file == ''):
			print("No knowledge base loaded")
		else:
			oldspacePos = 5
			#print(text[5:])
			for m in re.finditer(' ',text[5:]):
				newSpacePos = m.start() + 5

				atom = str(text[oldspacePos:newSpacePos])
				#print(text[oldspacePos:newSpacePos])

				if(not is_atom(atom)):
					print("Error: " + "\"" + str(atom) + "\" is not a valid atom")
					for attempt in attemptList:
						tellList.remove(attempt)
					Error = True
					#print(tellList)
					break
				
				if(atom not in tellList):
					tellList.append(atom)
					attemptList.append(atom)
				else:
					print("atom " + "\"" + str(atom) + "\" already known to be true")

				#print(is_atom(text[oldspacePos:newSpacePos]))
				#print("BRUHL " + str(m.start()))
				oldspacePos = newSpacePos + 1

			if(not Error):
				if(not is_atom(text[oldspacePos:])):
					print("Error: " + "\"" + str(text[oldspacePos:]) + "\" is not a valid atom")
					for attempt in attemptList:
						tellList.remove(attempt)
					Error = True
					#print(tellList)
				else:
					#print(text[oldspacePos:])
					tellList.append(str(text[oldspacePos:]))
					for a in tellList:
						print("\""+ str(a) + "\" added to KB")
						knowledgeBase[a] = True


		attemptList = []				

	elif(text[:9] == "infer_all"):
		C = []
		for a in knowledgeBase:
			head = a
			rules = knowledgeBase[a]
			# print(head,end=" ")
			# print(rules)
			if(rules == True):
				inferList.append(head)
		for b in knowledgeBase:
			head = b
			rules = knowledgeBase[b]
			# none of the inferred rules
			### iterate through inferList
			for i in inferList:
				if(head != i and rules != True):
					# print(head)
					# print(rules)
					# print(head in inferList[0])
					# print(inferList[0] in rules)
					if(head in i):
						inferList.append(head)
					if(i in rules):
						knowledgeBase[b][i] = True
		### check if all rules are true then add to the inferList
		for key in knowledgeBase:
			#print(knowledgeBase[key])
			if(knowledgeBase[key] != True):
				for value in knowledgeBase[key]:
					if(knowledgeBase[key][value] != True):
						break
					C.append(key)
					#print(inferList)
					#print(C)
		print("Newly inferred atoms:")
		if(not C):
			print("<none>")
		else:
			for val in C:
				print(val,end=" ")
			print()
		print("Atoms already known to be true:")
		for val in inferList:
			print(val,end=" ")
		print()

		inferList.extend(C)

		for d in knowledgeBase:
			for val in C:
				if(knowledgeBase[d] != True):
					if(val in knowledgeBase[d]):
						knowledgeBase[d][val] = True

		#print(knowledgeBase)


		# 	if(a in knowledgeBase.keys()):
		# 		print(knowledgeBase[a])
		# 		for key in knowledgeBase[a]:
		# 			knowledgeBase[a][key] = True
		# 			print(key)

		# 	if(a not in knowledgeBase.keys()):
		# 		for key in knowledgeBase:
		# 			for value in knowledgeBase[key]:
		# 				if(value == a):
		# 					knowledgeBase[key][value] = True
		#print(knowledgeBase)


			### WORK ON INFER ALL go through tellList and change values in knowledgeBase to True.
			### check which keys in knowledgeBase has values of all True to determine what was inferred






		### INFER ALL
		# atomList = []
		# oldspacePos = 5
		# #print(text[5:])
		# for m in re.finditer(' ',text[5:]):
		# 	newSpacePos = m.start() + 5

		# 	atom = str(text[oldspacePos:newSpacePos])
		# 	#print(text[oldspacePos:newSpacePos])

		# 	if(not is_atom(atom)):
		# 		print("Error: " + "\"" + str(atom) + "\" is not a valid atom")
		# 		Error = True
		# 		atom = []
		# 		break
		# 	atomList.append(atom)
		# 	#print(is_atom(text[oldspacePos:newSpacePos]))
		# 	#print("BRUHL " + str(m.start()))
		# 	oldspacePos = newSpacePos + 1

		# if(not is_atom(text[oldspacePos:])):
		# 	print("Error: " + "\"" + str(text[oldspacePos:]) + "\" is not a valid atom")
		# 	atom = []
		# 	Error = True
			
		# else:
		# 	atomList.append(text[oldspacePos:])
		# 	print(atomList)
		# 	for a in atomList:
		# 		## check for the key dictionary values
		# 		## then check inside each key and check if its a value instead of a key
		# 		print(a)
		# 		print(a in knowledgeBase.keys())
		# 		#if not in here
		# 		if(a not in knowledgeBase.keys()):
		# 			for kb in knowledgeBase.values():
		# 				print(kb)
		# 				print(a in kb)
		# 				if(a in kb):
		# 					kb[a] = True


		
			

			## do later
			#print("Error tell needs at least one atom")
	else:
		print("Error: unknown command " + "\""+str(text)+"\"")
