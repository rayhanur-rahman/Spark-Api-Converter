import re, math, sys

class MapBody:
    def __init__(self):
        self.closures = ''
        self.assignments = []
        self.pureexpressions = []
        self.varList = []
        self.returnStatement = ''
        self.sqlStatements = []
        self.finalSql = ''

class Statement:
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value
        self.dependency = []


def processAssignmentStatements(mapBody):
    list = mapBody.varList

    variables = []
    values = []
    statements = []
    variables.append(mapBody.closures)
    statements.append(Statement(mapBody.closures, ''))

    for str in list:
        str = str.split('=')
        variable = str[0].split(' ')
        variables.append(variable[1])
        value = str[1].split(';')
        values.append(value[0])
        statement = Statement(variable[1], value[0])
        statements.append(statement)


    for statement in statements:
        for element in variables:
            if element in statement.value:
                if element is not mapBody.closures:
                    statement.dependency.append(element)

    # for statement in statements:
    #     print(f'{statement.variable} {statement.value} {statement.dependency}')

    for statement in statements:
        if len(statement.dependency) > 0:
            for element in statement.dependency:
                if element is not mapBody.closures:
                    statementForReplace = next(x for x in statements if x.variable == element)
                    pattern = r'\b{stringToFind}\b'.format(stringToFind=element)
                    # statement.value = statement.value.replace(element, '('+ statementForReplace.value+')')
                    statement.value = re.sub(pattern, '(' + statementForReplace.value + ')', statement.value)

    # print('###')

    # for statement in statements:
    #     print(f'{statement.variable} {statement.value} {statement.dependency}')

    # print(mapBody.returnStatement)

    for element in variables:
        if element is not mapBody.closures:
            statementForReplace = next(x for x in statements if x.variable == element)
            pattern = r'\b{stringToFind}\b'.format(stringToFind=element)
            mapBody.returnStatement = re.sub(pattern, '(' + statementForReplace.value + ')', mapBody.returnStatement)




    for index in range(0, len(mapBody.returnStatement), 1):
        if mapBody.returnStatement[index] == '(':
            mapBody.returnStatement = mapBody.returnStatement[0:index] + mapBody.returnStatement[index+1:]
            break

    for index in range(len(mapBody.returnStatement) - 1, -1, -1):
        if mapBody.returnStatement[index] == ')':
            mapBody.returnStatement = mapBody.returnStatement[0:index] + mapBody.returnStatement[index+1:]
            break

    sqlStmts = mapBody.returnStatement.split(',')

    return sqlStmts

line =  'if (r==1) if(r==2) r+1 else r+2 else if(r==3) r+3 else if (r<0) x else y'
# line = 'r+r'

def processIfStatements(line, start, end):
    newLine = ''
    haveSeenIf = False
    pCount = 0
    ifConditionStartIndex = None
    ifConditionEndIndex = None
    ifCondition = ''

    for index in range(0, len(line), 1):
        if line[index] == 'i' and line[index+1] == 'f':
            haveSeenIf = True
        if haveSeenIf and line[index] == '(':
            pCount += 1
            if pCount == 1:
              ifConditionStartIndex = index + 1
        if haveSeenIf and line[index] == ')':
            pCount -= 1
            if pCount == 0:
                haveSeenIf = False
                ifConditionEndIndex = index - 1
                ifCondition = line[ifConditionStartIndex: ifConditionEndIndex + 1]
                break

    ifClauseStartIndex = ifConditionEndIndex + 2
    ifClauseEndIndex = None
    elseClauseStartIndex = None
    ifClause = ''
    elseClause = ''

    for index in range(ifClauseStartIndex, len(line), 1):
        if line[index] == 'e' and line[index+1] == 'l' and line[index+2] == 's' and line[index+3] == 'e':
            ifClauseEndIndex = index - 1
            ifClause = line[ifClauseStartIndex:ifClauseEndIndex+1]
            elseClauseStartIndex = index+4
            elseClause = line[elseClauseStartIndex:]
            break

    return f'if( {ifCondition}, {ifClause}, {elseClause} )'

class IfStatements:
    def __init__(self):
        self.start = None
        self.end = None
        self.sentence = None
        self.comparison = None
        self.ifClause = None
        self.elseClause = None
        self.ifChildren = None
        self.elseChildren = None

class Pair:
    def __init__(self):
        self.start = None
        self.end = None
        self.comparisonStart = None
        self.comparisonEnd = None
        self.sequence = None
        self.parent = None


def ifRecurse(line):
    ifcount = 0
    elsecount = 0
    pairs = []
    s = IfStatements()
    s.sentence = line
    for index in range(0, len(line), 1):
        if len(line) > index + 1 and line[index] == 'i' and line[index+1] == 'f':
            ifcount += 1
            p = Pair()
            p.sequence = ifcount
            p.start = index + 2
            if len(pairs) >0: p.parent = pairs[-1]
            else: p.parent = p
            pairs.append(p)
        if line[index] == 'e' and line[index + 1] == 'l' and line[index+2] == 's' and line[index + 3] == 'e':
            elsecount += 1
            p = pairs.pop(-1)
            p.end = index + 4
            if len(pairs) == 0:

                s.start = p.start
                s.end = p.end

                pCount = 0
                ifConditionStartIndex = 0

                for index in range(s.start, s.end,1):
                    if line[index] == '(':
                        pCount += 1
                        if pCount == 1:
                            ifConditionStartIndex = index + 1
                    if line[index] == ')':
                        pCount -= 1
                        if pCount == 0:
                            ifConditionEndIndex = index - 1
                            s.comparison = line[ifConditionStartIndex: ifConditionEndIndex + 1]
                            break

                s.ifClause = line[ifConditionEndIndex + 2:p.end - 5]
                s.elseClause = line[p.end:]
                break

    return s

def abc(s):
    # print(f'{s.comparison} {s.ifClause} {s.elseClause}')
    if s.comparison is not None:
        if 'if' in s.ifClause:
            s.ifChildren = ifRecurse(s.ifClause)
            abc(s.ifChildren)
        if 'if' in s.elseClause:
            s.elseChildren = ifRecurse(s.elseClause)
            abc(s.elseChildren)

def xyz(s, list):
    # print(f'### {s.sentence} {s.comparison} {s.ifClause} {s.elseClause}')

    if s.comparison is not None:
        list.append('if(')
        list.append(s.comparison)
        list.append(',')
        if s.ifChildren is not None:
            xyz(s.ifChildren, list)
        else:
            list.append(s.ifClause)
        list.append(',')
        if s.elseChildren is not None:
            xyz(s.elseChildren, list)
        else:
            list.append(s.elseClause)
        list.append(')')
    else:
        list.append(s.sentence)


s = ifRecurse(line)
abc(s)
ls = []
xyz(s, ls)


# for x in ls:
#     x = x.strip()
#     print(x, end=' ')

# split by comma
# replace by _1, _2 etc
# handle if else, nested if else if possible