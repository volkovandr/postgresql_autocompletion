'''Implementation of an SQL parser used by the plugin'''


def parseSQL(query_text):
    '''Parses a given SQL query and returns a dictionary of the elements of it.
    Example: given query is SELECT a, b, c FROM table1 WHERE a>b
    Returned value is
    {
        "select": ("a, b, c", 8, 14),
        "from": ("table1", 21, 26),
        "where": ("a>b", 34, 36)
    }
    '''
    if query_text is None or len(query_text) == 0:
        return None

