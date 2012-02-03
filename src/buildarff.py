import sys
import re
import os.path


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

def countAppearance(list, search_items):
    count = 0
    for item in search_items: count += list.count(item)
    return count

def count_upper_case(words):
     #count words in upper case
    for i in range(len(words)):
        if len(words) > 1:
            if sentence[i].isupper():
                feature_counts["Upper-case-words"] += 1

def count_future_tense(words):
    #count Future Sentece
    feature_counts["Future-tense-verbs"] += countAppearance(words, resources["Future-tense-verbs"])
    for i in range(len(words)):
        if words[i] == "going":
            if i+2 < len(words):
                if words[i+1] == "to" and tags[i+2] == "vb":
                    feature_counts["Future-tense-verbs"] += 1

def avrg_sentence_len(sentence):
    #count total length of sentences
    feature_counts["Total-sentence-length"] += len(sentence)

    #count number of sentences
    feature_counts["Number-of-sentences"] += 1


def avrg_token_len(words, tags):
    #count total length of tokens
    for i in range(len(words)):
        #TO DO: find out how to type allt ypes of pucntioans
        if re.match(r"[#$.,:()\'\"]", tags[i]) == None:
            feature_counts["Total-token-length"] += len(words[i])
            feature_counts["Number-of-tokens"] += 1


def create_arff(output_file, atribute_list):

    arff_file = open(output_file, 'w')
    arff_file.write("@relation Twitter\n\n")

    for atr in resource_filenames:
        arff_file.write("@attribute " + atr + " numeric\n")
    
    arff_file.write("@attribute " + "Upper-case-words\n")
    arff_file.write("@attribute " + "Average-sentence-length\n")
    arff_file.write("@attribute " + "Average-token-length\n")
    arff_file.write("@attribute " + "Number-of-sentences\n")
    arff_file.write("@attribute " + "Classname\n")

    arff_file.write("\n@data\n")

    for cls in atribute_list:
        for atr in resource_filenames:
            arff_file.write(str(cls[atr]) + ",")

        arff_file.write(str(cls["Upper-case-words"]) + ",")
        arff_file.write(str(cls["Average-sentence-length"]) + ",")
        arff_file.write(str(cls["Average-token-length"]) + ",")
        arff_file.write(str(cls["Number-of-sentences"]) + ",")
        arff_file.write(cls["Classname"] + "\n")

    arff_file.close()

if __name__ == "__main__":
    #TODO ADD SUPPORT FOR -500 !!!!!!!!!!!!!

    result = []      
    processResources() #get all resources

    numberOfTweets = -1
    classes = []
    classname = ""
    if (sys.argv[1].startswith('-')):  
        numberOfTweets = int(sys.argv[1][1:])
        classes = sys.argv[2:-1]
    else:
        classes = sys.argv[1:-1]

    output_file = sys.argv[-1]

    #print str(numberOfTweets)
    
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
      
        for twt in twt_array:

            for key in resource_filenames: feature_counts[key] = 0
            feature_counts["Upper-case-words"] = 0
            feature_counts["Total-sentence-length"] = 0
            feature_counts["Number-of-sentences"] = 0
            feature_counts["Total-token-length"] = 0
            feature_counts["Number-of-tokens"] = 0
            feature_counts["Average-sentence-length"] = 0
            feature_counts["Average-token-length"] = 0

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

                
                count_future_tense(words)

                count_upper_case(words)

                avrg_sentence_len(sentence)

                avrg_token_len(words, tags)

                if feature_counts["Number-of-sentences"] != 0:
                    feature_counts["Average-sentence-length"] = float(feature_counts["Total-sentence-length"]) / float(feature_counts["Number-of-sentences"])
                else:
                    feature_counts["Average-sentence-length"] = 0

                if feature_counts["Number-of-tokens"] != 0:
                    feature_counts["Average-token-length"] = float(feature_counts["Total-token-length"]) / float(feature_counts["Number-of-tokens"])
                else:
                    feature_counts["Average-token-length"] = 0

            feature_counts["Classname"] = classname

            result.append(feature_counts.copy())
            #print feature_counts
            feature_counts.clear()

  #  print result
    create_arff(output_file, result)

                




