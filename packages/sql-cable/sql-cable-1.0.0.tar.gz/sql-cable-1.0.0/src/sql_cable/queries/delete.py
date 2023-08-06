from .query_objects import DeleteObject, FilterObject


class RunDelete:
    def __init__(self, session, query, commit):
        self.session = session
        self.query = query
        self.commit = commit

    def all(self):
        if self.commit:
            self.session.add(DeleteObject(self.query, commit=self.commit))
        else:
            return DeleteObject(self.query, commit=self.commit)

    def where(self, conjunctive_op='AND', comparison_op='=', **args):
        self.query += " WHERE "
        self.params = []
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
            self.session.add(DeleteObject(self.query, params=self.params, commit=self.commit))
        else:
            return DeleteObject(self.query, params=self.params, commit=self.commit)


class Delete:
    def __init__(self, session, table_name):
        self.session = session
        self.table_name = table_name

    def remove(self, commit=False):
        query = f"DELETE FROM {self.table_name}"
        return RunDelete(self.session, query, commit)
