import sys
from NLPlib import *
import re

#anything more than two dots treat like an ellipsis
reg_ellipsis = "\.[ \t]*\.(?:[ \t]*\.)*"
reg_ellipsis_obj = re.compile(reg_ellipsis)

reg_dashes = "-[ \t]*-(?:[ \t]*-)*"

reg_mult_punct = "[!?\r\n]+(?:(?:\s+[!?\r\n]+)|[ \t]*[\"\'])*" #handles quote at the end
reg_mult_punct_obj = re.compile(reg_mult_punct)

reg_period = "\.(?:[ \t]*\")*[\r\n]*"
reg_period_obj = re.compile(reg_period)

reg_hashtag = "<[^<>]+?>#(?P<hashtag>\S+?)</[^<>]+?>"
reg_hashtag_obj = re.compile("<[^<>]+?>#(?P<hashtag>\S+?)</[^<>]+?>")

abbreviations = list()

#reg_multiple
#TODO Questions
#elipsis after punctioation EX: But I am no nervous record!  ...

#TODO Extra things
#Add smiles support
#add special html characters support

def separate_sentences(line):
    #TODO NEED TO DO checking of a chaacter after !?
    regex = "(" + reg_ellipsis + "|" + reg_mult_punct + "|" + reg_period + ")"
    tokens = re.split(regex, line)
    #tokens = map(lambda x: x.strip(), tokens)
    tokens = filter(lambda x: x.strip() != '', tokens) #filter out empty strings
    for i in range(len(tokens)):
        if i + 1 < len(tokens):
            token = tokens[i].strip()
            next_token = tokens[i+1].strip()
            first_ch = next_token[0]

            if reg_ellipsis_obj.match(token):
                #ellipsis at the beggining of the sentece
                if i == 0 or (i > 0 and (reg_period_obj.match(tokens[i-1].strip()) or reg_mult_punct_obj.match(tokens[i-1].strip()))):
                    if not (first_ch.isalpha() and first_ch.isupper()): 
                        tokens[i] += '\n'
                else:
                    if not ((first_ch.isalpha() and first_ch.islower()) or first_ch.isdigit() or first_ch == '!' or first_ch == '?'):
                        tokens[i] += '\n'
            elif reg_mult_punct_obj.match(token):
                tokens[i] += '\n'
            elif reg_period_obj.match(token):
                if not (first_ch.isalpha() and first_ch.islower()):
                    if i > 0:
                        words = re.split(' +', tokens[i-1])
                        if not (len(words) > 0 and (words[-1].lower() + '.') in abbreviations):
                            tokens[i] += '\n'
                    else:
                        tokens[i] += '\n'
            
        else:
            tokens[i] += '\n'

    result = "".join(tokens)

    return result


def remove_html_url(line):
    #remove hashtags
    s = reg_hashtag_obj.search(line)
    if s: line = reg_hashtag_obj.sub(s.group("hashtag"), line)

    #remove html tags
    line = re.sub("@?<[^<>]+?>", '', line)

    #TODO check what characters are allowed in the urls
    line = re.sub("(?:https?://|ftp://|www\.)?\S+\.(?:edu|gov|int|mil|net|org|com|ca|cn)(?:/\S*)*", '', line) #remove urls
    return line

def remove_html_special_char(line):
    #substitute &quot;, &amp;, &lt; &gt; with appropriate symbol
    line = re.sub("&quot;", '"', line)
    line = re.sub("&amp;", '&', line)
    line = re.sub("&lt;", '<', line)
    line = re.sub("&gt;", '>', line)
    return line

#TODO find a better name
#def sub_html_special_char(newtoken):
#    newtoken = re.sub("&hellip;", '...', newtoken)
#    newtoken = re.sub("&mdash;", "--", newtoken)
#    return newtoken

def handle_ellipsis(line):
    #mark the ellipsis that indicates the end of the sentece when
    #it is not followed by the word with leading lowercase letter or a number
    #print line
    tokens = re.split("(\.[ \t]?\.[ \t]?\.(?:[ \t]*\.)*)", line)
    tokens = map(lambda x: x.strip(), tokens)
    tokens = filter(lambda x: x != '', tokens)
    #print tokens
      
    for i in range(len(tokens)):
        match = re.compile("\.[ \t]?\.[ \t]?\.(?:[ \t]*\.)*").match(tokens[i])
        if match:
            print "MATCH!!"
            if i < len(tokens) - 1:
                t = tokens[i+1][0]
                if t.strip() != "":
                    if not (t.isalpha() and t.islower()) and not t.isdigit():
                        tokens[i] += "\n"

    #print tokens
    result = " ".join(tokens)
    #print result
    return result

def load_abbreviations():
    abrv_1 = open("./Wordlists/abbrev.english", "r").read().split('\n')
    abrv_2 = open("./Wordlists/pn_abbrev.english", "r").read().split('\n')
    abrv_1.pop()
    abrv_2.pop()
    return  map(lambda x : x.lower(), abrv_1 + abrv_2)
    #TODO add U.S. to abbrivations
    #print abbreviations

if __name__ == "__main__":
    input_fpntr = open(sys.argv[1], "r")
    output_fpntr = open(sys.argv[2], "w")
    clitics = ["'m", "'re", "'s", "'ll", "'ve", "n't"]
    abbreviations =  load_abbreviations()
    tagger = NLPlib()
    
    for line in input_fpntr:
        #output_fpntr.write('ORG:' + line + '\n') #TODO: delete
        
        #substitute ...(ellipsis) with &hellip; to avoid multiple periods
        #line = re.sub("\.[ \t]?\.[ \t]?\.[ \t]?(?:\.[ \t]?)*", " &hellip; ", line)
        #substitute em dash multiple dashes
        #line = re.sub("--", " &mdash; ", line)
        #output_fpntr.write(line+"\n")
        line = remove_html_url(line)
        #output_fpntr.write(line+"\n")
        line = remove_html_special_char(line)
        #output_fpntr.write(line+"\n")
        line = separate_sentences(line)
        #output_fpntr.write(line)
      
        #line = handle_ellipsis(line)
        #line = handle_dashes(line)
        #print line
        newlinearray = re.findall("[^\r\n]+?[\r\n]+?", line) #separate sentences in the tweet
        #output_fpntr.write(str(newlinearray)+"\n")
        tokens = [re.split("[ \t]+", line.strip()) for line in newlinearray] # separate every word using space as separator
#        print tokens
#        #extract words, punctiation and clitics
        nopunctiation = []
        for sentence in tokens:
            newsentence = []
            for word in sentence:
                newtokens = re.compile("('(?:m|re|s|ll|ve|t)|n't|#\S+|\.[ \t]?\.(?:[ \t]*\.)*|-[ \t]*-(?:[ \t]*-)*|[!?\s]+|[^\w\s])", re.IGNORECASE).split(word)
                noempty = [newtoken.strip() for newtoken in newtokens if newtoken.strip() != '']
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
        #output_fpntr.write('##########################################################\n')
    #close file pointers
    input_fpntr.close()
    output_fpntr.close()
    print("Done")
