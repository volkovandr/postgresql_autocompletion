'''Implementation of an SQL parser used by the plugin'''

from postgresql_autocompletion_lib.pyparsing import *


def addToDict(dict_, key, token):
    if token and token != '':
        dict_[key] = (token[1], token[0] + 1, token[2] + 1)


def cursorPositionInQuery(cursor_position, parse_results):
    '''Takes the result of base_parse. Returns the name of the query part
    where the cursor is, the text of this part,
    and the relative cursor position'''
    for query_part in parse_results:
        if parse_results[query_part][1] <= \
                cursor_position <= \
                parse_results[query_part][2]:
            return (
                query_part,
                parse_results[query_part][0],
                cursor_position - parse_results[query_part][1])


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

    ret = {}
    addToDict(ret, "select", tokens.selectList)
    addToDict(ret, "from", tokens.fromList)

    return ret

def parseFrom(from_clause_text):
    '''Parses the FROM clause.
    Example: given string is schema1.table1 as t1, schema2.table2 as t2, t3
    Returns list of dictionaries:
    [
        {
            "schema_name": ("schema1", 1, 7),
            "table_name": ("table1", 9, 14),
            "alias": ("t1", 19, 20)
        },
        {
            "schema_name": ("schema2", 23, 29),
            "table_name": ("table2", 31, 36),
            "alias": ("t2", 41, 42)
        },
        {
            "schema_or_table_name": ("t3", 45, 46)
        }
    ]
    Assuming the user is still typing a name of a schema or a name of a table,
    in the third element of the example it is not possible to tell whether
    it is a schema or table name, ergo "schema_or_table_name" is returned.
    '''
    ret = []
    if from_clause_text is None or from_clause_text == '':
        return ret

    identifier = Word(alphas, alphanums).setName("identifier")
    as_keyword = Keyword("as", caseless=True).setName("AS")

    schemaname = locatedExpr(identifier).setResultsName("schemaname")
    tablename = locatedExpr(identifier).setResultsName("tablename")
    table_or_schemaname = \
        locatedExpr(identifier).setResultsName("table_or_schemaname")
    alias = locatedExpr(identifier).setResultsName("alias")

    full_qualified_table_name = schemaname + "." + tablename + \
        Optional(as_keyword) + Optional(alias)
    unqualified_table_name = tablename + Optional(as_keyword) + alias

    from_element = Suppress(StringStart() | ",") + \
        (
            full_qualified_table_name |
            unqualified_table_name |
            table_or_schemaname) + \
        (FollowedBy(",") | FollowedBy(StringEnd()))

    for parsed_from_element in from_element.scanString(from_clause_text):
        tokens = parsed_from_element[0]
        parse_result = {}
        addToDict(parse_result, "schema_name", tokens.schemaname)
        addToDict(parse_result, "table_name", tokens.tablename)
        addToDict(parse_result, "alias", tokens.alias)
        addToDict(parse_result, "schema_or_table_name",
                  tokens.table_or_schemaname)
        ret.append(parse_result)

    return ret

