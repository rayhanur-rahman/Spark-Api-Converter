from lark import Lark, lexer, tree
import sys, Utils, re
from lark import Transformer

closures = ''
assignments = []
pureexpressions = []
varList = []
returnStatement = ''

mapBodies = []

def getString(node, list):
    if type(node) is lexer.Token:
        list.append(node)
    if type(node) is tree.Tree:
        for child in node.children:
            getString(child, list)

class AST(Transformer):
    def map(self, items):
        global returnStatement
        global assignments
        global pureexpressions
        global varList
        global closures

        for assignment in assignments:
            statement = ''
            for item in assignment:
                statement = statement + item
                if item == 'val': statement = statement + ' '
            varList.append(statement)

        global returnStatement
        for pureexpression in pureexpressions:
            for element in pureexpression:
                if element == 'else': returnStatement = returnStatement + ' '
                returnStatement = returnStatement + element
                if element == 'else': returnStatement = returnStatement + ' '

        mapbody = Utils.MapBody()
        mapbody.returnStatement = returnStatement
        mapbody.pureexpressions = pureexpressions
        mapbody.closures = closures
        mapbody.varList = varList
        mapbody.assignments = assignments

        mapBodies.append(mapbody)

        returnStatement = ''
        assignments = []
        pureexpressions = []
        varList = []
        closures = ''

    def ae(self, items):
        assignment = []
        for element in items:
            getString(element, assignment)
        assignments.append(assignment)
        # print(f'ae: {assignments}')

    def pe(self, items):
        pureexpression = []
        for element in items:
            getString(element, pureexpression)
        pureexpressions.append(pureexpression)
        # print(f'pe: {pureexpressions}')

    def te(self, items):
        pureexpression = []
        for element in items:
            getString(element, pureexpression)
        pureexpressions.append(pureexpression)
        # print(f'pe: {pureexpressions}')

    def ce(self, items):
        global closures
        closures = items[0]
        # print(f'ce: {closures}')





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
            tokens[index] = 'spark'

        if terminals[index] == 'MAP':
            tokens[index] = 'selectExpr'


def replaceRangeTokens(tokens, terminals):
    haveSeenRange = False
    pCount = 0

    for index in range(0, len(terminals)):
        if terminals[index] == 'RANGE':
            haveSeenRange = True
        if haveSeenRange and terminals[index] == 'LP':
            pCount += 1
        if haveSeenRange and terminals[index] == 'RP':
            pCount -= 1
            if pCount == 0:
                haveSeenRange = False
                tokens[index] = ').selectExpr("id as _1")'


def replaceMapTokens(tokens, terminals, mapBodies):
    haveSeenMap = False
    pCount = 0
    start = []
    end = []

    for index in range(0, len(terminals)):
        if terminals[index] == 'MAP':
            haveSeenMap = True
            start.append(index)
        if haveSeenMap and terminals[index] == 'LP':
            pCount += 1
        if haveSeenMap and terminals[index] == 'RP':
            pCount -= 1
            if pCount == 0:
                haveSeenMap = False
                end.append(index)
    # for i in range(start[0]+2, end[0], 1):
    #     tokens[i] = ''
    # tokens[11]='abc'
    for index in range(0, len(start), 1):
        for i in range(start[index]+2, end[index], 1):
            tokens[i] = ''
        tokens[start[index]+2] = mapBodies[index].finalSql


def parse(program):
    parse_tree = parser.parse(program)

    tokens = []
    terminals = []
    for inst in parse_tree.children:
        processTree(inst, tokens, terminals)

    x = parse_tree
    x = AST().transform(parse_tree)

    for mapBody in mapBodies:
        sqlstmt = Utils.processAssignmentStatements(mapBody)
        for element in sqlstmt:
            s = Utils.ifRecurse(element)
            Utils.abc(s)
            ls = []
            Utils.xyz(s, ls)
            for x in ls:
                x = x.strip()
            mapBody.sqlStatements.append(ls)

        count = 1
        finalSql = ''
        for sql in mapBody.sqlStatements:
            pattern = r'\b{stringToFind}\b'.format(stringToFind=mapBody.closures)
            pattern2 = r'\b{stringToFind}._[a-zA-Z0-9]+\b'.format(stringToFind=mapBody.closures)
            match2 = re.match(pattern2, ''.join(sql))
            finalStatement = re.sub(pattern, "_1", ''.join(sql))
            finalStatement = '"' + finalStatement + f' as _{count}"'

            if match2:
                finalStatement = re.sub(pattern+'.', "", ''.join(sql))
                finalStatement = '"' + finalStatement + f' as _{count}"'

            if len(finalSql) > 0: finalSql = finalSql + ', '
            finalSql = finalSql + finalStatement
            count += 1
        mapBody.finalSql = finalSql
        # print(mapBody.finalSql)
        # print('end of one map statement\n')

    # print(f'{terminals}')
    replaceLPTokens(tokens, terminals)
    replaceRangeTokens(tokens, terminals)
    replaceMapTokens(tokens, terminals, mapBodies)

    for token in tokens:
        if token == 'if' or token == 'else' or token == 'val':
            print(' ', end="")
        print(token, end="")
        if token == 'if' or token == 'else' or token == 'val':
            print(' ', end="")

    print('')

def transform():
    # text = r'''sc.range(8,10)
    # .map(x=>x+length)
    # .map(i => {val j = i%3; (i, if (j==0) i*10 else i*2 ) } )
    # .map(r=> r._1+r._2)
    # .collect()
# '''
    input = open('input.txt', 'r')
    text = input.read()
    print('input:')
    print(text, end='\n\n')
    print(f'output: ')
    try:
        parse(text)
    except Exception as e:
        print(e)


transform()