# simpleSQL.py
#
# simple demo of using the parsing library to do simple-minded SQL parsing
# could be extended to include where clauses etc.
#
# Copyright (c) 2003, Paul McGuire
#
from pyparsing import CaselessLiteral, Word, upcaseTokens, \
    delimitedList, Optional, Combine, Group, alphas, nums, alphanums, \
    ParseException, Forward, oneOf, quotedString, ZeroOrMore, restOfLine,\
    Keyword, originalTextFor, locatedExpr

cp = 0
token_at = None

def test(str, cursor_position):
    global cp
    global token_at
    cp = cursor_position
    print(str, "->")
    try:
        tokens = simpleSQL.parseString(str)
        selectList = tokens.select[1]
        tables = tokens.from_[1]
        if tokens.where:
            where = tokens.where[1]
        print("tokens          =", tokens)
        print("Select list     =", selectList)
        print("Tables          =", tables)
        if where:
            print("Where condition =", where)
        if selectList[0] <= cursor_position <= selectList[2]:
            print("Cursor is in the Select list")
        elif tables[0] <= cursor_position <= tables[2]:
            print("Cursor is in the Tables")
        elif where:
            if where[0] <= cursor_position <= where[2]:
                print("Cursor is in the where clause")
    except ParseException as err:
        print(" " * err.loc + "^\n" + err.msg)
        print(err)

def parse_action1(s, loc, toks):
    if cp >= loc and cp <= loc + len(toks[0]):
        global token_at
        token_at = toks[0]
        print("We are here:", toks[0])



# define SQL tokens
selectStmt = Forward()
selectToken = Keyword("select", caseless=True)
fromToken = Keyword("from", caseless=True)

ident = Word(alphas, alphanums + "_$").setName("identifier")
columnName = (delimitedList(ident, ".", combine=True))
columnNameList = Group(delimitedList(columnName))
tableName = (delimitedList(ident, ".", combine=True))
tableNameList = Group(delimitedList(tableName))

whereExpression = Forward()
and_ = Keyword("and", caseless=True)
or_ = Keyword("or", caseless=True)
in_ = Keyword("in", caseless=True)

E = CaselessLiteral("E")
binop = oneOf("= != < > >= <= eq ne lt le gt ge", caseless=True)
arithSign = Word("+-", exact=1)
realNum = Combine(Optional(arithSign) +
                  (Word(nums) + "." + Optional(Word(nums)) |
                   ("." + Word(nums))) +
                  Optional(E + Optional(arithSign) + Word(nums)))
intNum = Combine(Optional(arithSign) + Word(nums) +
                 Optional(E + Optional("+") + Word(nums)))

# need to add support for alg expressions
columnRval = realNum | intNum | quotedString | columnName
whereCondition = Group(
    (columnName + binop + columnRval) |
    (columnName + in_ + "(" + delimitedList(columnRval) + ")") |
    (columnName + in_ + "(" + selectStmt + ")") |
    ("(" + whereExpression + ")")
)
whereExpression << whereCondition + ZeroOrMore((and_ | or_) + whereExpression)
whereExpression = locatedExpr(whereExpression)
# define the grammar
selectList = Group(selectToken + locatedExpr('*' | columnNameList)).setResultsName("select")
fromClause = Group(fromToken + locatedExpr(tableNameList)).setResultsName("from_")
whereClause = Group(CaselessLiteral("where") +
                   whereExpression).setResultsName("where")
selectStmt << ( selectList + fromClause + Optional(whereClause, ""))

simpleSQL = selectStmt

# define Oracle comment format, and ignore them
oracleSqlComment = "--" + restOfLine
simpleSQL.ignore(oracleSqlComment)


test("SELECT a, b, c from table1, table2       where mok = bok", 30)
#test("select * from SYS.XYZZY")
#test("Select A from Sys.dual")
#test("Select A,B,C from Sys.dual")
#test("Select A, B, C from Sys.dual")
#test("Select A, B, C from Sys.dual, Table2   ")
#test("Xelect A, B, C from Sys.dual")
#test("Select A, B, C frox Sys.dual")
# test("Select")
#test("Select &&& frox Sys.dual")
#test("Select A from Sys.dual where a in ('RED','GREEN','BLUE')")
# test("Select A from Sys.dual where a in ('RED','GREEN','BLUE')" +
#     " and b in (10,20,30)")
# test("Select A,b from table1,table2 where table1.id eq table2.id" +
#     " -- test out comparison operators")
#test("SELECT a FROM (SELECT b) a")
