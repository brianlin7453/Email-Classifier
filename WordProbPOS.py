import math
import os
import sys


class wordProb:
    def __init__(self, word, spamCount, hamCount, probSpam, probHam):
        self.word = word
        self.spamCount = spamCount
        self.hamCount = int(hamCount) - int(spamCount)
        self.wordGivenSpam = probSpam
        self.wordGivenHam = probHam
        self.hamAndProbs = dict()
        self.spamAndProbs = dict()

    def updateEmissionsHam(self, posTag, prob):
        self.hamAndProbs[posTag] = prob

    def updateEmissionsSpam(self, posTag, prob):
        self.spamAndProbs[posTag] = prob

class processTraining:
    def __init__(self):
        self.words = dict()

    def readTraining(self):
        with open('out.txt') as f:
            lines = f.readlines()
            lines = [x.strip() for x in lines]
        f.close()
        for line in lines:
            components = line.split(',')
            word = wordProb(components[0], components[1], components[2], components[3], components[4])
            self.words[components[0]]=word

    def readEmmisions(self,fileName,isHam):
        with open(fileName)as f:
            lines = f.readlines()
            lines = [x.strip() for x in lines]
        f.close()

        for line in lines:
            components = line.split()
            posTag = components[0]
            word = components[1]
            prob = float(components[2])
            if word in self.words:
                currWordProb = self.words[word]
                if isHam:
                    currWordProb.updateEmissionsHam(posTag,prob)
                else:
                    currWordProb.updateEmissionsSpam(posTag,prob)

    def lookUp(self, word):
        for i in range(0, len(self.words)):
            if self.words[i].word.lower() == word.lower():
                return i
        return -1

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
            filepath = 'emails'+"\\"+file
            wordDict = self.textToWords(filepath)
            hamOrSpam = self.classifiy(wordDict)
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
        dictOfPath = dict()
        with open(path, 'r') as f:
            for line in f:
                for pair in line.split():
                    if "_" in pair:
                        splitPair = pair.rsplit('_',1)
                        dictOfPath[splitPair[0]] = splitPair[1]
        return dictOfPath

    def classifiy(self, wordsDict):
        lamda1 = 0.95
        lamda2 = 0.05
        probSpam = 0.25105
        probHam = 0.74895

        value = self.spamOverHam
        start = 0
        for word in wordsDict:
            if word in self.words:
                wordObj = self.words[word]
                if (float(wordObj.wordGivenHam) == 1.0):
                    start-= 1.0
                elif(float(wordObj.wordGivenSpam) == 1.0):
                    start+= 2.0

                else:
                    currentTag = wordsDict[word]
                    probTGW_ham = 0
                    probTGW_spam = 0
                    if currentTag in wordObj.hamAndProbs:
                        probTGW_ham = wordObj.hamAndProbs[currentTag]
                    if currentTag in wordObj.spamAndProbs:
                        probTGW_spam = wordObj.spamAndProbs[currentTag]
                    normalizedPOSHam = probTGW_ham/probSpam
                    normalizedPOSSpam = probTGW_spam/probHam
                    start += math.log10((lamda1*float(wordObj.wordGivenSpam)+lamda2*normalizedPOSHam) / ((lamda1*float(wordObj.wordGivenHam))+lamda2*normalizedPOSSpam))
        value+=start

        if value > 0:
            return 'spam'
        else:
            return 'ham'


def main():
    p = processTraining()
    print("Reading training")
    p.readTraining()
    print("Reading ham mmissions")
    p.readEmmisions("emissions_ham.txt",True)
    print("Reading spam emissions")
    p.readEmmisions("emissions_spam.txt",False)
    c = classifier(p)
    c.classifyFolder()

    print ('num span correct: ' + str(c.numSpamCorrect) + ' num ham correct ' + str(c.numHamCorrect))
    print ('num spam predicted: ' + str(c.numSpamPredicted) + ' num ham predicted: ' + str(c.numHamPredicted))
if __name__ == "__main__": main()
