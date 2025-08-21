'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 20, 2023.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    max = {}
    mini = {}
    dot = 0
    if len(vec1) >= len(vec2):
        max = vec1
        mini = vec2
    else:
        max = vec2
        mini = vec1
    L1 = list(max.values())
    L2 = list(mini.values())
    for i in mini.keys():
        if i in max.keys():
            j = list(max.keys()).index(i)
            dot += mini[i]*L1[j]
    if norm(vec1) == 0 or norm(vec2) == 0:
        return 0.0
    else:
        return dot / (norm(vec1) * norm(vec2))


def uniquelist(sentence):
    L = []
    for i in range(0,len(sentence)):
        for j in range(0,len(sentence[i])):
            L.append(sentence[i][j])
    for k in range(0,len(L)):
         num = L.count(L[k])
         if num > 1:
             L.remove(L[k])
             k-=1
    return L

def listsContainWord(sentence,w):
    L = []
    for i in range(0,len(sentence)):
        if w in sentence[i]:
            L.append(i)
    return L

'''def build_semantic_descriptors(sentences):
    L = uniquelist(sentences)
    listOfIndex = []
    semantic_overall = {}
    semantic = {}
    for word in L:
        for i in range(0,len(sentences)):
            if word in sentences[i]:
                listOfIndex.append(i)
        for j in listOfIndex:
            for k in range(0,len(sentences[j])):
                semantic[sentences[j][k]] = sentences[j].count(sentences[j][k])
        listOfIndex = []
        semantic_overall[word] = semantic
        semantic = {}
    return semantic_overall'''

def build_semantic_descriptors(sentences):
    semantic = {}
    for sentence in sentences:
        i = 0
        j = 0
        for target in sentence:
            if sentence.count(target) > 1:
                j += 1
            for word in sentence:
                if sentence.count(target) > 1 and j != 1:
                    break
                x = sentence.count(word)
                if target != word:
                    if target in semantic and word in semantic[target]:
                        i += 1
                        if x == 1 or i == 1:
                            semantic[target][word] += 1
                    elif target in semantic:
                        i+=1
                        semantic[target][word] = 1
                    else:
                        i+=1
                        semantic[target] = {}
                        semantic[target][word] = 1
            i = 0
    return semantic

def combine(d1,d2):
    d = {}
    if len(d1) >= len(d2):
        for word in d1:
            if word in d2:
                d[word] = d1[word] + d2[word]
                del d2[word]
            else:
                d[word] = d1[word]
        for word in d2:
            d[word] = d2[word]
    if len(d1) < len(d2):
        for word in d2:
            if word in d1:
                d[word] = d1[word] + d2[word]
                del d1[word]
            else:
                d[word] = d2[word]
        for word in d1:
            d[word] = d1[word]
    return d

def test_build_semantic_descriptors_05(self):
       '''05: overall'''
       slist = list = [['this', 'is', 'file', 'one'],
                    ['this', 'is', 'file', 'two'],
                    ['file', 'two', 'has', 'two', 'sentences'],
                    ['this', 'is', 'file', 'three'],
                   ['file', 'three', 'has', 'three', 'sentences'],
                   ['this', 'is', 'the', 'third', 'sentence']]
       vecs = build_semantic_descriptors(slist)
       expected = {'this': {'is':4, 'file':3, 'one':1, 'two':1, 'three':1, 'the':1, 'third':1, 'sentence':1},
'is': {'this':4, 'file':3, 'one':1, 'two':1, 'three':1, 'the':1, 'third':1, 'sentence':1},
'file': {'this':3, 'is':3, 'one':1, 'two':2, 'has':2, 'sentences':2, 'three':2},
'one': {'this':1, 'is':1, 'file':1},
'two': {'this':1, 'is':1, 'file':2, 'has':1, 'sentences':1},
'has': {'file':2, 'two':1, 'sentences':2, 'three':1},
'sentences': {'file':2, 'two':1, 'three':1, 'has':2},
'three': {'this': 1, 'is': 1, 'file': 2, 'has': 1, 'sentences': 1},
'the': {'this':1, 'is':1, 'third':1, 'sentence':1},
'third': {'this':1, 'is':1, 'the':1, 'sentence':1},
'sentence': {'this':1, 'is':1, 'the':1, 'third':1}}
       if vecs == expected:
           print('Passed')
       else:
           print('Failed')

