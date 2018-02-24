tests = {}
# STEP 1: 
#	Create lists of all test case names and the respective file paths to their hakaru programs
# 	Pull this info from hakaru/haskell/Tests/RoundTrip.hs
#	Only want tests from the sets listed in test_sets_to_summarize
#	Keep test sets separate
#	tests = {'testSetName': { 
#					'testName': { 
#							'files': {
#									'fileName': '<HAKARU CODE>', 
#									'fileName2': '<HAKARU CODE>'	
#							}
#							'logs':  '<LOG FILE THINGS>' OR 'PASS'
#					} 
#			 } 
#			}

# STEP 2:
#	For each test case:
#		Scan hakaru/.stack-work/logs/hakaru-0.6.0-test.log to see if it comes up as a failure
#		If it appears:
#			Mark test case as failed
#			Extract relevant info from the log and output to a file
#		Else:
#			Mark test case as passed

# STEP 3:
#	Output test results 
#	Create a summary table with test name and whether it passed or failed
#	Create an appendix which has headings for every test case.
#		For each test case we want: 
#			the filenames and code used in the test
#			the failure info from the logs or something saying the test passed