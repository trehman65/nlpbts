import nltk
import sys
import re
import os
import csv
import numpy
import string
import enchant
import enchant.checker
import difflib
import json
from enchant.tokenize import get_tokenizer, EmailFilter, URLFilter, WikiWordFilter



def countVerbs(inputString):
    totalVerbs=0
    tokenizedString = nltk.word_tokenize(inputString)
    taggedTokens = nltk.pos_tag(tokenizedString, tagset="universal")
    for token in taggedTokens:
        tag = token[1]
        if tag.find("VERB") != -1:
            totalVerbs += 1
    return totalVerbs


def containsPOS(inputString, POS):
    tokenizedString = nltk.word_tokenize(inputString)
    taggedTokens = nltk.pos_tag(tokenizedString, tagset="universal")
    #print taggedTokens
    for token in taggedTokens:
        #print token
        tag = token[1]
        if tag.find(POS) != -1:
            return True
    return False


def containsNoun(inputString):
    tokenizedString = nltk.word_tokenize(inputString)
    taggedTokens = nltk.pos_tag(tokenizedString, tagset="universal")
    for token in taggedTokens:
        tag = token[1]
        #print tag
        if tag.find("NOUN") != -1:
            return True
    return False


def containsVerb(inputString):
    tokenizedString = nltk.word_tokenize(inputString)
    taggedTokens = nltk.pos_tag(tokenizedString, tagset="universal")
    for token in taggedTokens:
        tag = token[1]
        if tag.find("VERB") != -1:
            return True
    return False


def evaluateString(inputString, dictSubjects):
    inputString = inputString.lower()
    # inputString=inputString.replace(' ','')

    if dictSubjects.__contains__(inputString):
        return "Subject"
    elif containsNoun(inputString) and not containsPOS(inputString, "VERB") and not (
            containsPOS(inputString, "ADP") or containsPOS(inputString, "DET") or containsPOS(inputString, "ADV")):
        return "Item"
    elif containsPOS(inputString, "ADP") or containsPOS(inputString, "DET") or containsPOS(inputString,
                                                                                           "PRT") or not containsPOS(
            inputString, "VERB") or not containsPOS(inputString, "NUM"):
        return "Not a Product"

    return "Not a Product"

    
def dict_check(inputString):
    #print inputString
    tknzr = get_tokenizer("en_US", [URLFilter, EmailFilter, WikiWordFilter])
    d = enchant.DictWithPWL("en_US", "my_pwl.txt")
    words = nltk.word_tokenize(inputString)
    out = ''
   
   
    if str.isdigit(words[0]):
        words = words[1:]
    for w in words:
        #print w
        sub_words_check = 1
        if len(w) >= 2 and d.check(w):# and not str.isdigit(w):
            
            sub_words = tknzr(w)
            #print w, '!!!!!!!!'
            for sub in sub_words:
                #print sub
                if not d.check(sub[0]) and not d.check(sub[0].lower()):
                    #print sub
                    sub_words_check = 0
  
            if sub_words_check == 1:
                #print w
                out = out + w + ' '
   
    
    
    if len(out.strip()) > 2:
        return out.strip()
    else:
        return ''   




