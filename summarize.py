import json

jsonList ='test_sets_to_summarize.json'

hakaruRootDir = "C:/Users/Nevin/Documents/dev/hakaru/4ZP6/hakaru/" 	# must be absolute path
roundTripFile = "RoundTrip.hs"			# hakaruRootDir + "haskell/Tests/RoundTrip.hs"
logFile = "hakaru-0.6.0-test.log" 		# hakaruRootDir + ".stack-work/logs/hakaru-0.6.0-test.log"

json_data=open(jsonList)
data = json.load(json_data)
json_data.close()

listOfSets = data['testSets']

tests = {}
in_file = open(roundTripFile, "rt")

for testSet in listOfSets:
	testList = []
	testArray = testSet + " = test ["
	tempString = ""
	inScope = False
	failure = False
	tests[testSet] = {}

	for line in in_file:

		if ((inScope == True) and ("]" in line)):
			inScope = False

		if (inScope == True):

			testList.append(line)
			
			lineArray = line.split(" ")
			fileIndex = 0
			for i in range(len(lineArray)) :
				if lineArray[i] == "testConcreteFiles":
					fileIndex = i + 1
					break

			file1 = hakaruRootDir + line.split(" ")[fileIndex].replace("\"","")
			file2 = hakaruRootDir + line.split(" ")[fileIndex + 1].replace("\"","").replace(",","").replace('\n', '')

			with open(file1, 'r') as fin:
				file1Code=fin.read()

			with open(file2, 'r') as fin:
				file2Code = fin.read()

			file1Name = "hakaru/" + line.split(" ")[fileIndex].replace("\"","").replace("\'","")
			file2Name = "hakaru/" + line.split(" ")[fileIndex + 1].replace("\"","").replace("\'","").replace(",","").replace('\n', '')

			testName = file1Name.split(".")[0]
			
			tests[testSet][testName] = {'files' : {
				'file1': {'name': file1Name, 'code': file1Code},
				'file2': {'name': file2Name, 'code': file2Code}}}

			in_file2 = open(logFile, "rt")
			for line2 in in_file2:

				if ((failure == True) and ("Cases:" in line2) and ("Tried:" in line2) and  ("Errors:" in line2)):
					failure = False
					tests[testSet][testName]['testResult'] = "Failed"
					tests[testSet][testName]['logs'] = tempString	
					tempString = ""
							
				if ((failure == True) and ("Cases:" not in line2) and ("Tried:" not in line2) and  ("Errors:" not in line2)):
					tempString += line2

				if (("### Failure" in line2) and (testName + ":0" in line2)):
					failure = True
					
			in_file2.close() 
		if (testArray in line):
			inScope = True		

in_file.close() 

# print json.dumps(tests, ensure_ascii=False)

with open('summary.json', 'w') as outfile:
    json.dump(tests, outfile)

####################################################################################
# 									
# 								EXAMPLE OF JSON OUTPUT
#
# {"testStdChiSqRelations": {
# 	"t_beta_to_chiSq": {
# 		"files": {
# 			"file1": {
# 						"name": "t_beta_to_chiSq.0.hk",
#						"code": "..."
# 					 }, 
# 			"file2": {
# 						"name": "t_beta_to_chiSq.expected.hk\n",
#						"code": ...
# 					 }
# 			}
# 		"testResult": "Passed/Failed"
# 		"logs": "if failed, display logs here"
# 		}
# 	}
# }
#####################################################################################

