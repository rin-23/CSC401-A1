import string
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Rinat"
__date__ ="$Jan 14, 2012 1:20:52 PM$"
import sys
import tokenize
import re

if __name__ == "__main__":
    input_fname = sys.argv[1]
    output_fname = sys.argv[2]
    input_fpntr = open(input_fname, "r")
    output_fpntr = open(output_fname, "w")
    clitics = ["'m", "'re", "'s", "'ll", "'ve", "n't"]

    for line in input_fpntr:
        #output_fpntr.write('|')
        #print tokenize.generate_tokens(line)
        origin = line
        nolinks = re.sub(r'<(.*) .*?>.*?</\1>', '', line) #remove html tags
        nourls = re.sub(r'(?:http://|ftp://|www\.)\S+\.\S+', '', nolinks) #remove urls

        newlinearray = re.findall('(.*?[.!?\n]+?)', nourls) #separate sentences in the tweet

        tokens = [re.split(r" +", line.strip()) for line in newlinearray] # separate every word usinf space as separator
        
        nopunctiation = []
        for sentence in tokens:
            newsentence = []
            for word in sentence:
                newtokens = re.split("('(?:m|re|s|ll|ve|t)|n't|&amp|&quote|[^\w\s])", word)
                noempty = [newtoken.strip() for newtoken in newtokens if newtoken.strip() != '']
                newsentence = newsentence + noempty
            if (newsentence != []): nopunctiation.append(newsentence)



        print "--------------"
        print origin
        print tokens
        print nopunctiation
  #      print nolinks
        #print nourls
        #  print newlinearray
    #    print noclitics
     #   print tokens2
     #   print "--------------"
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