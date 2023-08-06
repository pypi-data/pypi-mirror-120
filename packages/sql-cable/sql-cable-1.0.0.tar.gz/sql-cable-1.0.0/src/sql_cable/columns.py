class None_:
    def __init__(self):
        self.sql = "NONE"


class Set_Null:
    def __init__(self):
        self.sql = "SET NULL"


class Set_Default:
    def __init__(self):
        self.sql = "SET DEFAULT"


class Cascade:
    def __init__(self):
        self.sql = "CASCADE"


class Restrict:
    def __init__(self):
        self.sql = "RESTRICT"


class Simple:
    def __init__(self):
        self.sql = "SIMPLE"


class Full:
    def __init__(self):
        self.sql = "FULL"


class Partial:
    def __init__(self):
        self.sql = "PARTIAL"


def type_to_sql_type(type):
    if type == float:
        sql_type = "REAL"
    elif type == int:
        sql_type = "INTEGER"
    elif type == str:
        sql_type = "STRING"
    elif type == bool:
        sql_type = "BOOLEAN"
    return sql_type


def sql_args(column):
    args_str = ""
    if column.unique:
        args_str += " UNIQUE"
    if column.not_null:
        args_str += " NOT NULL"
    if column.default:
        if type(column.default) == str:
            args_str += f" DEFAULT [{column.default}]"
        else:
            args_str += f" DEFAULT {column.default}"
    return args_str


def lenght_sql(column):
    lenght_str = ""
    if column.max_length and not column.min_length:
        lenght_str += f" ({column.max_length})"
    if column.min_length and column.min_length:
        lenght_str += f"({column.min_length}, {column.max_length})"
    return lenght_str


# default column that all others use
class Column:
    def __init__(self, pk=False, foreign_model=None, on_delete=None, on_update=None, match=None, unique=False, not_null=False, default=None, max_length=None, min_length=None):
        self.name = None
        self.pk = pk
        self.fk = True if foreign_model else False
        self.foreign_model = foreign_model
        self.on_delete = on_delete
        self.on_update = on_update
        self.match = match
        self.unique = unique
        self.not_null = not_null
        self.default = default
        self.max_length = max_length
        self.min_length = min_length
        self.type = type_to_sql_type(self.python_type) + lenght_sql(self)

    def generate_sql(self):
        return f"[{self.name}] {self.type}{sql_args(self)}"


class PrimaryKeyColumn(Column):
    def __init__(self, type=int):
        self.python_type = type
        super().__init__(pk=True)

    def generate_sql(self):
        return f"[{self.name}] {self.type} PRIMARY KEY AUTOINCREMENT"


class ForeignKeyColumn(Column):
    def __init__(self, foreign_model, on_delete=Cascade(), on_update=None_(), match=None_(), unique=False, not_null=False, default=None, max_length=None, min_length=None):
        self.python_type = int
        super().__init__(foreign_model=foreign_model, on_delete=on_delete, on_update=on_update, match=match, unique=unique, not_null=not_null, default=default, max_length=max_length, min_length=min_length)
        self.foreign_model_in = self.foreign_model()
        self.type = type_to_sql_type(self.foreign_model_in.primary_key.python_type) + lenght_sql(self)

    def generate_sql(self):
        return f"[{self.name}] {self.type}{sql_args(self)} REFERENCES {self.foreign_model_in.model_name} ({self.foreign_model_in.primary_key.name})  ON DELETE {self.on_delete.sql}"


class StringColumn(Column):
    def __init__(self, unique=False, not_null=False, default=None, max_length=None, min_length=None):
        self.python_type = str
        super().__init__(unique=unique,  not_null=not_null, default=default, max_length=max_length, min_length=min_length)


class IntegerColumn(Column):
    def __init__(self, unique=False, not_null=False, default=None, max_length=None, min_length=None):
        self.python_type = int
        super().__init__(unique=unique,  not_null=not_null, default=default, max_length=max_length, min_length=min_length)


class FloatColumn(Column):
    def __init__(self, unique=False, not_null=False, default=None, max_length=None, min_length=None):
        self.python_type = float
        super().__init__(unique=unique,  not_null=not_null, default=default, max_length=max_length, min_length=min_length)


class BooleanColumn(Column):
    def __init__(self, unique=False, not_null=False, default=None, max_length=None, min_length=None):
        self.python_type = bool
        super().__init__(unique=unique,  not_null=not_null, default=default, max_length=max_length, min_length=min_length)
