from pyparsing import *

identifier = Word(alphas + "_", alphanums + "_").setName("identifier")
as_keyword = Keyword("as", caseless=True).setName("AS")

schemaname = locatedExpr(identifier).setResultsName("schemaname")
tablename = locatedExpr(identifier).setResultsName("tablename")
alias = locatedExpr(identifier).setResultsName("alias")

full_qualified_table_name = schemaname + "." + tablename + \
    Optional(as_keyword) + Optional(alias)
unqualified_table_name = tablename + Optional(as_keyword) + alias
table_or_schemaname = \
    locatedExpr(identifier).setResultsName("table_or_schemaname")

schema_name_and_dot = schemaname + "." + Optional(as_keyword) + \
    Optional(alias)

nothing = Optional(White()).setResultsName('nothing') + (FollowedBy(",") | FollowedBy(StringEnd()))


from_element = Suppress(StringStart() | ",") + \
    (
        full_qualified_table_name |
        schema_name_and_dot.setResultsName("schemaname_and_dot") |
        unqualified_table_name |
        table_or_schemaname | nothing) + \
    (FollowedBy(",") | FollowedBy(StringEnd()))

parse = from_element.parseWithTabs()


def test(test_str):
    print(">>>", test_str)
    try:
        tokens = parse.scanString(test_str)
        for substring in tokens:
            from_element = substring[0]
            print(">>>>>", "'" + test_str[substring[1]:substring[2]] + "'")
            if from_element.tablename:
                print(
                    "Tablename:",
                    '"' + str(from_element.tablename[1]) + '"',
                    str(from_element.tablename[0]) + ":" +
                    str(from_element.tablename[2]))
            if from_element.table_or_schemaname:
                print(
                    "Table- or schemaname:",
                    '"' + str(from_element.table_or_schemaname[1]) + '"',
                    str(from_element.table_or_schemaname[0]) + ":" +
                    str(from_element.table_or_schemaname[2]))
            if from_element.alias:
                print(
                    "Alias:",
                    '"' + str(from_element.alias[1]) + '"',
                    str(from_element.alias[0]) + ":" +
                    str(from_element.alias[2]))
            if from_element.schemaname:
                print(
                    "Schemaname:",
                    '"' + str(from_element.schemaname[1]) + '"',
                    str(from_element.schemaname[0]) + ":" +
                    str(from_element.schemaname[2]))
            if from_element.schemaname_and_dot:
                print(
                    "Tablename (empty):",
                    str(from_element.schemaname[2] + 1) + ":" +
                    str(from_element.schemaname[2] + 1))
            if from_element.nothing or (len(from_element) == 0 and substring[1] != substring[2]):
                print(
                    "Table or schemaname (empty):",
                    '"' + str(from_element.nothing) + '"',
                    str(substring[1] + 1) + ":" + str(substring[2]))

    except ParseException as e:
        print(e)
    print()


test_strings = [
    "",
    "table1 as zo",
    "table1, table2",
    "table1,           , table2",
    " ,      ",
    "table, ",
    "table1,",
    "bla bla,bla",
    "mok."]

for test_str in test_strings:
    test(test_str)
