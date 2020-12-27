class CursorByName():
    def __init__(self, cursor):
        self._cursor = cursor
    
    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.__next__()
        return { description[0]: row[col] for col, description in enumerate(self._cursor.description) }