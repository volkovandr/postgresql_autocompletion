'''Implementation of an SQL parser used by the plugin'''


def parseSQL(query_text):
    if query_text is None or len(query_text) == 0:
        return None
