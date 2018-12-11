import sys, re

def checkForNumber(text):
    pattern = r'^[0-9]+$'
    match = re.match(pattern, text)
    if match: return (True, 'number')
    else: return False

def checkForIdentifier(text):
    pattern = r'^[_a-zA-Z]+[_a-zA-Z0-9]*$'
    match = re.match(pattern, text)
    if match: return (True, 'id')
    else: return False

def checkForString(text):
    pattern = r'^"[\s\S]*"$'
    match = re.match(pattern, text)
    if match: return (True, 'string')
    else: return False

def checkForChar(text):
    pattern = r"^'[a-zA-Z0-9]?'$"
    match = re.match(pattern, text)
    if match: return (True, 'char')
    else: return False

def checkForSymbol(text):
    pattern = r'^[*-+/!@#$%^&()={}\|\[\];:,<.>?~`]{1}$'
    match = re.match(pattern, text)
    if match: return (True, 'symbol')
    else: return False

def checkForWhiteSpace(text):
    pattern = r'^[\s]+$'
    match = re.match(pattern, text)
    if match: return (True, 'space')
    else: return False

def getToken(text):
    if checkForNumber(text): return checkForNumber(text)[1]
    if checkForIdentifier(text): return checkForIdentifier(text)[1]
    if checkForString(text): return checkForString(text)[1]
    if checkForChar(text): return checkForChar(text)[1]
    if checkForSymbol(text): return checkForSymbol(text)[1]
    if checkForWhiteSpace(text): return checkForWhiteSpace(text)[1]
    return 'none'

def getFirstNChar(text, n):
    return text[0:n]


def replaceLPTokens(tokens):
    for index in range(0, len(tokens)):
        if tokens[index] == 'sc':
            tokens[index] = 'spark'

        if tokens[index] == 'textFile':
            tokens[index] = 'read.textFile'

        if tokens[index] == 'reduce':
            tokens[index] = 'select(reduceAggregator'

        if tokens[index] == 'reduceByKey':
            tokens[index] = 'groupByKey(_._1).agg(reduceByKeyAggregator'

        if tokens[index] == 'sortBy':
            tokens[index] = 'map(row=>('

def replaceReduceTokens(tokens):
    haveSeenReduce = False
    pCount = 0

    for index in range(0, len(tokens)):
        if tokens[index] == 'select(reduceAggregator':
            haveSeenReduce = True
        if haveSeenReduce and tokens[index] == '(':
            pCount += 1
        if haveSeenReduce and tokens[index] == ')':
            pCount -= 1
            if pCount == 0:
                haveSeenReduce = False
                tokens[index] = ')).collect()'

def replaceReduceByKeyTokens(tokens):
    haveSeenReduceByKey = False
    pCount = 0

    for index in range(0, len(tokens)):
        if tokens[index] == 'groupByKey(_._1).agg(reduceByKeyAggregator':
            haveSeenReduceByKey = True
        if haveSeenReduceByKey and tokens[index] == '(':
            pCount += 1
        if haveSeenReduceByKey and tokens[index] == ')':
            pCount -= 1
            if pCount == 0:
                haveSeenReduceByKey = False
                tokens[index] = '))'

def replaceSortByTokens(tokens):
    haveSeenSortBy = False
    pCount = 0

    for index in range(0, len(tokens)):
        if tokens[index] == 'map(row=>(':
            haveSeenSortBy = True
        if haveSeenSortBy and tokens[index] == '(':
            pCount += 1
        if haveSeenSortBy and tokens[index] == ')':
            pCount -= 1
            if pCount == 0:
                haveSeenSortBy = False
                tokens[index] = ')(row), row)).orderBy("_1").map(_._2)'

def transform(text):
    text = text.replace('\n', '')

    n = 1
    ls = []
    isAlreadyMatch = False
    while (len(text) > 0):
        if n <= len(text):
            chunk = getFirstNChar(text, n)
        else:
            ls.append(getFirstNChar(text, n))
            break
        token = getToken(chunk)
        if token != 'none':
            isAlreadyMatch = True
            n += 1
        if token == 'none':
            if isAlreadyMatch:
                ls.append(getFirstNChar(text, n - 1))
                text = text[n - 1:]
                n = 1
                isAlreadyMatch = False
            else:
                n += 1

    for x in ls:
        print(f'{x}', end='')

    print('')

    replaceLPTokens(ls)
    replaceReduceTokens(ls)
    replaceReduceByKeyTokens(ls)
    replaceSortByTokens(ls)

    for x in ls:
        print(f'{x}', end='')

# text = r'''sc.range(8,10)
# .textFile("input.txt")
# .map(x=>y)
# .reduce(x=>y)
# .reduceByKey(x=>y)
# .sortBy(x=>y)
# .reduce(a=>b)
# '''

text = r'''
sc.range(1,100)
  .filter(i => (i%8 == 0))
  .map(i => (if(i%2 == 0) i/4, 2))
  .reduceByKey((a:Int, b:Int) => a+b)
  .collect()
  '''

text = input('please provide an input:\n')

transform(text)