def build_semantic_descriptors_from_files(filenames):
    L = []
    st = ""
    start = 0
    cL = []
    for filename in filenames:
        text = open(filename,"r",encoding="latin1")
        txt = text.read().lower()
        for char in txt:
            if char == "." or char == "!" or char == "?":
                txt = txt.replace(char,"*")
        for i in range(0,len(txt)):
            if txt[i] == "*":
                L.append(txt[start:i])
                start = i+1
        for i in range(0,len(L)):
            for char in L[i]:
                if char == "," or char == "-" or char == "--" or char == ":" or char == ";":
                    L[i] = L[i].replace(char," ")

            st = L[i]


            sl = st.split()
            if len(sl) > 0:
                cL.append(sl)

        L = []
        start = 0

    return build_semantic_descriptors(cL)


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    max = -100
    most = ""
    for candidate in choices:
        if candidate not in semantic_descriptors:
            score = -1
        else:
            v1 = semantic_descriptors[candidate]
            v2 = semantic_descriptors[word]
            score = similarity_fn(v1, v2)
        if score > max:
            max = score
            most = candidate
    return most


def count_words_in_lines(filename):
    with open(filename, "r") as file:
        first = file.readline().strip()
        words = first.split()
        num = len(words)

        return num


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    text = open(filename, "r", encoding="latin1")
    txt = text.read()
    txt = txt.split()
    total = len(txt)/count_words_in_lines(filename)
    correct = 0
    L =[]
    for i in range(0,len(txt),count_words_in_lines(filename)):
        L.append(txt[i:i+count_words_in_lines(filename)])
    for i in range(0,len(L)):
        most = most_similar_word(L[i][0], L[i][2:],semantic_descriptors, similarity_fn)
        if most == L[i][1]:
            correct += 1
    return (correct / total)*100




if __name__ == '__main__':
    slist = [['this', 'is', 'file', 'one'],
             ['this', 'is', 'file', 'two'],
             ['file', 'two', 'has', 'two', 'sentences'],
             ['this', 'is', 'file', 'three'],
             ['file', 'three', 'has', 'three', 'sentences'],
             ['this', 'is', 'the', 'third', 'sentence']]
    vecs = {'this': {'is': 4, 'file': 3, 'one': 1, 'two': 1, 'three': 1, 'the': 1, 'third': 1, 'sentence': 1},
            'is': {'this': 4, 'file': 3, 'one': 1, 'two': 1, 'three': 1, 'the': 1, 'third': 1, 'sentence': 1},
            'file': {'this': 3, 'is': 3, 'one': 1, 'two': 2, 'has': 2, 'sentences': 2, 'three': 2},
            'one': {'this': 1, 'is': 1, 'file': 1},
            'two': {'this': 1, 'is': 1, 'file': 2, 'has': 1, 'sentences': 1},
            'has': {'file': 2, 'two': 1, 'sentences': 2, 'three': 1},
            'sentences': {'file': 2, 'two': 1, 'three': 1, 'has': 2},
            'the': {'this': 1, 'is': 1, 'third': 1, 'sentence': 1},
            'third': {'this': 1, 'is': 1, 'the': 1, 'sentence': 1},
            'sentence': {'this': 1, 'is': 1, 'the': 1, 'third': 1}}
    #print(build_semantic_descriptors(slist))
    #test_build_semantic_descriptors_05(slist)
    #print(build_semantic_descriptors_from_files(["c_file1.txt","c_file2.txt","c_file3.txt"]))
    #sem_descriptors = build_semantic_descriptors_from_files(["file2.txt","file3.txt"])
    #res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
    #print(res, "percent of the guesses were correct")
    print(most_similar_word("third",['four','siavash','kaldi'],vecs,cosine_similarity))