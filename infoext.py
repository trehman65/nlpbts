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


'''
Types of input:
1 box of 12 colored pencils
1x box of 12 colored pencils
box of 12 colored pencils 1
one box of 12 colored pencils

'''
file = open("/Users/talha/Documents/Workspace/nlpbts/trainmac/files2.txt")
abspath = "/Users/talha/Documents/Workspace/nlpbts/trainmac/"

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

            # strip spaces from stat and end of string
            line = line.strip()
            orgline = line
            # strip punctuation marks from start and end
            line = line.strip(string.punctuation)
            # strip spaces again from start and end
            line = line.strip()

            input = line
            input2 = input

            outfile.write("Input String: " + orgline.replace("\n", "") + "\n")

            input = re.sub(r'([^\s\w]|_)+', '', input)

            words = nltk.word_tokenize(input)
            tags = nltk.pos_tag(words)

            if tags[0][1] == 'CD':

                # print "Quantity:",tags[0][0]
                outfile.write("Quantity: " + tags[0][0] + "\n")
                item = input.replace(tags[0][0], '', 1)

                # print "Item: ",item
                outfile.write("Item: " + item)
                outfile.write("\n\n")

            elif tags[len(tags) - 1][1] == 'CD':
                # print "Quantity:",tags[len(tags)-1][0]
                outfile.write("Quantity: " + tags[len(tags) - 1][0] + "\n")

                item = input.strip(tags[len(tags) - 1][0])
                # print "Item: ",item
                outfile.write("Item: " + item)
                outfile.write("\n\n")

            else:
                outfile.write(evaluateString(input.strip(), dictSubjects) + ": " + input)
                outfile.write("\n\n")


