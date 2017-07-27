import os
import csv
import nltk
import numpy

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

def list_files(path):
    # returns a list of names (with extension, without full path) of all files
    # in folder path
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)
    return files

def evaluateString(inputString, dictSubjects):
    
    inputString=inputString.lower()

    if inputString.replace('.', '', 1).isdigit():
        return "quantity"
    elif dictSubjects.__contains__(inputString):
        return "subject"
    elif containsNoun(inputString) and not containsPOS(inputString, "PRT") and not(containsPOS(inputString, "ADP") or containsPOS(inputString, "DET") or containsPOS(inputString, "ADV")):
        return "item"
    elif containsPOS(inputString, "ADP") or containsPOS(inputString, "DET") or containsPOS(inputString, "PRT") or not containsPOS(inputString, "VERB") or not containsPOS(inputString, "NUM"):
        return "comment"

    return "none"


dictSubjects = set()
with open("dictSubjects.txt") as f:
    content = f.readlines()
    for line in content:
        line = line.strip().lower()
        if len(line) == 0:
            continue
        dictSubjects.add(line)

file = open("/Users/talha/Documents/Workspace/nlpbts/train/62.png.txt")
for line in file.readlines():
    print evaluateString(line.replace("\n",""),dictSubjects),": ",line.replace('\n','')


