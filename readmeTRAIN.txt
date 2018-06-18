The program train.py used to generate the dictinary of the training data. 
It requires all the training files(spam and ham) to be in a folder that is in the 
current directory as the .py script

To run:
			py train.py <name of folder containing the training dataset>
				it outputs the name of all files it went through. And also creates
				a new out.txt file that contains all the words,thier counts and probabilities
				seperated with commas
				
				The format of output:
					word, #(word occurred in spam), #(word occurred in total), P(spam|word), P(ham|word)