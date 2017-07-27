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
    if inputString.replace('.', '', 1).isdigit():
        return "quantity"
    elif dictSubjects.__contains__(inputString):
        return "subject"
    elif containsNoun(inputString) and not containsPOS(inputString, "PRT") and not(containsPOS(inputString, "ADP") or containsPOS(inputString, "DET") or containsPOS(inputString, "ADV")):
        return "item"
    elif containsPOS(inputString, "ADP") or containsPOS(inputString, "DET") or containsPOS(inputString, "PRT") or not containsPOS(inputString, "VERB") or not containsPOS(inputString, "NUM"):
        return "comment"

    return "none"

# get ground truth for later evaluation
groundTruth = dict()
filesList = list_files("csvs/")
for file in filesList:
    with open("csvs/" + file) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if not len(row[1]) == 0:
                groundTruth[row[1].strip().lower()] = "subject"
            if not len(row[2]) == 0:
                groundTruth[row[2].strip().lower()] = "item"
            if not len(row[3]) == 0:
                groundTruth[row[3].strip().lower()] = "quantity"
            if not len(row[4]) == 0:
                groundTruth[row[4].strip().lower()] = "comment"

# EXPERIMENTATION
# list = ["ADJ", "ADP", "ADV", "CONJ", "DET", "NOUN", "NUM", "PRT", "PRON", "VERB", ".", "X"]
# for POS in list:
#     nums = []
#     nums2 = []
#     for item in groundTruth:
#         if groundTruth[item] == "item":
#             nums.append(averageDensity(item,POS))
#         if groundTruth[item] == "comment":
#             nums2.append(averageDensity(item,POS))
#     print "\n\nitem:::" + POS
#     print numpy.mean(nums)
#     print numpy.std(nums)
#     print "comment:::" + POS
#     print numpy.mean(nums2)
#     print numpy.std(nums2)

# get testing results
# loading subject dictionary
dictSubjects = set()
with open("dictSubjects.txt") as f:
    content = f.readlines()
    for line in content:
        line = line.strip().lower()
        if len(line) == 0:
            continue
        dictSubjects.add(line)
        
results = dict()
filesList = list_files("csvs/")
for file in filesList:
    with open("csvs/" + file) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            for someString in row[1:5]:
                if not len(someString) == 0:
                    someString = someString.strip().lower()
                    results[someString] = evaluateString(someString, dictSubjects)




# evaluate results
### DETAILED RESULTS
truePositives = dict()
truePositives["subject"] = 0
truePositives["quantity"] = 0
truePositives["item"] = 0
truePositives["comment"] = 0
truePositives["none"] = 0
falsePositives = dict()
falsePositives["subject"] = 0
falsePositives["quantity"] = 0
falsePositives["item"] = 0
falsePositives["comment"] = 0
falsePositives["none"] = 0
trueNegatives = dict()
trueNegatives["subject"] = 0
trueNegatives["quantity"] = 0
trueNegatives["item"] = 0
trueNegatives["comment"] = 0
trueNegatives["none"] = 0
falseNegatives = dict()
falseNegatives["subject"] = 0
falseNegatives["quantity"] = 0
falseNegatives["item"] = 0
falseNegatives["comment"] = 0
falseNegatives["none"] = 0

for item in results:
    if results[item] == groundTruth[item]:
        truePositives[results[item]] += 1
    else:
        falsePositives[results[item]] += 1
for item in groundTruth:
    if item not in results or groundTruth[item] != results[item]:
        falseNegatives[groundTruth[item]] += 1

print "precision for item: " + str(float(truePositives["item"]) / (truePositives["item"] + falsePositives["item"]))
print "precision for quantity: " + str(float(truePositives["quantity"]) / (truePositives["quantity"] + falsePositives["quantity"]))
print "precision for comment: " + str(float(truePositives["comment"]) / (truePositives["comment"] + falsePositives["comment"]))
print "precision for subject: " + str(float(truePositives["subject"]) / (truePositives["subject"] + falsePositives["subject"]))

print "\nrecall for item: " + str(float(truePositives["item"]) / (truePositives["item"] + falseNegatives["item"]))
print "recall for quantity: " + str(float(truePositives["quantity"]) / (truePositives["quantity"] + falseNegatives["quantity"]))
print "recall for comment: " + str(float(truePositives["comment"]) / (truePositives["comment"] + falseNegatives["comment"]))
print "recall for subject: " + str(float(truePositives["subject"]) / (truePositives["subject"] + falseNegatives["subject"]))
################