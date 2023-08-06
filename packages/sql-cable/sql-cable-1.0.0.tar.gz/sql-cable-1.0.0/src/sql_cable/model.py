from .columns import (PrimaryKeyColumn, ForeignKeyColumn,
                      StringColumn, IntegerColumn,
                      FloatColumn, BooleanColumn)
from .queries import SelectObject, Select, Insert, Update, Delete


class Model:
    def __init__(self):
        # setting the name that will be used as the table name
        # example str(self) = "<__main__.Test object at 0x000001D9BC34C448>"
        if isinstance(self, Model):
            self.model_name = str(self).split('.')[-1].split(' object ')[0].lower()
            self.get_columns()
        else:
            self.model_name = str(self).split('.')[-1].replace("'>", '').lower()
            self.get_columns(self)

    # get all columns into a dict and assign columns names
    def get_columns(self):
        self.columns = {}
        for var in dir(self):
            # making sure the var is not a magic method
            if '__' not in var:
                class_in = getattr(self, var)
                # checking it is a column
                if isinstance(class_in, (PrimaryKeyColumn, ForeignKeyColumn, IntegerColumn, StringColumn, FloatColumn, BooleanColumn)):
                    self.columns[var] = class_in
                    self.columns[var].name = var
                    if isinstance(class_in, PrimaryKeyColumn):
                        self.primary_key = self.columns[var]

    def check_for_changes(self):
        changes = []

        # checking if the table exists
        table_data = self.session.select(SelectObject("SELECT name FROM sqlite_master WHERE type ='table' AND name = ?;", params=[self.model_name], fetch_mode='one'))
        if table_data:
            # checking that all the columns in the model exist
            """
            table_info keys:
            index : value : type
            0 : cid: int
            1 : name: str
            2 : type: str
            3 : not_null : int/bool
            4 : default : what ever the value of the default was
            5 : primary_key : int/bool
            """
            table_info = self.session.select(SelectObject(f"PRAGMA table_info({self.model_name});", fetch_mode='all'))
            column_name = []
            # checking each column for changes
            for column in self.columns:
                column = self.columns[column]
                column_table_info = None
                for column_ in table_info:
                    if column_[1] == column.name:
                        column_table_info = column_
                if column_table_info:
                    # type check
                    if column.type != column_table_info[2]:
                        changes.append(f'{column.name} is meant to have a type of {column.type} not {column_table_info[2]}')
                    # primary key check
                    if column.pk != bool(column_table_info[5]):
                        if column.pk:
                            changes.append(f'{column.name} is meant to be a primary key')
                        if not column.pk:
                            changes.append(f'{column.name} is not meant to be a primary key')
                    # not null check
                    if column.not_null != bool(column_table_info[3]):
                        if column.not_null:
                            changes.append(f'{column.name} is meant have not_null')
                        else:
                            changes.append(f'{column.name} is not meant to have not_null')
                    # default check
                    if column.default != column_table_info[4]:
                        changes.append(f"{column.name}'s default value is meant to be [{column.default}] not {column_table_info[4]}")
                    # unique check
                    """
                    index_list keys:
                    index : value : type
                    0 : seq : int
                    1 : name : str
                    2 : unique : int/bool
                    3 : origin : str?
                    4 : partial : int/bool
                    """
                    index_list = self.session.select(SelectObject(f'PRAGMA index_list({self.model_name});', fetch_mode='all'))
                    unique = False
                    for index in index_list:
                        """
                        index_info keys:
                        index : value : type
                        0 : seqno : int
                        1 : cid : int
                        2 : name : str
                        """
                        index_info = self.session.select(SelectObject(f'PRAGMA index_info({index[1]});', fetch_mode='one'))
                        if column.name == index_info[2]:
                            unique = True
                    if column.unique and not unique:
                        changes.append(f"{column.name} is meant to be unique")
                    elif not column.unique and unique:
                        changes.append(f"{column.name} is not meant to be unique")
                    # foreign key check
                    """
                    pragma_foreign_key_list keys:
                    index : value : type
                    0 : id : int
                    1 : seq : int
                    2 : table : str
                    3 : from : str
                    4 : to : str
                    5 : on_update : str
                    6 : on_delete : str
                    7 : match : str
                    """
                    foreign_key_list = self.session.select(SelectObject(f"SELECT * FROM pragma_foreign_key_list('{self.model_name}');", fetch_mode='all'))
                    is_foreign_key = False
                    for foreign_key in foreign_key_list:
                        if column.name == foreign_key[3]:
                            is_foreign_key = True
                            foreign_key_info = foreign_key
                    if column.fk and not is_foreign_key:
                        changes.append(f"{column.name} is meant to be foreign key")
                    elif not column.fk and is_foreign_key:
                        changes.append(f"{column.name} is not meant to be foreign key")
                    if is_foreign_key:
                        # foreign table check
                        if column.foreign_model.model_name != foreign_key_info[2]:
                            changes.append(f"{column.name}'s foreign_model is meant to be {column.foreign_model.model_name} but is {foreign_key_info[2]}")
                        # foreign column check
                        if column.foreign_model.primary_key.name != foreign_key_info[4]:
                            changes.append(f"{column.name}'s foreign column is meant to be {column.foreign_model.primary_key.name} but is {foreign_key_info[4]}")
                        # on delete check
                        if column.on_delete.sql != foreign_key_info[6]:
                            changes.append(f"{column.name}'s on_delete is meant to be {column.on_delete.sql} but is {foreign_key_info[6]}")
                        # on update check
                        if column.on_update.sql != foreign_key_info[5]:
                            changes.append(f"{column.name}'s on_update is meant to be {column.on_update.sql} but is {foreign_key_info[5]}")
                        # match check
                        if column.match.sql != foreign_key_info[7]:
                            changes.append(f"{column.name}'s match is meant to be {column.match.sql} but is {foreign_key_info[7]}")
                else:
                    changes.append(f'{column.name} does not exist')
        else:
            changes.append(f"{self.model_name} table does not exist")
        return changes

    def generate_migrations(self, changes):
        table_creation_str = f"CREATE TABLE {self.model_name} ({self.columns[self.primary_key.name].generate_sql()}, "
        for column in self.columns:
            if self.columns[column].pk is False:
                table_creation_str += self.columns[column].generate_sql() + ", "
        table_creation_str = table_creation_str[:-2] + ')'
        if f"{self.model_name} table does not exist" in changes:
            action = 'CREATE'
        else:
            action = 'UPDATE'
        migrations_file_str = f"""\n\n
class {self.model_name}(Migration):
    def __init__(self):
        self.table_name = '{self.model_name}'
        self.table_creation_str = '{table_creation_str}'
        self.changes = {changes}
        self.columns = {list(self.columns.keys())}
        self.action = '{action}'"""
        return migrations_file_str

    def load_queries(self):
        self.select = Select(self.session, self.model_name, self.columns)
        self.insert = Insert(self.session, self.model_name).add
        self.update = Update(self.session, self.model_name).set
        self.delete = Delete(self.session, self.model_name).remove
