from lark import Lark, lexer, tree
import sys
from lark import Transformer


# just install lark-parser from pip

grammar = open('grammar3.lark', 'r').read()
parser = Lark(grammar,
              parser='lalr',
              keep_all_tokens=True)

def getString(node, list):
    if type(node) is lexer.Token:
        list.append(str(node))
    if type(node) is tree.Tree:
        for child in node.children:
            getString(child, list)


class AST(Transformer):
    def se(self, children):
        compTree = None
        ifPureExpression = None
        elsePureExpression = None
        for child in children:
            if type(child) is tree.Tree:
                print(child)
                if child.data == 'comparisonexpression':
                    compTree = child
                if child.data == 'pureexpression' and ifPureExpression is None:
                    ifPureExpression = child
                if child.data == 'pureexpression':
                    elsePureExpression = child
        ls1 = []
        ls2 = []
        ls3 = []
        getString(compTree, ls1)
        getString(ifPureExpression, ls2)
        getString(elsePureExpression, ls3)
        print(f'{ls1} {ls2} {ls3}')



def processTree(node, list, prev):
    if type(node) is lexer.Token:
        list.append(node)
        prev.append(node.type)
        return

    # prev.append(node.data)
    for child in node.children:
        processTree(child, list, prev)

def parse(program):
    parse_tree = parser.parse(program)

    x = parse_tree
    x = AST().transform(parse_tree)

    tokens = []
    terminals = []
    for inst in parse_tree.children:
        processTree(inst, tokens, terminals)


def transform():
    text = r'''
    if ((5*r)>10) r-r else if (r==0) r+r else r*r
'''
    # print(f'input: {text}')
    print(f'output: ')
    try:
        parse(text)
    except Exception as e:
        print(e)


transform()