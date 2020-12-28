class CursorByName():
    """
    This class is used to convert results from database into
    key-value pairs where key is the column name and value is
    the column value for every row fetched by the cursor
    """
    def __init__(self, cursor):
        self._cursor = cursor
    
    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.__next__()
        return { description[0]: row[col] for col, description in enumerate(self._cursor.description) }