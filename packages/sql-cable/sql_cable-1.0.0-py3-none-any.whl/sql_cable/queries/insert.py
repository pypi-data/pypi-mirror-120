from .query_objects import InsertObject


class Insert:
    def __init__(self, session, table_name):
        self.session = session
        self.table_name = table_name

    def add(self, commit=False, **args):
        # making the query
        columns = ""
        value_str = ""
        params = []
        for arg in args:
            columns += arg + ', '
            value_str += '?, '
            params.append(args[arg])
        query = f"INSERT INTO {self.table_name} ({columns[:-2]}) VALUES ({value_str[:-2]})"
        if commit:
            self.session.add(InsertObject(query, params=params, commit=commit))
        else:
            return InsertObject(query, params=params, commit=commit)
