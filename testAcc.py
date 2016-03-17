fh3 = open("brown.test.taggedlines", "r")
taggedLines = []
for line in fh3:
    stripped = line.strip()
    taggedLines.append(stripped)

fh4 = open("brown.test.taggedwords", "r")
taggedWords = []
for line in fh4:
    stripped = line.strip()
    split = stripped.split()
    taggedWords += split

fh2 = open("brown.test.answers", "r")
taggedLinesAnswer = []
for line in fh2:
    stripped = line.strip()
    taggedLinesAnswer.append(stripped)

taggedWordsAnswer = []
for line in taggedLinesAnswer:
    split = line.split()
    taggedWordsAnswer += split


accuracyWords = {"right" : 0, "wrong" : 0, "total" : 0}
for i in range(len(taggedWords)): #range(len(taggedWords)):
    accuracyWords["total"] += 1
    if taggedWords[i] == taggedWordsAnswer[i]:
        accuracyWords["right"] += 1
    else:
        accuracyWords["wrong"] += 1

accuracyLines = {"right" : 0, "wrong" : 0, "total" : 0}
for i in range(len(taggedLines)):
    accuracyLines["total"] += 1
    if taggedLines[i] == taggedLinesAnswer[i]:
        accuracyLines["right"] += 1
    else:
        accuracyLines["wrong"] += 1

print "Word accuracy: ", float(accuracyWords["right"]) / accuracyWords["total"]
print "Sentence accuracy: ", float(accuracyLines["right"]) / accuracyLines["total"]
