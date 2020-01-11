# Gomoku Project [GomokuBoard]
# B351 - Sreekar Antharam, Daniel Byun, Andrew Chong

from sklearn.neural_network import MLPRegressor
import random
import pickle
import numpy as np

# Takes a 1d array containing only 0s and 1s or only 0s and 2s
# Counts how many either 1s or 2s there are and fills the board
# randomly with the opposite value for the amount of times the first value was seen -1
def addRandomVals(array):
	numDict = {}
	numDict[1]=0
	numDict[2]=0
	for a in array:
		if a == 1:
			numDict[1] += 1
		elif a == 2:
			numDict[2] += 1
	# Is the least frequent value
	leastFreq = list(numDict.keys())[list(numDict.values()).index(min(numDict.values()))]
	# Is the most frequent value
	mostFreq = list(numDict.keys())[list(numDict.values()).index(max(numDict.values()))]
	# Frequency of how often the most frequent value occurs
	frequency = numDict[list(numDict.keys())[list(numDict.values()).index(max(numDict.values()))]]
	while frequency > 1:
		rand = random.randint(0,len(array)-1)
		if array[rand] == 0:
			array[rand] = leastFreq
			frequency -= 1
	return array

def addingValues(array):
	originalvalues = []
	oneCount = 0
	twoCount = 0
	arrayCount = 0
	for i in range(len(array)):
		arrayCount += 1
		if array[i] == 1:
			oneCount += 1
		elif array[i] == 2:
			twoCount += 1
	if oneCount > 0:
		boundaries = int(arrayCount / oneCount)
		boundariesCount = 0
		for j in range(oneCount - 1):
			pos = random.randint(boundariesCount, boundariesCount + boundaries)
			while array[pos] == 1 or array[pos] == 2:
				pos = random.randint(boundariesCount, boundariesCount + boundaries)
			boundariesCount += boundaries
			array[pos] = 2
	elif twoCount > 0:
		boundaries = int(arrayCount / twoCount)
		boundariesCount = 0
		for j in range(twoCount - 1):
			pos = random.randint(boundariesCount, boundariesCount + boundaries)
			while array[pos] == 1 or array[pos] == 2:
				pos = random.randint(boundariesCount, boundariesCount + boundaries)
			boundariesCount += boundaries
			array[pos] = 1
	return array

"""
pickle_in_update = open("gomoku_board_data_fivepattern.pickle","rb")
board_data_update = pickle.load(pickle_in_update)

for a in range(len(board_data_update)):
	board_data_update[a] = np.asarray(addingValues(board_data_update[a].tolist()))
	print("--Updated--")
	print(board_data_update[a])

pickle_out1 = open("gomoku_board_data_fivepattern_andrew.pickle","wb")
pickle.dump(board_data_update,pickle_out1)
pickle_out1.close()

Load
pickle_in_update = open("gomoku_board_data_fivepattern_andrew.pickle","rb")
board_data_update = pickle.load(pickle_in_update)

pickle_in_update2 = open("gomoku_label_data_fivepattern.pickle","rb")
label_data_update = pickle.load(pickle_in_update2)

regressor = MLPRegressor()
regressor.fit(board_data_update,label_data_update)
testingFile3 = regressor
pickle_out3 = open("gomoku_regressor_fivepattern_andrew.pickle","wb")
pickle.dump(testingFile3,pickle_out3)
pickle_out3.close()
"""

pickle_in_update = open("gomoku_regressor_fivepattern_andrew.pickle","rb")
regressor = pickle.load(pickle_in_update)
