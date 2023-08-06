from .query_objects import SelectObject, FilterObject
import math


class ForeignRowObject:
    def __init__(self, session, foreign_model, tuple_rows, value):
        self.session = session
        self.tuple_rows = tuple_rows
        self.foreign_model = foreign_model
        self.columns_unsorted = self.foreign_model.columns
        self.value = value
        self.get_columns()
        self.rows_to_rowobjects()

    def rows_to_rowobjects(self):
        self.rows = []
        for row in self.tuple_rows:
            self.rows.append(RowObject(self.session, row, self.columns))

    def get_columns(self):
        table_data = self.session.select(selectobj=SelectObject(f"PRAGMA table_info({self.foreign_model.model_name});", fetch_mode='all'))
        self.columns = {}
        for column in table_data:
            for col in self.columns_unsorted:
                if self.columns_unsorted[col].name == column[1]:
                    self.columns[column[1]] = self.columns_unsorted[col]


class RowObject:
    def __init__(self, session, row_data, columns):
        self.session = session
        self.row_data = row_data
        self.columns = columns
        self.row_to_var()

    def row_to_var(self):
        for i in range(len(self.columns)):
            # if the column is a foreign key
            if self.columns[list(self.columns.keys())[i]].fk:
                foreign_model = self.columns[list(self.columns.keys())[i]].foreign_model_in
                foreign_pk = foreign_model.primary_key.name
                _locals = locals()
                # get the row that the foreign key links to
                foreign_data = self.session.select(SelectObject(f"SELECT * FROM {foreign_model.model_name} WHERE {foreign_pk} = ?", params=[self.row_data[i]], fetch_mode='all'))
                exec(f"self.{list(self.columns.keys())[i]} = value", {'self': self, 'value': ForeignRowObject(self.session, foreign_model, foreign_data, self.row_data[i])})
            # if the column is a boolean column change the value from a int to a bool
            elif self.columns[list(self.columns.keys())[i]].python_type == bool:
                exec(f"self.{list(self.columns.keys())[i]} = value", {'self': self, 'value': bool(self.row_data[i])})

            else:
                exec(f"self.{list(self.columns.keys())[i]} = value", {'self': self, 'value': self.row_data[i]})


class PaginationPage:
    def __init__(self, session, table_name, columns, query, params, per_page, page_num):
        self.session = session
        self.table_name = table_name
        self.columns = columns
        self.query = query
        self.params = params
        self.per_page = per_page
        self.page_num = page_num
        self.get_all_data()
        self.get_items()

    def get_all_data(self):
        # work out how many posible pages there are
        result = self.session.select(self.session, SelectObject(self.query, params=self.params, fetch_mode='all'))
        self.page_amount = math.ceil(len(result) / self.per_page)

    def get_items(self):
        # get the page data
        start = self.per_page * (self.page_num - 1)
        self.query = self.query + " LIMIT ? OFFSET ?"
        self.params.append(self.per_page)
        self.params.append(start)
        items = self.session.select(self.session, SelectObject(self.query, params=self.params, fetch_mode='all'))
        f_result = []
        if items != []:
            for row in items:
                f_result.append(RowObject(self.session, row, self.columns))
            self.items = f_result

    # button stuff
    def iter_page(self, first, last, left, right):
        self.page_nums = []
        self.page_nums.append(1)
        for i in range(left):
            if self.page_num - (i + 1) > 1:
                self.page_nums.append(self.page_num - (i + 1))
        if self.page_num != 1 and self.page_num != self.page_amount:
            self.page_nums.append(self.page_num)
        for i in range(right):
            if self.page_num + (i + 1) < self.page_amount:
                self.page_nums.append(self.page_num + (i + 1))
        if self.page_amount != 1:
            self.page_nums.append(self.page_amount)
        return self.page_nums


class FinalFunctions:
    def __init__(self, session, table_name, columns, query, params):
        self.session = session
        self.table_name = table_name
        self.columns = columns
        self.query = query
        self.params = params

    def all(self):
        result = self.session.select(SelectObject(self.query, params=self.params, fetch_mode='all'))
        if result:
            final_result = []
            for row in result:
                final_result.append(RowObject(self.session, row, self.columns))
            return final_result
        else:
            return []

    def one(self):
        result = self.session.select(SelectObject(self.query, params=self.params, fetch_mode='one'))
        if result:
            return RowObject(self.session, result, self.columns)
        else:
            # returning a RowObject with all values set to None
            none_result = []
            for column in self.columns:
                none_result.append(None)
            return RowObject(self.session, tuple(none_result), self.columns)

    def paginate(self, per_page, page_num):
        return PaginationPage(self.table_name, self.columns, self.query, self.params, per_page, page_num)


class SortBy(FinalFunctions):
    def sortby(self, **args):
        # used the function is being run from the sortby function in Select
        if 'pre_data' in list(args.keys()):
            args = args['pre_data']
        # adding to the query
        self.query += ' ORDER BY '
        for arg in args:
            self.query += f"{arg} {args[arg]}, "
        # taking off extra comma and space
        self.query = self.query[:-2]
        return FinalFunctions(self.session, self.table_name, self.columns, self.query, self.params)


class Filter(FinalFunctions):
    def filter(self, conjunctive_op='AND', comparison_op='=', **args):
        if 'pre_data' in list(args.keys()):
            # used the function is being run from the filter function in Select
            args = args['pre_data']
            # checking if a conjunctive_op was passed from the filter function in Select
            if 'conjunctive_op' in list(args.keys()):
                conjunctive_op = args['conjunctive_op']
                del args['conjunctive_op']
            if 'comparison_op' in list(args.keys()):
                comparison_op = args['comparison_op']
                del args['comparison_op']
        # adding to the query
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
        return SortBy(self.session, self.table_name, self.columns, self.query, self.params)


class Select(FinalFunctions):
    def __init__(self, session, table_name, columns):
        self.session = session
        self.table_name = table_name
        self.columns_unsorted = columns
        self.get_columns()
        self.query = f"SELECT * FROM {self.table_name}"
        self.params = []

    def get_columns(self):
        table_data = self.session.select(selectobj=SelectObject(f"PRAGMA table_info({self.table_name});", fetch_mode='all'))
        self.columns = {}
        for column in table_data:
            for col in self.columns_unsorted:
                if self.columns_unsorted[col].name == column[1]:
                    self.columns[column[1]] = self.columns_unsorted[col]

    def sortby(self, **kwargs):
        return SortBy(self.session, self.table_name, self.columns, self.query, self.params).sortby(pre_data=kwargs)

    def filter(self, **kwargs):
        return Filter(self.session, self.table_name, self.columns, self.query, self.params).filter(pre_data=kwargs)
