import re

def toUUID(query:str):
    """
    Convert a standard name (author/topic) to a formatted UUID.

    Args:
        query (str): The query to convert.

    Returns:
        str: The formatted version (UUID).

    Raises:
        ValueError: Not specifing a query triggers this error.

    Example:
        Converting the name H. Jackson Brown, Jr. to an UUID.

        >>> print(toUUID('H. Jackson Brown, Jr.'))
        h-jackson-brown-jr
    """
    if(not query):
        raise ValueError('Specify a query bud.')
    return re.sub('(^-|-$)','',re.sub('--','-',re.sub('[^a-z]','-',query.lower())))
