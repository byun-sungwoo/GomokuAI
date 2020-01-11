# Gomoku Project [GomokuBoard]
# B351 - Sreekar Antharam, Daniel Byun, Andrew Chong

from sklearn.neural_network import MLPRegressor
import numpy as np
import copy
import pickle

class GomokuNeuralNet(object):
	def __init__(self):
		self.testingFile = ""
		return
	##################################
	##	Main Board Generator]	##
	##################################

	# Takes a 2d array and a width and height for a larger array.
	# Takes the 2d array and places the pattern in every possible
	# position in the larger array.
	# generateAllBoards returns all the possible boards in the
	# form of an array of 2d arrays.
	"""Blank spaces are represented as 0's"""
	def generateAllBoards(array, w, h):
		masterBoard = []
		listOfPatterns = GomokuNeuralNet.combinations(array)
		for currentPattern in listOfPatterns:
			currentListOfBoards = GomokuNeuralNet.generateBoards(currentPattern, w, h)
			for currentBoard in currentListOfBoards:
				if currentBoard not in masterBoard:
					masterBoard.append(currentBoard)
		return masterBoard

	# [Helper function for generateAllBoards(array, w, h)]
	# Takes a 2d array and a width and height for a larger array
	# The functions translates the pattern throughout the larger array in
	# every possible position without losing parts of the pattern and returns
	# an array of 2d arrays showing every possible translation
	"""Blank spaces are represented as 0's"""
	def generateBoards(pattern, w, h):
		masterList = []
		for a in range(w - len(pattern) + 1):
			for b in range(h - len(pattern[0]) + 1):
				tempboard = np.zeros((w,h)).astype(int).tolist()
				for c in range(len(pattern)):
					for d in range(len(pattern[0])):
						tempboard[a + c][b + d] = pattern[c][d]
				masterList.append(tempboard)
		return masterList

	# [Helper function for generateAllBoards(array, w, h)]
	# Takes a 2d array and returns a list of 2d arrays which
	# is the original array rotated and reflected
	def combinations(array):
		bigArray = []
		reflection = GomokuNeuralNet.mirror(array)
		for a in range(4):
			bigArray.append(array)
			bigArray.append(reflection)
			array = GomokuNeuralNet.rotateNinety(array)
			reflection = GomokuNeuralNet.rotateNinety(reflection)
		return bigArray

	# [Helper function for combinations(array)]
	# Takes a 2d array and returns the array reflected across a y axis
	def mirror(array):
		mirrored = np.zeros((len(array),len(array[0]))).tolist()
		for a in range(len(array)):
			for b in range(len(array[0])):
				mirrored[a][len(array[0])-b-1] = int(array[a][b])
		return mirrored

	# [Helper function for combinations(array)]
	# Takes a 2d array and returns the array rotated 90 degrees
	def rotateNinety(array):
		rotate = np.zeros((len(array[0]),len(array))).tolist()
		for a in range(len(array[0])):  # y pos
			for b in range(len(array)): # x pos
				rotate[a][b] = array[len(array)-b-1][a]
		return rotate

	# Takes a 2d array and a value you want to replace as "a"
	# and the value you want to replace it with as "b"
	# The function returns a new array with all "a" values as "b"
	def replace(array, a, b):
		for i in range(len(array)):
			if array[i] == a:
				array[i] = b
		
		return array

	def noDuplicates(array):
		while(len(array) > 1):
			arrayCopy = array.copy()
			arrayCopy.remove(array[0])
			for currentVal in arrayCopy:
				if array[0] == currentVal:
					return False
			array.remove(array[0])
		
		return True

