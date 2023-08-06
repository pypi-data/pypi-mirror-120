# all the objects used with the db session

class SelectObject:
    def __init__(self, query, params=None, fetch_mode='all'):
        self.type = 'SELECT'
        self.query = query
        self.params = params
        self.fetch_mode = fetch_mode

    def execute(self, cursor):
        if self.params:
            cursor.execute(self.query, tuple(self.params))
        else:
            cursor.execute(self.query)

        if self.fetch_mode == 'one':
            data = cursor.fetchone()
        else:
            data = cursor.fetchall()
        return data


# used for example where or querys to prevent the same key word error if you want to do something like
# username='test1' or username='test2' you would do
# username1=FilterObject('username', 'test1') or username2=FilterObject('username', 'test2')
class FilterObject:
    def __init__(self, **args):
        self.args_to_column_and_value(args)

    def args_to_column_and_value(self, args):
        for arg in args:
            self.column = arg
            self.value = args[arg]


class InsertObject:
    def __init__(self, query, params=None, commit=False):
        self.type = 'INSERT'
        self.query = query
        self.params = params
        self.commit = commit

    def execute(self, conn, cursor):
        if self.params:
            cursor.execute(self.query, tuple(self.params))
        else:
            cursor.execute(self.query)
        if self.commit:
            conn.commit()


class UpdateObject:
    def __init__(self, query, params=None, commit=False):
        self.type = 'UPDATE'
        self.query = query
        self.params = params
        self.commit = commit

    def execute(self, conn, cursor):
        if self.params:
            cursor.execute(self.query, tuple(self.params))
        else:
            cursor.execute(self.query)
        if self.commit:
            conn.commit()


class DeleteObject:
    def __init__(self, query, params=None, commit=False):
        self.type = 'DELETE'
        self.query = query
        self.params = params
        self.commit = commit

    def execute(self, conn, cursor):
        if self.params:
            cursor.execute(self.query, tuple(self.params))
        else:
            cursor.execute(self.query)
        if self.commit:
            conn.commit()
