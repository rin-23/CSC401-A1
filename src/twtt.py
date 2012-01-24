import sys
from NLPlib import *
import re

#!!!!!!!!!Also consider tags as <a/>


if __name__ == "__main__":
    input_fpntr = open(sys.argv[1], "r")
    output_fpntr = open(sys.argv[2], "w")
    clitics = ["'m", "'re", "'s", "'ll", "'ve", "n't"]
    
    tagger = NLPlib()
    for line in input_fpntr:
        #output_fpntr.write('|\n')
        #output_fpntr.write("ORIGINAL: " + line)
        
        line = re.sub(r'&quot|&amp', '', line) #get rid of quot and amp
        line = re.sub(r'\. *?\. *?\.', ' &ellipsis ', line) # substitute ... with &elipsis to avoid multiple periods
        line = re.sub(r'@?<(.*) .*?>.*?</\1>', '', line) #remove html tags
        line = re.sub(r'(?:http://|ftp://|www\.)\S+\.\S+', '', line) #remove urls

        newlinearray = re.findall('([^.]*?[.!?\n]+)', line) #separate sentences in the tweet

        tokens = [re.split(r" +", line.strip()) for line in newlinearray] # separate every word using space as separator

        #extract words, punctiation and clitics
        nopunctiation = []
        for sentence in tokens:
            newsentence = []
            for word in sentence:
                newtokens = re.compile("('(?:m|re|s|ll|ve|t)|n't|&ellipsis|[^\w\s])", re.IGNORECASE).split(word)
                noempty = [re.sub(r'&ellipsis', '...', newtoken.strip()) for newtoken in newtokens if newtoken.strip() != '']
                newsentence = newsentence + noempty
            if (newsentence != []): nopunctiation.append(newsentence)

        sent = nopunctiation
        tags = [tagger.tag(sent) for sent in nopunctiation ]

        zipper = lambda x, y, z: [x[i]+y[i]+z[i] for i in range(0, len(x))]
        zipped = [zipper(nopunctiation[i], ['/']*len(tags[i]), tags[i]) for i in range(0, len(tags))]

        for sentence in zipped:
            for i in range (0, len(sentence)):
                output_fpntr.write(sentence[i])
                if i != len(sentence) - 1: output_fpntr.write(' ')
            output_fpntr.write('\n')
                
        output_fpntr.write('|\n')

    #close file pointers
    input_fpntr.close()
    output_fpntr.close()
    print("Done")
