import math
import os
import sys


class wordProb:
    def __init__(self, word, spamCount, hamCount, probSpam, probHam, emmisionsHam, emmisionsSpam):
        self.word = word
        self.spamCount = spamCount
        self.hamCount = int(hamCount) - int(spamCount)
        self.wordGivenSpam = probSpam
        self.wordGivenHam = probHam
        self.emmisionsHam = emmisionsHam
        self.emmisionsSpam = emmisionsSpam


class processTraining:
    def __init__(self):
        self.words = []
        emmisionsHamMap = dict()
        emmisionsSpamMap = dict()

    def readTraining(self):
        lines = []
        with open('out.txt') as f:
            lines = f.readlines()
            lines = [x.strip() for x in lines]
        f.close()
        for line in lines:
            components = line.split(',')
            word = wordProb(components[0], components[1], components[2], components[3], components[4])
            self.words.append(word)


class classifier:
    def __init__(self, training):
        self.words = training.words
        self.spamOverHam = -0.38881141348
        self.numSpamPredicted = 0
        self.numHamPredicted = 0
        self.numSpamCorrect = 0
        self.numHamCorrect = 0

    def classifyFolder(self):
        counter = 0
        for file in os.listdir('emails'):
            print(counter)
            counter+= 1
            wordArray = self.textToWords(file)
            hamOrSpam = self.classifiy(wordArray)
            if hamOrSpam == 'ham':
                self.numHamPredicted += 1
                if (file.endswith(".ham.txt")):
                    self.numHamCorrect+= 1
            else:
                self.numSpamPredicted += 1
                if (file.endswith(".spam.txt")):
                    self.numSpamCorrect+= 1

    def lookUp(self, word):
        for i in range(0, len(self.words)):
            if self.words[i].word.lower() == word.lower():
                return i
        return -1

    def textToWords(self,path):
        words = []
        with open(path, 'r') as f:
            for line in f:
                for word in line.split():
                    words.append(word)
        return words

    def classifiy(self, wordsArray):
        value = self.spamOverHam
        start = 0
        for word in wordsArray:
            index = self.lookUp(word)
            if index >= 0:
                if (float(self.words[index].wordGivenHam) == 1.0):
                    start-= 1.0
                elif(float(self.words[index].wordGivenSpam) == 1.0):
                    start+= 2.0

                else:
                    start += math.log10(float(self.words[index].wordGivenSpam) /float(self.words[index].wordGivenHam))
        value+=start

        if value > 0:
            return 'spam'
        else:
            return 'ham'


def main():
    p = processTraining()
    p.readTraining()
    c = classifier(p)
    c.classifyFolder()

    print ('num span correct: ' + str(c.numSpamCorrect) + ' num ham correct ' + str(c.numHamCorrect))
    print ('num spam predicted: ' + str(c.numSpamPredicted) + ' num ham predicted: ' + str(c.numHamPredicted))
if __name__ == "__main__": main()
