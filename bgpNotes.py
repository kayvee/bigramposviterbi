import pickle
import math #math.log(x) to change score to log form

# Part 1: build trellis

# 2d dictionary of probabilities
# A = transition probabilities
# A[tag1][tag2] = P(tag2|tag1) (4)
A = pickle.load(open('A.pickle'))

# B = emission probabilities
# B[tag][word] = P(word|tag)
B = pickle.load(open('B.pickle'))

#trellis = list of dictionaries, one for each column in it
#lists because we need to know the order of columns
#dictionaries because we need to know the states in the column
def buildTrellis(A, B, words):
    #Build a trellis as a list of dictionaries:
    # 1 one dictionary per column
    # 2 one key per state in column
    # 3 d[key] = [log-delta, crumb]
    # (3-1) log-delta(state) = max | log-delta(prev-state) + log(A[prev-state][state]) + log(B[state][word])) |
    # (3-2) crumb = argmax log-delta(state)
    # Build the trellis in following procedure:
    trellis = []
    # 1 first column
    first_column = {"<s>" : [0.0, None]}
    trellis.append(first_column)
    # 2 use previous column to create next column/add column based on previous column
    # 3 repeat step 2 until we run out of words
    for i in range(1, len(words)):
        word = words[i] #latest word
        pd = trellis[-1] #last entry/previous column in trellis
        trellis.append(createColumn(pd, A, B, word)) #add new column

    return trellis

#where the prevCol is the previous column dictionary
def createColumn(prevCol, A, B, word):
    # Create a column of states to add to our trellis
    # What are those states?
    # (1) Reachable states (from previous column)
    # (2) Generating state (can spit out this word)
    currentCol = {}
    for prev_state in prevCol:
        reachables = A[prev_state].keys()
        for reachable in reachables:
            if word in B[reachable].keys():
                if not reachable in currentCol:
                    currentCol[reachable] = [None, None] #[log-delta, crumb]
                score = prevCol[prev_state][0] #log-delta from previous state
                score += math.log(A[prev_state][reachable])
                score += math.log(B[reachable][word])
                if score > currentCol[reachable][0]: # is new score better?
                    currentCol[reachable] = [score, prev_state]

    return currentCol

def padSentence(line):
    padded = "<s> " + line + " </s>"
    return padded

# Part 2: track-back, follow the bread-crumbs
def best(trellis):
    # Find the best path i the trellis
    crumbs = ['</s>'] # store crumbs here
    for i in range(len(t)-1, 0, -1):
        crumb = trellis[i][crumbs[-1]][1]
        crumbs.append(crumb)
    crumbs.reverse()
    return crumbs

def tag(A, B, sent):
    words = ['<s>'] + sent.split() + ['</s>']
    t = build(A, B, words)
    return best(t)

if __name__ == '__main__':
    sent = "you are forgetting your place '' ." #toy example
    words = ['<s>'] + sent.split() + ['</s>']

    #test if buildTrellis works
    t = buildTrellis(A, B, words)
    print t
    # for i in range(len(t)):
    #     print "Column #:", i
    #     for states in t[i]:
    #         print "State:", [t][i][states]
    print sent
    print best(t)
