import glob, os

TRAINING_FILE_PATH = 'C:\\SBU\\CSE390\\final_project\\enron_tagged\\spam\\'
EMISSIONS_OUTPUT_FILE = 'emissions_spam.txt'
LAPLACE_OUTPUT_FILE = 'laplace-tag-unigrams_spam.txt'
NULL = 'NULL'
TAG = 'TAG'
WORD = 'WORD'
MLE_TGW = 'MLE_TGW'
MLE_WGT = 'MLE_WGT'
LAP_WGT = 'LAP_WGT'


def populate_wordTaggedT(word,tag):
    if word in wordTaggedT:
        tags_of_word = wordTaggedT[word]
        if tag in tags_of_word:
            tags_of_word[tag] += 1
        else:
            tags_of_word[tag] = 1
    else:
        wordTaggedT[word] = {tag: 1}
    return

def populate_tagOfWords(word,tag):
    if tag in tagOfWords:
        words_of_tag = tagOfWords[tag]
        if word in words_of_tag:
            words_of_tag[word] += 1
        else:
            words_of_tag[word] = 1
    else:
        tagOfWords[tag] = {word: 1}
    return

def populate_tagOfTags(prevTag,tag):
    if prevTag in tagOfTags:
        second_tags = tagOfTags[prevTag]
        if tag in second_tags:
            second_tags[tag] += 1
        else:
            second_tags[tag] = 1
    else:
        tagOfTags[prevTag] = {tag: 1}
    return

def populate_tags(tag):
    if tag in all_tags:
        all_tags[tag] += 1
    else:
        all_tags[tag] = 1
    return

def populate_words(word):
    if word in all_words:
        all_words[word] += 1
    else:
        all_words[word] = 1
    return

def get_mle_tags(first_tag,second_tag):
    firstFollowSecond = (tagOfTags[first_tag])[second_tag]
    numSecondTag = all_tags[second_tag]
    return float(firstFollowSecond)/numSecondTag

wordTaggedT = dict()
tagOfWords = dict()
tagOfTags = dict()
all_tags = dict()
all_words = dict()
emissions = dict()
num_tags = 0

for filename in os.listdir(TRAINING_FILE_PATH):
    file_path = TRAINING_FILE_PATH+filename
    tf_file = open(file_path,'r')
    tf_source = tf_file.read()
    tf_file.close()
    #parses training file and creates the proper data sets
    sentences = tf_source.split("\n")
    for sentence in sentences:
        choppedSentence = sentence.split()
        previousTag = NULL
        for pair in choppedSentence:
            if "_" in pair:
                splitPair = pair.rsplit("_",1)
                word = splitPair[0]
                tag = splitPair[1]
                populate_wordTaggedT(word,tag)
                populate_tagOfWords(word,tag)
                populate_tagOfTags(previousTag,tag)
                populate_tags(tag)
                populate_words(word)
                previousTag = tag
                num_tags+=1

for tag in tagOfWords:
    words = tagOfWords[tag]
    totalNumWordsTagged = 0
    for word in words:
        numTimesTagged = words[word]
        totalNumWordsTagged += numTimesTagged
    for word in words:
        numTimesTagged = words[word]
        MLE_P = numTimesTagged/float(totalNumWordsTagged)
        LAPLACE_P = (numTimesTagged+1)/float(totalNumWordsTagged+len(all_tags)+1)
        if tag in emissions:
            (emissions[tag])[word] = {MLE_WGT: MLE_P, LAP_WGT: LAPLACE_P}
        else:
            emissions[tag] = {word: {MLE_WGT: MLE_P, LAP_WGT: LAPLACE_P}}

for word in wordTaggedT:
    tags = wordTaggedT[word]
    totalNumTaggedWords = 0
    for tag in tags:
        numWordsTagged = tags[tag]
        totalNumTaggedWords += numWordsTagged
    for tag in tags:
        numWordsTagged = tags[tag]
        MLE_P = numWordsTagged/float(totalNumTaggedWords)
        current_probs = (emissions[tag])[word]
        current_probs[MLE_TGW] = MLE_P

emission_output = open(EMISSIONS_OUTPUT_FILE, 'w')
for tag in emissions:
    #print (emissions[tag])
    for word in emissions[tag]:
        probs_of_word = (emissions[tag])[word]
        emission_output.write("{:<7}".format(tag)+"{:<35}".format(word)+"{:<18}".format(str(probs_of_word[MLE_TGW]))+"\n")
emission_output.close()

laplace_unigram_output = open(LAPLACE_OUTPUT_FILE, 'w')
for tag in all_tags:
    LAPLACE_P = (all_tags[tag]+1)/float(num_tags+len(all_tags)+1)
    laplace_unigram_output.write("{:<7}".format(tag)+str(LAPLACE_P)+"\n")
laplace_unigram_output.close()
