'''Implementation of an SQL parser used by the plugin'''

from postgresql_autocompletion_lib.pyparsing import *


def addToDict(dict_, token, key):
    if token:
        dict_[key] = (token[1], token[0] + 1, token[2] + 1)
    return dict_


def base_parse(query_text):
    '''Parses a given SQL query and returns a dictionary of the elements of it.
    Example: given query is SELECT a, b, c FROM table1 WHERE a>b
    Returned value is
    {
        "select": ("a, b, c", 8, 14),
        "from": ("table1", 21, 26),
        "where": ("a>b", 34, 36)
    } and so on: the contents of every block of a query it could find.
    Subqueries are returned as is.
    Returns None on empty string or None
    The expected structure of an SQL query is the following:
    [something] [SELECT <select block>] [FROM <from block>]
    [WHERE <where block>] [GROUP BY <group by block]
    [HAVING <having block>] [WINDOW <window block>]
    [ORDER BY <order by block>]
    [LIMIT <limit block>]
    [OFFSET <offset block>]
    Blocks are separated from each other by whitespace, newline or
    closing parethesis.
    Blocks' contents are separated from the keywords by whitespace, newline or
    opening parenthesis.
    Comments are ignored.
    '''
    if query_text is None or len(query_text) == 0:
        return None

    selectKeyword = Keyword("SELECT", caseless=True)
    fromKeyword = Keyword("FROM", caseless=True)
    separatorKeyword = selectKeyword | fromKeyword | StringEnd()

    selectBlock = selectKeyword + \
        locatedExpr(SkipTo(separatorKeyword)).setResultsName("selectList")
    fromBlock = fromKeyword + \
        locatedExpr(SkipTo(separatorKeyword)).setResultsName("fromList")

    query = selectBlock + Optional(fromBlock)

    tokens = query.parseString(query_text)
    ret = addToDict({}, tokens.selectList, "select")
    ret = addToDict(ret, tokens.fromList, "from")

    return ret
