This readme is for the POS tagging part of the Project.
All testing and training is done using the enron email dataset format.
==========================================================================================

The directory pos_tagger holds the tagging code in java for tagging any set of text files.
The tagger i'm using is from stanford, which is why I'm including the entire directory.

In src/pos_tagger.java: 
Input: change the path to the SPAM and HAM folders containing the e-mails.
Output: change the path to the output directory. Currently it's set to a path to "ernon_tagged"

==========================================================================================

The code to get the emissions probabilities of the e-mails

In train-tagger.py:
Input: change the path to the ouput folder of pos_tagger.java, it will read in all SPAM and HAM files.
Output: 
	-emissions_ham.txt	-> emissions prob for all ham emails
	-emissions_spam.txt	-> emissions prob for all spam emails
	Will output these in same directory as train-tagger.py

==========================================================================================

The modified Bayes algorithm incorporating emissions.

WordProbPOS.py
Input: Takes in the following files in the same directory:
	-emissions_ham.txt	>From train-tagger.py
	-emissions_spam.txt	>From train-tagger.py
	-out.txt		>From eriks training code (readmeTRAIN)
	Also takes in a test set with the form:
	directory: emails
		-subdirectory:spam
		-subdirectory:ham
		The subdirectories contain the spam and ham emails for testing.
Output:
The numbers needed to calculate the precision and recall in the console.