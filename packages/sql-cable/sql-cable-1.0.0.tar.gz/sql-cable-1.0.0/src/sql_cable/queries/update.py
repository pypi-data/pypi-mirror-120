from .query_objects import UpdateObject, FilterObject


class RunUpdate:
    def __init__(self, session, query, params, commit):
        self.session = session
        self.query = query
        self.params = params
        self.commit = commit

    def all(self):
        if self.commit:
            self.session.add(UpdateObject(self.query, params=self.params, commit=self.commit))
        else:
            return UpdateObject(self.query, params=self.params, commit=self.commit)

    def where(self, conjunctive_op='AND', comparison_op='=', **args):
        self.query += " WHERE "
        for param in args:
            # if the param is a FilterObject get the column name and value from that obj
            if isinstance(args[param], FilterObject):
                self.query += f"{args[param].column} {comparison_op} ? {conjunctive_op} "
                self.params.append(args[param].value)
            else:
                self.query += f"{param} {comparison_op} ? {conjunctive_op} "
                self.params.append(args[param])
        # taking off the extra spaces and conjunctive_op at the end
        self.query = self.query[:-(len(conjunctive_op) + 2)]
        if self.commit:
            self.session.add(UpdateObject(self.query, params=self.params, commit=self.commit))
        else:
            return UpdateObject(self.query, params=self.params, commit=self.commit)


class Update:
    def __init__(self, session, table_name):
        self.session = session
        self.table_name = table_name

    def set(self, commit=False, **args):
        set_str = ""
        params = []
        for arg in args:
            set_str += f"{arg} = ?, "
            params.append(args[arg])
        query = f"UPDATE {self.table_name} SET {set_str[:-2]}"
        return RunUpdate(self.session, query, params, commit)
