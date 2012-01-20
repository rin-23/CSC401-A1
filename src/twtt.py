import sys
from NLPlib import *
import re


if __name__ == "__main__":
    input_fname = sys.argv[1]
    output_fname = sys.argv[2]
    input_fpntr = open(input_fname, "r")
    output_fpntr = open(output_fname, "w")
    clitics = ["'m", "'re", "'s", "'ll", "'ve", "n't"]
    
    tagger = NLPlib()
    print tagger.tag(['/'])
    for line in input_fpntr:
        #output_fpntr.write('|')
        #print tokenize.generate_tokens(line)
        origin = line

        line = re.sub(r'&quot|&amp', '', line)
        line = re.sub(r'\. *?\. *?\.', ' &ellipsis ', line)
        nolinks = re.sub(r'<(.*) .*?>.*?</\1>', '', line) #remove html tags
        nourls = re.sub(r'(?:http://|ftp://|www\.)\S+\.\S+', '', nolinks) #remove urls

        newlinearray = re.findall('([^.]*?[.!?\n]+)', nourls) #separate sentences in the tweet

        tokens = [re.split(r" +", line.strip()) for line in newlinearray] # separate every word using space as separator

        #extract words, punctiation and clitics
        nopunctiation = []
        for sentence in tokens:
            newsentence = []
            for word in sentence:
                newtokens = re.split("('(?:m|re|s|ll|ve|t)|n't|&ellipsis|[^\w\s])", word)
                noempty = [re.sub(r'&ellipsis', '...', newtoken.strip()) for newtoken in newtokens if newtoken.strip() != '']
                newsentence = newsentence + noempty
            if (newsentence != []): nopunctiation.append(newsentence)



        print "|"
        print origin
        #print tokens
        #print nopunctiation
        sent = nopunctiation
        tags = [tagger.tag(sent) for sent in nopunctiation ]
        #print tags

        zipper = lambda x, y, z: [x[i]+y[i]+z[i] for i in range(0, len(x))]
        zipped = [zipper(nopunctiation[i], ['/']*len(tags[i]), tags[i]) for i in range(0, len(tags))]
        #print zipped

        for sentence in zipped:
            for i in range (0, len(sentence)):
                sys.stdout.write(sentence[i])
                if i != len(sentence)-1: sys.stdout.write(' ')
            sys.stdout.write('\n')
                


        print '|'
        #output_fpntr.write(line)  
        #output_fpntr.write('|')

#       noclitics = []
#        for line in newlinearray:
#            prog = re.compile(.*?, flags)            for clitic in clitics:
#                line = line.replace(clitic, " " + clitic)
#            noclitics.append(line)



#        newlinearray = [temparray[i] for i in range (1, len(temparray), 2)] #array of sentences in the tweet

#        noclitics = []
#        for newline in newlinearray:
#            srch = re.search(r"(?P<sub>'(?:m|re|s|ll|ve|t)|n't|[^\w\s])", newline)
#            if srch != None:
#                new = re.sub(srch.group("sub"), " " + srch.group("sub"), newline)
#                noclitics.append(new)
#            else:
#                noclitics.append(newline)

#
#        tokens = [re.split(r" +", line.strip()) for line in newlinearray]
#        tokens2 = []
#        for sentence in tokens:
#            newsentence = []
#            for word in sentence:
#                newwords = re.split("('(?:m|re|s|ll|ve|t)|n't)", word)
#                for newword in newwords:
#                    if  not (newword.strip() in clitics):
#                        newword = re.split("([^\w\s])", newword.strip())
#                        newsentence = newsentence + newword
#                    else:
#                        newsentence = newsentence.append(newword)
#            tokens2.append(newsentence)
##
#        tokens3 = []

        #tokens2 = [re.split(r"") for token in tokens]


    input_fpntr.close()
    output_fpntr.close()   