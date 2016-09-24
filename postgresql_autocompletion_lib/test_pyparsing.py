# simpleSQL.py
#
# simple demo of using the parsing library to do simple-minded SQL parsing
# could be extended to include where clauses etc.
#
# Copyright (c) 2003, Paul McGuire
#
from pyparsing import *


identifier = Word(alphas, alphanums).setName("identifier")
as_keyword = Keyword("as", caseless=True).setName("AS")

schemaname = locatedExpr(identifier).setResultsName("schemaname")
tablename = locatedExpr(identifier).setResultsName("tablename")
table_or_schemaname = locatedExpr(identifier).setResultsName("table_or_schemaname")
alias = locatedExpr(identifier).setResultsName("alias")

full_qualified_table_name = schemaname + "." + tablename + \
    Optional(as_keyword) + Optional(alias)
unqualified_table_name = tablename + Optional(as_keyword) + alias

from_element = Suppress(StringStart() | ",") + (full_qualified_table_name | unqualified_table_name | table_or_schemaname) + (FollowedBy(",") | FollowedBy(StringEnd()))

parse = from_element.parseWithTabs()

def test(test_str):
    print(">>>", test_str)
    try:
        tokens = parse.scanString(test_str)
        #print(tokens)
        for substring in tokens:
            from_element = substring[0]
            print(">>>>>", test_str[substring[1]:substring[2]])
            if from_element.schemaname != '':
                print("schemaname:", from_element.schemaname)
            if from_element.tablename != '':
                print("tablename :", from_element.tablename)
            if from_element.table_or_schemaname != '':
                print("t_or_sch  :", from_element.table_or_schemaname)
            if from_element.alias != '':
                print("alias     :", from_element.alias)
    except ParseException as e:
        print(e)
    print()


test_strings = [
    "",
    "table1",
    "table1 as t1",
    "table1 t1",
    "schema1.table1 as t1",
    "schema1.table1 t1",
    "schema1.table1",
    "table1, table2",
    "table1 as t1, table2 as t2",
    "table1, schema2.table2 t2",
    "schema1.table1 t1, schema2.table2 as t2",
    "s1.t1, s2.t2, s3.t3, s4.t4",
    "bla1 bla2 bla3 bla4",
    '''schema1.table1
    as zorro  ,
    schema2.table2
    mumba''',
    "bla.bla, zok.mok, a b c, kum.zum"]

for test_str in test_strings:
    test(test_str)
