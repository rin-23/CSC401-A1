import sys
import re
import os.path
from NLPlib import *

tagger = NLPlib()
resources = {} #contains resources to perform counts
resource_filenames = ["First-person", "Second-person", "Third-person", "Coordinating-Conjuction", 
                      "Past-tense-verbs", "Future-tense-verbs", "Commas", "Colons-semi-colons",
                      "Dashes", "Parenthesis", "Ellipses", "Common-nouns", "Proper-nouns", "Adverbs",
                      "wh-words", "Slang"]

def processTweetFile(twt_fpointer):
    twt_text = twt_fpointer.read()
    tweets = twt_text.split('|\n') #split into tweet
    tweets.pop() #remove last element since its an empty string

    twt_array = []
    for twt in tweets:
        sentences = twt.split('\n') #split into sentences
        sentences.pop() #remove last element since its an empty string
        tokens = map(lambda x: x.split(' '), sentences) #split into tokens
        twt_array.append(tokens) 

    return twt_array

def processResources():
   
    #Initialize resource to count First person pronouns
    for resource in resource_filenames:
        words = open("./Wordlists/"+resource).read().split('\n')
        words.pop()
        resources[resource] = map(lambda x : x.lower(), words)

    print resources



def countFirstPersonPronouns(twt_array):
    processResources()

#    count = 0
#    for twt in twt_array:
#        for sentence in twt:
#            for fp_token in fp_words_tagged:
#                count += sentence.count(fp_token)







if __name__ == "__main__":
    numberOfTweets = -1
    classes = []
    if (sys.argv[1].startswith('-')): 
        numberOfTweets = int(sys.argv[1][1:])
        classes = sys.argv[2:]
    else:
        classes = sys.argv[1:]

    print str(numberOfTweets)
    for c in classes:
        classNameMatchObject = re.match(r"(?P<classname>.*?):(?P<tweetfiles>.*)", c)
        if classNameMatchObject != None:
            classname = classNameMatchObject.group('classname')
            tweetfiles = classNameMatchObject.group('tweetfiles').split('+')
            twt_array = []
            for tweetfile in tweetfiles:
                twt_array = twt_array + processTweetFile(open(tweetfile, 'r'))

            #print classname
            #print twt_array

            countFirstPersonPronouns(twt_array)



        else:
            base_c = os.path.basename(c)
            classname = base_c.split('.twt')[0]
            twt_array = processTweetFile(open(c, 'r'))
            countFirstPersonPronouns(twt_array)
            #print classname
            #print twt_array
      


