import nltk
import sys
import re
import os
import csv
import numpy
import string


def averageDensity(inputString, POS):
    totalPOS = 0
    tokenizedString = nltk.word_tokenize(inputString)
    taggedTokens = nltk.pos_tag(tokenizedString, tagset="universal")
    for token in taggedTokens:
        tag = token[1]
        if tag.find(POS) != -1:
            totalPOS += 1
    return float(totalPOS) / len(taggedTokens)

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
    for token in taggedTokens:
        tag = token[1]
        if tag.find(POS) != -1:
            return True
    return False


def containsNoun(inputString):
    tokenizedString = nltk.word_tokenize(inputString)
    taggedTokens = nltk.pos_tag(tokenizedString, tagset="universal")
    for token in taggedTokens:
        tag = token[1]
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
        return "Comment"

    return "None"

def process(inputString):

    wordlabel=[]

    line = inputString

    line = line.replace("\n", "")
    # strip spaces from stat and end of string
    line = line.strip()
    orgline = line
    # strip punctuation marks from start and end
    line = line.strip(string.punctuation)
    # strip spaces again from start and end
    line = line.strip()

    input = line
    wordlabel.append(["Input String", orgline])

    if (countVerbs(line) >= 2):

        wordlabel.append(["Comment", line])
    else:

        input = re.sub(r'([^\s\w]|_)+', '', input)

        words = nltk.word_tokenize(input)
        tags = nltk.pos_tag(words)

        # first word is a number
        if tags[0][1] == 'CD':
            wordlabel.append(["Quantity", tags[0][0]])
            wordlabel.append(["Item", input.replace(tags[0][0], '', 1).strip()])
        # last word is quantity
        elif tags[len(tags) - 1][1] == 'CD':
            wordlabel.append(["Quantity", tags[len(tags) - 1][0]])
            wordlabel.append(["Item", input.strip(tags[len(tags) - 1][0]).strip()])

        else:
            wordlabel.append([evaluateString(line.strip(), dictSubjects), line])

    return wordlabel




abspath = "/Users/talha/PycharmProjects/bts/trainmac/"
file = open(abspath+"files2.txt")


dictSubjects = set()
with open("dictSubjects.txt") as f:
    content = f.readlines()
    for line in content:
        line = line.lower()
        if len(line) == 0:
            continue
        dictSubjects.add(line.replace("\n", ""))

for filename in file.readlines():

    filename = filename.replace("\n", "")
    file = open(abspath + filename)

    print "Processing: ", filename

    filename = filename.replace(".png.txt", ".nltk.out.txt")
    outpath = abspath + filename
    outfile = open(outpath, 'w')


    for line in file.readlines():

        if len(line) > 3:
            print process(line)

