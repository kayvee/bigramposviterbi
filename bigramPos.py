import pickle
import math #math.log(x) to change score to log form

# Part 1: build trellis

# 2d dictionary of probabilities
# A = transition probabilities
# A[tag1][tag2] = P(tag2|tag1)
A = pickle.load(open('A.pickle'))

# B = emission probabilities
# B[tag][word] = P(word|tag)
B = pickle.load(open('B.pickle'))

def buildTrellis(words):
    trellis = [] # list (order of columns) of dictionaries (content of columns)

    # base first column
    first_column = {"<s>" : [0.0, None]}
    trellis.append(first_column)

    # iterate over words to add columns
    for i in range(1, len(words)):
        word = words[i] #latest word
        pc = trellis[-1] #previous column in trellis
        trellis.append(createColumn(pc, word)) #add new column

    return trellis

def createColumn(prevCol, word):
    #
    currentCol = {}
    for prev_state in prevCol: #from each prev state in previous column
        reachables = A[prev_state].keys() # list reachable states
        for reachable in reachables: #for each reachable state
            if word in B[reachable].keys(): # check if reachable can generate word
                if not reachable in currentCol:
                    currentCol[reachable] = [None, None] #[log-delta, crumb]
                score = prevCol[prev_state][0] #log-delta from previous state
                score += math.log(A[prev_state][reachable])
                score += math.log(B[reachable][word])
                if score > currentCol[reachable][0]: # if score is better
                    currentCol[reachable] = [score, prev_state] #update probabilities

    return currentCol

# Part 2: track-back, follow the bread-crumbs
def tag(sent):
    words = ["<s>"] + sent.split() + ["</s>"]
    t = buildTrellis(words)
    return best(t)

def best(trellis):
    # Find the best path i the trellis
    crumbs = ['</s>'] # store crumbs here
    for i in range(len(trellis)-1, 0, -1):
        crumb = trellis[i][crumbs[-1]][1]
        crumbs.append(crumb)
    crumbs.reverse()
    return crumbs

if __name__ == '__main__':
    fh = open("brown.test", "r")
    fh2 = open("brown.test.answers", "r")

    fh3 = open("brown.test.taggedlines", "w")
    fh4 = open("brown.test.taggedwords", "w")

    for line in fh:
        sent = line.strip()
        tags = tag(sent)[1:-1]
        out = ''
        words = sent.split()

        for i in range(len(words)):
            tagged = words[i] + '_#_' + tags[i]
            fh4.write(tagged + '\n')

            out += words[i] + '_#_' + tags[i] + ' '
        fh3.write(out + '\n')
