import sys
import re
import os.path
from NLPlib import *

tagger = NLPlib()
resources = {} #contains resources to perform counts
feature_counts = {}
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
        feature_counts[resource] = 0

def countAppearance(list, search_items):
    count = 0
    for item in search_items: count += list.count(item)
    return count

if __name__ == "__main__":
    processResources() #get all resources

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
        else:
            base_c = os.path.basename(c)
            classname = base_c.split('.twt')[0]
            twt_array = processTweetFile(open(c, 'r'))
                 
        count = 0
        for twt in twt_array:
            for sentence in twt:
                lowercase_sentence = map(lambda x : x.lower(), sentence)
                words = map(lambda x: (re.match(r"(?P<word>.*)/(?P<tag>.*)", x)).group("word"), lowercase_sentence)
                tags = map(lambda x: (re.match(r"(?P<word>.*)/(?P<tag>.*)", x)).group("tag"), lowercase_sentence)

                for key in resources.keys():
                    if key == "First-person":
                        feature_counts[key] += countAppearance(words, resources[key])
                    elif key == "Second-person":
                        feature_counts[key] += countAppearance(words, resources[key])
                    elif key == "Third-person":
                        feature_counts[key] += countAppearance(words, resources[key])
                    elif key == "Coordinating-Conjuction":
                        feature_counts[key] += countAppearance(words, resources[key])
                    elif key == "Past-tense-verbs":
                        feature_counts[key] += countAppearance(tags, resources[key])
                    elif key == "Future-tense-verbs":
                        feature_counts[key] += countAppearance(words, resources[key])
                    elif key == "Commas":
                        feature_counts[key] += countAppearance(tags, resources[key])
                    elif key == "Colons-semi-colons":
                        feature_counts[key] += countAppearance(words, resources[key])
                    elif key == "Dashes":
                        feature_counts[key] += countAppearance(words, resources[key])
                    elif key == "Parenthesis":
                        feature_counts[key] += countAppearance(words, resources[key])
                    elif key == "Ellipses":
                        feature_counts[key] += countAppearance(words, resources[key])
                    elif key == "Common-nouns":
                        feature_counts[key] += countAppearance(tags, resources[key])
                    elif key == "Proper-nouns":
                        feature_counts[key] += countAppearance(tags, resources[key])
                    elif key == "Adverbs":
                        feature_counts[key] += countAppearance(tags, resources[key])
                    elif key == "wh-words":
                        feature_counts[key] += countAppearance(tags, resources[key])
                    elif key == "Slang":
                        feature_counts[key] += countAppearance(words, resources[key])

                #count goint+to+VB
                for i in range(len(words)):
                    if words[i] == "going":
                        if i+2 < len(words):
                            if words[i+1] == "to" and tags[i+2] == "vb":
                                feature_counts["Future-tense-verbs"] += 1

                #count words in upper case
                feature_counts["Upper-case-words"] = 0
                for i in range(len(words)):
                    if len(words) > 1:
                        if sentence[i].isupper():
                            feature_counts["Upper-case-words"] += 1








        print feature_counts




                