def process(inputString):

    wordlabel=[]
    comment=""
    
    line = inputString
    line = line.replace("\n", "")
    # strip spaces from stat and end of string
    line = line.strip()
    #orgline = line
    wordlabel.append(["Input", line])
    
    #print line
    line = line.replace(' w/o ','without')
    line = line.replace(' w/','with ')
    line = line.replace(' Pkg ', ' Package ')
    line = line.replace(' pkg ', ' package ')
    line = line.replace(' Pk ', ' Pack ')
    line = line.replace(' pk ', ' pack ')
    line = line.replace(' pk', ' pack')
    line = line.replace(' Pkt ', ' Packet ')
    line = line.replace(' pkt ', ' packet ')
    line = line.replace(' Ea ', ' Each ')
    line = line.replace('Bx ', 'Box ')
    line = line.replace(' St ', ' Set ')
    line = line.replace(' sht ', ' sheet ')
    line = line.replace(' sht', ' sheet ')
    line = line.replace(' Pr ', ' Pair ')
    line = line.replace('Dz ', 'Dozen ')
    line = line.replace('dz ', 'dozen ')
    line = line.replace('oz.', 'ounce')
    line = line.replace(' x ', ' by ')
    line = line.replace('No. ', 'No-')
    
    #print line
    line = re.sub(r'(?<![a-zA-Z])["](?![a-zA-Z])', '-inch', line) #to replace <"> with <-inch>, only when it comes after a number
    line = re.sub(r'(?<![0-9])[/](?![0-9])', ' or ', line)
    line = re.sub(r'(?<![0-9])[0](?![0-9])', '', line)   

    if line == '':
        return wordlabel


    # strip punctuation marks from start and end
    line = line.strip(string.punctuation)
    # strip spaces again from start and end
    line = line.strip()

    #input = line
    comment = line.split("(")[-1].split(")")[0]
    if comment != line:
        line=line.replace(comment,"")
        line = line.strip(string.punctuation)
        wordlabel.append(["Comment", comment])   


    input = line

    if (countVerbs(line) >= 2):
        #print wordlabel
        wordlabel.append(["Not a Product", line])
        return wordlabel
    else:
        #input = re.sub(r'([^\s\w]|_)+', ' ', input)
        #line = re.sub(r'([^\s\w]|_)+', ' ', line)
        
        
        words = nltk.word_tokenize(input)
        tags = nltk.pos_tag(words)
        #print tags
        if(input.isdigit()):
            wordlabel.append(["Not a Product", line])
            #print wordlabel
            return wordlabel
        

        # first word is a number
        if tags[0][1] == 'CD':
            if len(input.replace(tags[0][0], '', 1).strip()) < 1:
                input = dict_check(line)
                wordlabel.append(["Not a Product", line])
                #print wordlabel
                return wordlabel

            wordlabel.append(["Quantity", tags[0][0]])
            input = dict_check(input)
            #print input
            #wordlabel.append(["Item", input.replace(tags[0][0], '', 1).strip()])
            wordlabel.append(["Item", input.strip()])
        # last word is quantity
        
        elif tags[len(tags) - 1][1] == 'CD':
            wordlabel.append(["Quantity", tags[len(tags) - 1][0]])
            input = dict_check(input)
            #print input
            wordlabel.append(["Item", input.strip(tags[len(tags) - 1][0]).strip()])

        else:
            
            line = dict_check(line)
            wordlabel.append([evaluateString(line.strip(), dictSubjects), line])
            #print wordlabel
      
    return wordlabel



abspath = os.getcwd()


dictSubjects = set()
with open("dictSubjects.txt") as f:
    content = f.readlines()
    for line in content:
        line = line.lower()
        if len(line) == 0:
            continue
        dictSubjects.add(line.replace("\n", ""))



inputpath = sys.argv[1]
filename = inputpath.split('/')[-1]
inputdir = inputpath.replace(filename,"")

file_counter = 0
my_dict_allimages = {}
my_dict_overall = {}

out = 0
outjson=[]

filename = filename.replace("\n", "")
file_txtfile = open(inputpath)

print "Processing: ", filename

out_filename = filename.replace(".txt", ".nltk.json")
outpath = os.path.join(inputdir, out_filename)
outfile = open(outpath, 'w')

my_dict_img = {}
line_counter = 0
for line in file_txtfile.readlines():
    line = line.strip()
    line_counter += 1
    if len(line) > 3:
        if line.find("     "):
            parts= line.split("     ")
            for part in parts:

                if len(part)>1:
                    out = process(part.strip())

        else:

            out =  process(line)



    thisitem={}
    thisitem["Comment"]=""
    thisitem["Label"] = "Not a Product"
    thisitem["Quantity"]=""
    thisitem["Item"]=""

    for arr in out:
        if arr[0] != "Not a Product":
            thisitem[arr[0]] = arr[1].replace("\""," ")

    quant_check = 0

    if (len(thisitem["Item"]) != 0):
        thisitem["Label"] = "Product"

    #process quantity
    if (len(thisitem["Quantity"]) == 0 and len(thisitem["Item"]) != 0):
        for t in nltk.pos_tag([x.lower() for x in nltk.word_tokenize(thisitem["Item"])[:4]]):
            if t[1] == 'NNS':
                quant_check = 1

        if quant_check == 1:
            thisitem["Quantity"]="Multiple"
        else:
            thisitem["Quantity"]="1"


    outjson.append(thisitem)


json.dump(outjson,outfile)

       
