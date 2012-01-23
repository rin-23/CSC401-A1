import sys
import re

def processTweetFile(twt_fpointer):
    twt_text = twt_fpointer.read()
#    twt_array = []
#    for line in twt_text:
#        twt = []
#        while line != '|\n': twt.append(line.split(' '))

    tweets = twt_text.split('|\n') #split into tweet
    tweets.pop() #remove last element since its an empty string

    twt_array = []
    for twt in tweets:
        sentences = twt.split('\n') #split into sentences
        sentences.pop() #remobe last element since its an empty string
        tokens = map(lambda x: x.split(' '), sentences) #split into tokens
        twt_array.append(tokens)
    return twt_array


#def countFirstPersonPronouns(twt_fpointer):

if __name__ == "__main__":
    numberOfTweets = -1
    classes = []
    if (sys.argv[1].startswith('-')): 
        numberOfTweets = int(sys.argv[1][1:])
        classes = sys.argv[2:]
    else:
        classes = sys.argv[1:]

    print str(numberOfTweets) + '\n'
    for c in classes:
        classNameMatchObject = re.match(r"(?P<classname>.*?):(?P<tweetfiles>.*)", c)
        if classNameMatchObject != None:
            classname = classNameMatchObject.group('classname')
            #print classname + '\n'
            tweetfiles = classNameMatchObject.group('tweetfiles').split('+')
            for tweetfile in tweetfiles:
                #print tweetfile + '\n'
                twt_array = processTweetFile(open(tweetfile, 'r'))
                print twt_array
        else:
            twt_array = processTweetFile(open(c, 'r'))
            print twt_array
      


