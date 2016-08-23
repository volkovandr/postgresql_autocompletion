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
    Keyword, originalTextFor


def test(str):
    print(str, "->")
    try:
        tokens = simpleSQL.parseString(str)
        print("tokens          =", tokens)
        print("Select clause   =", tokens.select)
        print("Select list     =", tokens.select[1])
        print("From clause     =", tokens.from_)
        print("Tables          =", tokens.from_[1])
        print("Where clause    =", tokens.where)
        print("Where condition =", tokens.where)
    except ParseException as err:
        print(" " * err.loc + "^\n" + err.msg)
        print(err)
    print

def parse_action_test(s, loc, toks):
    print("s", s)
    print("loc", loc)
    print("toks", toks)

# define SQL tokens
selectStmt = Forward()
selectToken = Keyword("select", caseless=True)
fromToken = Keyword("from", caseless=True)

ident = Word(alphas, alphanums + "_$").setName("identifier")
columnName = (delimitedList(ident, ".", combine=True))
columnNameList = Group(delimitedList(columnName))
tableName = (delimitedList(ident, ".", combine=True))
tableNameList = Group(delimitedList(tableName)). \
    setParseAction(parse_action_test)

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

# define the grammar
selectStmt << (
    Group(selectToken + ('*' | columnNameList)).setResultsName("select") +
    Group(fromToken + tableNameList).setResultsName("from_") +
    Optional(Group(CaselessLiteral("where") +
                   whereExpression), "").setResultsName("where"))

simpleSQL = selectStmt

# define Oracle comment format, and ignore them
oracleSqlComment = "--" + restOfLine
simpleSQL.ignore(oracleSqlComment)


test("SELECT a, b, c from table1, table2 WHERE a = b")
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
