from lark import Lark, lexer, tree
import sys

grammar = open('grammar.lark', 'r').read()
parser = Lark(grammar, parser='lalr', keep_all_tokens=False)

def processTree(node, list, prev):
    if type(node) is lexer.Token and node.type == 'SC':
        list.append('Spark')
        prev.append(node.type)
        return
    if type(node) is lexer.Token and node.type == 'TEXTFILELP':
        prev.append(node.type)
        list.append('read.textFile(')
        return
    if type(node) is lexer.Token and node.type == 'TEXTFILERP':
        list.append(')')
        prev.append(node.type)
        return
    if type(node) is lexer.Token and node.type == 'REDUCELP':
        prev.append(node.type)
        list.append('select(reduceAggregator(')
        return
    if type(node) is lexer.Token and node.type == 'REDUCERP':
        list.append(')).collect()')
        prev.append(node.type)
        return
    if type(node) is lexer.Token and node.type == 'REDUCEBYKEYLP':
        prev.append(node.type)
        list.append('groupByKey(_._1).agg(reduceByKeyAggregator(')
        return
    if type(node) is lexer.Token and node.type == 'REDUCEBYKEYRP':
        list.append('))')
        prev.append(node.type)
        return
    if type(node) is lexer.Token and node.type == 'SORTBYLP':
        prev.append(node.type)
        list.append('map(row=>((')
        return
    if type(node) is lexer.Token and node.type == 'SORTBYRP':
        list.append(')(row), row)).orderBy("_1").map(_._2)')
        prev.append(node.type)
        return
    if type(node) is lexer.Token:
        list.append(node)
        prev.append(node.type)
        return

    prev.append(node.data)
    for child in node.children:
        processTree(child, list, prev)


def parse(program):
    parse_tree = parser.parse(program)
    list = []
    prev = []
    for inst in parse_tree.children:
        processTree(inst, list, prev)

    for token in list:
        print(token, end="")
    # print(f'{prev}')

def transform():
    text = r'''sc.range(8,10)
    .textFile('input.txt')
    .map(<func>)
    .filter(<func>)
    .reduce(<func>)
    .reduceByKey(<func>)
    .sortBy(<func>)
    .collect()
'''
    print(f'input: {text}')
    print(f'output: ')
    try:
        parse(text)
    except Exception as e:
        print(e)


transform()