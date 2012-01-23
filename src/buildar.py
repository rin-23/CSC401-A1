import sys
import re

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
           print classname + '\n'
           tweetfiles = classNameMatchObject.group('tweetfiles')
           tweetarray = tweetfiles.split('+')
           for tweetfile in tweetarray:
               print tweetfile + '\n'
        else:
            print c
      


