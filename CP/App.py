from lark import Lark, lexer, tree
import sys

# just install lark-parser from pip

grammar = open('grammar.lark', 'r').read()
parser = Lark(grammar, parser='lalr', keep_all_tokens=True)

def processTree(node, list, prev):
    if type(node) is lexer.Token:
        list.append(node)
        prev.append(node.type)
        return

    # prev.append(node.data)
    for child in node.children:
        processTree(child, list, prev)

def replaceLPTokens(tokens, terminals):
    for index in range(0, len(terminals)):
        if terminals[index] == 'SC':
            tokens[index] = 'Spark'

        if terminals[index] == 'TEXTFILE':
            tokens[index] = 'read.textFile'

        if terminals[index] == 'REDUCE':
            tokens[index] = 'select(reduceAggregator'

        if terminals[index] == 'REDUCEBYKEY':
            tokens[index] = 'groupByKey(_._1).agg(reduceByKeyAggregator'

        if terminals[index] == 'SORTBY':
            tokens[index] = 'map(row=>('


def replaceReduceTokens(tokens, terminals):
    haveSeenReduce = False
    pCount = 0

    for index in range(0, len(terminals)):
        if terminals[index] == 'REDUCE':
            haveSeenReduce = True
        if haveSeenReduce and terminals[index] == 'LP':
            pCount += 1
        if haveSeenReduce and terminals[index] == 'RP':
            pCount -= 1
            if pCount == 0:
                haveSeenReduce = False
                tokens[index] = ')).collect()'

def replaceReduceByKeyTokens(tokens, terminals):
    haveSeenReduceByKey = False
    pCount = 0

    for index in range(0, len(terminals)):
        if terminals[index] == 'REDUCEBYKEY':
            haveSeenReduceByKey = True
        if haveSeenReduceByKey and terminals[index] == 'LP':
            pCount += 1
        if haveSeenReduceByKey and terminals[index] == 'RP':
            pCount -= 1
            if pCount == 0:
                haveSeenReduceByKey = False
                tokens[index] = '))'

def replaceSortByTokens(tokens, terminals):
    haveSeenSortBy = False
    pCount = 0

    for index in range(0, len(terminals)):
        if terminals[index] == 'SORTBY':
            haveSeenSortBy = True
        if haveSeenSortBy and terminals[index] == 'LP':
            pCount += 1
        if haveSeenSortBy and terminals[index] == 'RP':
            pCount -= 1
            if pCount == 0:
                haveSeenSortBy = False
                tokens[index] = ')(row), row)).orderBy("_1").map(_._2)'


def parse(program):
    parse_tree = parser.parse(program)
    tokens = []
    terminals = []
    for inst in parse_tree.children:
        # print(f'### {inst}')
        processTree(inst, tokens, terminals)

    # print(f'{terminals}')
    replaceLPTokens(tokens, terminals)
    replaceReduceTokens(tokens, terminals)
    replaceReduceByKeyTokens(tokens, terminals)
    replaceSortByTokens(tokens, terminals)

    for token in tokens:
        if token == 'if' or token == 'else' or token == 'val':
            print(' ', end="")
        print(token, end="")
        if token == 'if' or token == 'else' or token == 'val':
            print(' ', end="")

#handle else


def transform():
    text = r'''sc.range(8,10)
    .textFile('input.txt')
    .map(x => { val z = x % 2; ( x+2, if (z+3>0) x else y ) } )
'''
    print(f'input: {text}')
    print(f'output: ')
    try:
        parse(text)
    except Exception as e:
        print(e)


transform()