"""
if __name__ == '__main__':
	for a in generateAllBoards([	[1,0,0,0,0],
					[0,1,0,0,0],
					[0,0,1,0,0],
					[0,0,0,1,0],
					[0,0,0,0,1]],19,19):
	for a in generateAllBoards([[1,1,1,1,1]],19,19):
		print("Start")
		for b in a:
			print(b)

##########################################
##	[Neural Network Training]	##
##########################################

patternDict={}
patternDict[1]=[[0,0,0,0,0],
		[0,1,0,1,0],
		[0,0,1,0,0],
		[0,1,0,1,0],
		[0,0,0,0,0]]
patternDict[2]=[[0,0,0,0,0],
		[0,0,1,0,0],
		[0,1,1,1,0],
		[0,0,1,0,0],
		[0,0,0,0,0]]
patternDict[3]=[[0,0,0,0,0],
		[0,0,1,0,0],
		[0,0,1,0,0],
		[0,1,1,1,0],
		[0,0,0,0,0]]
patternDict[4]=[[0,0,0,0,0],
		[0,0,1,0,0],
		[0,0,0,0,0],
		[0,0,1,0,0],
		[0,1,1,1,0],
		[0,0,0,0,0]]
patternDict[5]=[[0,0,0,0,0],
		[0,0,1,0,0],
		[0,0,1,0,0],
		[0,0,0,0,0],
		[0,1,1,1,0],
		[0,0,0,0,0]]
patternDict[6]=[[0,0,0,0,0],
		[0,0,1,0,0],
		[0,0,0,0,0],
		[0,1,1,1,0],
		[0,0,1,0,0],
		[0,0,0,0,0]]
patternDict[7]=[[0,0,0,0,0],
		[0,1,1,1,0],
		[0,1,0,0,0],
		[0,1,0,0,0],
		[0,0,0,0,0]]
patternDict[8]=[[0,0,0,0,0,0],
		[0,1,0,1,1,0],
		[0,1,0,0,0,0],
		[0,1,0,0,0,0],
		[0,0,0,0,0,0]]
patternDict[9]=[[0,0,0,0,0,0],
		[0,1,1,0,1,0],
		[0,1,0,0,0,0],
		[0,1,0,0,0,0],
		[0,0,0,0,0,0]]
patternDict[10]=[[0,0,0,0,0,0],
		 [0,1,1,0,1,0],
		 [0,1,0,0,0,0],
		 [0,0,0,0,0,0],
		 [0,1,0,0,0,0],
		 [0,0,0,0,0,0]]
patternDict[11]=[[0,0,0,0,0,0],
		 [0,1,0,1,1,0],
		 [0,0,0,0,0,0],
		 [0,1,0,0,0,0],
		 [0,1,0,0,0,0],
		 [0,0,0,0,0,0]]
patternDict[12]=[[0,0,0,0,0,0],
		 [0,1,0,1,1,0],
		 [0,1,0,0,0,0],
		 [0,0,0,0,0,0],
		 [0,1,0,0,0,0],
		 [0,0,0,0,0,0]]
fivePatternOne=[[1,1,1,1,1]]
fivePatternTwo=[[1,0,0,0,0],
		[0,1,0,0,0],
		[0,0,1,0,0],
		[0,0,0,1,0],
		[0,0,0,0,1]]

allPatternsOne=[]	Holds patterns for player 1
patternOneBoards=[]	Holds board data for player 1
patternOneLabels=[]	Holds label data cooresponding to patternOneBoards members

allPatternsTwo=[]	Holds patterns for player 2
patternTwoBoards=[]	Holds board data for player 2
patternTwoLabels=[]	Holds label data cooresponding to patternTwoBoards members

for i in range(len(patternDict)):
	allPatternsOne.append(patternDict[i+1])
	
for i in range(len(patternDict)):
	allPatternsTwo.append(replace(patternDict[i+1],1,2))

##########################
##	Player 1	##
##########################


for a in GomokuNeuralNet.generateAllBoards(fivePatternOne,19,19):
	print("Start")
	print(a)
	patternOneBoards.append(np.asarray(a).flatten())
patternOneLabels.extend(np.full(len(patternOneBoards),1))
oldSize = len(patternOneBoards)

for a in GomokuNeuralNet.generateAllBoards(fivePatternTwo,19,19):
	print("Start")
	print(a)
	patternOneBoards.append(np.asarray(a).flatten())
patternOneLabels.extend(np.full(len(patternOneBoards)-oldSize,1))

patternOneBoards.append(np.zeros((19,19),int).flatten())
patternOneLabels.append(0)


# Adding boards and lables for every pattern in allPatternsOne for player 1
for currentPattern in allPatternsOne:
# quicker way
##	patternOneBoards.extend(generateAllBoards(currentPattern,19,19))
	for a in generateAllBoards(currentPattern,19,19):
		print("Start")
		print(a)
		patternOneBoards.append(np.asarray(a).flatten())
patternOneLabels.extend(np.full(len(patternOneBoards),1000000000000000000))
oldSize = len(patternOneBoards)

# Adding boards and labels for fivePatternOne for player 1
for a in generateAllBoards(fivePatternOne,19,19):
	print("Start")
	print(a)
	patternOneBoards.append(np.asarray(a).flatten())
patternOneLabels.extend(np.full(len(patternOneBoards)-oldSize,9000000000000000000))
oldSize = len(patternOneBoards)

# Adding boards and labels for fivePatternTwo for player 1
for a in generateAllBoards(fivePatternTwo,19,19):
	print("Start")
	print(a)
	patternOneBoards.append(np.asarray(a).flatten())
patternOneLabels.extend(np.full(len(patternOneBoards)-oldSize,9000000000000000000))
oldSize = len(patternOneBoards)

#----------------------------------------------------
##########################
##	Player 2	##
##########################

for a in GomokuNeuralNet.generateAllBoards(GomokuNeuralNet.replace(fivePatternOne,1,2),19,19):
	print("Start")
	print(a)
	patternTwoBoards.append(np.asarray(a).flatten())
patternTwoLabels.extend(np.full(len(patternTwoBoards),-1))
oldSize = len(patternTwoBoards)

for a in GomokuNeuralNet.generateAllBoards(GomokuNeuralNet.replace(fivePatternTwo,1,2),19,19):
	print("Start")
	print(a)
	patternTwoBoards.append(np.asarray(a).flatten())
patternTwoLabels.extend(np.full(len(patternTwoBoards)-oldSize,-1))

patternTwoBoards.append(np.zeros((19,19),int).flatten())
patternTwoLabels.append(0)

# Adding boards and lables for every pattern in allPatternsTwo for player 2
for currentPattern in allPatternsTwo:
# quicker way
##	patternTwoBoards.extend(generateAllBoards(currentPattern,19,19))
	for a in generateAllBoards(currentPattern,19,19):
		print("Start")
		print(a)
		patternTwoBoards.append(np.asarray(a).flatten())
patternTwoLabels.extend(np.full(len(patternTwoBoards),-1000000000000000000))
oldSize = len(patternTwoBoards)

# Adding boards and labels for fivePatternOne for player 2
for a in generateAllBoards(replace(fivePatternOne,1,2),19,19):
	print("Start")
	print(a)
	patternTwoBoards.append(np.asarray(a).flatten())
patternTwoLabels.extend(np.full(len(patternTwoBoards)-oldSize,-9000000000000000000))
oldSize = len(patternTwoBoards)

# Adding boards and labels for fivePatternTwo for player 2
for a in generateAllBoards(replace(fivePatternTwo,1,2),19,19):
	print("Start")
	print(a)
	patternTwoBoards.append(np.asarray(a).flatten())
patternTwoLabels.extend(np.full(len(patternTwoBoards)-oldSize,-9000000000000000000))

allBoards = []
allLabels = []

allBoards.extend(patternOneBoards)
allLabels.extend(patternOneLabels)
allBoards.extend(patternTwoBoards)
allLabels.extend(patternTwoLabels)

testingFile1 = allBoards
pickle_out1 = open("gomoku_board_data_fivepattern.pickle","wb")
pickle.dump(testingFile1,pickle_out1)
pickle_out1.close()

testingFile2 = allLabels
pickle_out2 = open("gomoku_label_data_fivepattern.pickle","wb")
pickle.dump(testingFile2,pickle_out2)
pickle_out2.close()
===================================================

pickle_in = open("gomoku_board_data.pickle","rb")
board_data = pickle.load(pickle_in)
pickle_in_update = open("gomoku_board_data_update.pickle","rb")
board_data_update = pickle.load(pickle_in_update)

board_data.append(np.zeros((19,19),int).flatten())
pickle_out = open("gomoku_board_data_update.pickle","wb")
pickle.dump(board_data,pickle_out)
pickle_out.close()

pickle_in2 = open("gomoku_label_data.pickle","rb")
label_data = pickle.load(pickle_in2)
pickle_in2_update = open("gomoku_label_data_update.pickle","rb")
label_data_update = pickle.load(pickle_in2_update)

label_data.append(0)
pickle_out2 = open("gomoku_label_data_update.pickle","wb")
pickle.dump(label_data,pickle_out2)
pickle_out2.close()

pickle_in3 = open("gomoku_regressor.pickle","rb")
load_regressor = pickle.load(pickle_in3)

regressor = MLPRegressor()

-0.06420534 when board is 0
-0.06186364 when 1 wins alone
-0.05935972 when 2 wins alone
-0.06388112 when one 1 piece in middle
-0.06299755 when one 2 piece in middle
-0.06316387 when 1 wins in short game
-0.06337829 when 2 wins in short game

There is no pattern?


print(final_training.shape)
print(len(one_training_labels))
print(final_training)		# numpy array
print(total_training_labels)	# normal array

regressor.fit(board_data_update,label_data_update)

testingFile3 = regressor
pickle_out3 = open("gomoku_regressor.pickle","wb")
pickle.dump(testingFile3,pickle_out3)
pickle_out3.close()

print(regressor.predict(final_training[:]))
"""
