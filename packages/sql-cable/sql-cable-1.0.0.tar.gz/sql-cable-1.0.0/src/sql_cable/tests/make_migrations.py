from .. import DB, Model
from ..columns import (PrimaryKeyColumn, ForeignKeyColumn,
                       StringColumn, IntegerColumn,
                       FloatColumn, BooleanColumn)
from .req import get_test_str, get_default_value
import os
import shutil
import sqlite3


single_model_make_migrations = {
    StringColumn: '''
from sql_cable.migrations import Migration


class test(Migration):
    def __init__(self):
        self.table_name = 'test'
        self.table_creation_str = 'CREATE TABLE test ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [c] STRING, [cd] STRING DEFAULT [test-string], [cdl] STRING(3, 16) DEFAULT [test-string], [cl] STRING(3, 16), [cn] STRING NOT NULL, [cnd] STRING NOT NULL DEFAULT [test-string], [cnl] STRING(3, 16) NOT NULL, [cu] STRING UNIQUE, [cud] STRING UNIQUE DEFAULT [test-string], [cul] STRING(3, 16) UNIQUE, [cun] STRING UNIQUE NOT NULL, [cundl] STRING(3, 16) UNIQUE NOT NULL DEFAULT [test-string])'
        self.changes = ['test table does not exist']
        self.columns = ['c', 'cd', 'cdl', 'cl', 'cn', 'cnd', 'cnl', 'cu', 'cud', 'cul', 'cun', 'cundl', 'id']
        self.action = 'CREATE'


models = [test()]''',
    IntegerColumn: '''
from sql_cable.migrations import Migration


class test(Migration):
    def __init__(self):
        self.table_name = 'test'
        self.table_creation_str = 'CREATE TABLE test ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [c] INTEGER, [cd] INTEGER DEFAULT 1234567890, [cdl] INTEGER(3, 16) DEFAULT 1234567890, [cl] INTEGER(3, 16), [cn] INTEGER NOT NULL, [cnd] INTEGER NOT NULL DEFAULT 1234567890, [cnl] INTEGER(3, 16) NOT NULL, [cu] INTEGER UNIQUE, [cud] INTEGER UNIQUE DEFAULT 1234567890, [cul] INTEGER(3, 16) UNIQUE, [cun] INTEGER UNIQUE NOT NULL, [cundl] INTEGER(3, 16) UNIQUE NOT NULL DEFAULT 1234567890)'
        self.changes = ['test table does not exist']
        self.columns = ['c', 'cd', 'cdl', 'cl', 'cn', 'cnd', 'cnl', 'cu', 'cud', 'cul', 'cun', 'cundl', 'id']
        self.action = 'CREATE'


models = [test()]''',
    FloatColumn: '''
from sql_cable.migrations import Migration


class test(Migration):
    def __init__(self):
        self.table_name = 'test'
        self.table_creation_str = 'CREATE TABLE test ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [c] REAL, [cd] REAL DEFAULT 100.001, [cdl] REAL(3, 16) DEFAULT 100.001, [cl] REAL(3, 16), [cn] REAL NOT NULL, [cnd] REAL NOT NULL DEFAULT 100.001, [cnl] REAL(3, 16) NOT NULL, [cu] REAL UNIQUE, [cud] REAL UNIQUE DEFAULT 100.001, [cul] REAL(3, 16) UNIQUE, [cun] REAL UNIQUE NOT NULL, [cundl] REAL(3, 16) UNIQUE NOT NULL DEFAULT 100.001)'
        self.changes = ['test table does not exist']
        self.columns = ['c', 'cd', 'cdl', 'cl', 'cn', 'cnd', 'cnl', 'cu', 'cud', 'cul', 'cun', 'cundl', 'id']
        self.action = 'CREATE'


models = [test()]''',
    BooleanColumn: '''
from sql_cable.migrations import Migration


class test(Migration):
    def __init__(self):
        self.table_name = 'test'
        self.table_creation_str = 'CREATE TABLE test ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [c] BOOLEAN, [cd] BOOLEAN, [cdl] BOOLEAN(3, 16), [cl] BOOLEAN(3, 16), [cn] BOOLEAN NOT NULL, [cnd] BOOLEAN NOT NULL, [cnl] BOOLEAN(3, 16) NOT NULL, [cu] BOOLEAN UNIQUE, [cud] BOOLEAN UNIQUE, [cul] BOOLEAN(3, 16) UNIQUE, [cun] BOOLEAN UNIQUE NOT NULL, [cundl] BOOLEAN(3, 16) UNIQUE NOT NULL)'
        self.changes = ['test table does not exist']
        self.columns = ['c', 'cd', 'cdl', 'cl', 'cn', 'cnd', 'cnl', 'cu', 'cud', 'cul', 'cun', 'cundl', 'id']
        self.action = 'CREATE'


models = [test()]'''
}


class SingleModelMakeMigrations:
    def __init__(self, app, column_type):
        self.app = app
        self.column_type = column_type
        self.test_name = f'''SingleModelMakeMigrations_{str(self.column_type).split("<class 'sql_cable.columns.")[1].split("'>")[0]}'''

    def run(self):
        if os.path.isdir('migrations'):
            shutil.rmtree('migrations')
        if os.path.isfile(self.app.config['DB_PATH']):
            os.remove(self.app.config['DB_PATH'])
        self.db = DB(self.app)

        class Test(Model):
            id = PrimaryKeyColumn()
            c = self.column_type()
            cu = self.column_type(unique=True)
            cn = self.column_type(not_null=True)
            cd = self.column_type(default=get_default_value(self.column_type))
            cl = self.column_type(min_length=3, max_length=16)

            cun = self.column_type(unique=True, not_null=True)
            cud = self.column_type(unique=True, default=get_default_value(self.column_type))
            cul = self.column_type(unique=True, min_length=3, max_length=16)
            cnd = self.column_type(not_null=True, default=get_default_value(self.column_type))
            cnl = self.column_type(not_null=True, min_length=3, max_length=16)
            cdl = self.column_type(default=get_default_value(self.column_type), min_length=3, max_length=16)

            cundl = self.column_type(unique=True, not_null=True,
                                     default=get_default_value(self.column_type),
                                     min_length=3, max_length=16)
        self.db.register_model(Test)
        path = self.db.make_migrations(test=True)
        self.db.session.stop()

        with open(path, 'r') as f:
            migrations_file_data = f.read()
        migrations_file_data = migrations_file_data.replace(migrations_file_data.split('\n')[0], '')
        if migrations_file_data == single_model_make_migrations[self.column_type]:
            return True
        # print(migrations_file_data)
        return False


double_model_make_migrations_correct = '''
from sql_cable.migrations import Migration


class test1(Migration):
    def __init__(self):
        self.table_name = 'test1'
        self.table_creation_str = 'CREATE TABLE test1 ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [name] STRING)'
        self.changes = ['test1 table does not exist']
        self.columns = ['id', 'name']
        self.action = 'CREATE'


class test2(Migration):
    def __init__(self):
        self.table_name = 'test2'
        self.table_creation_str = 'CREATE TABLE test2 ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [test_1_id] INTEGER REFERENCES test1 (id)  ON DELETE CASCADE)'
        self.changes = ['test2 table does not exist']
        self.columns = ['id', 'test_1_id']
        self.action = 'CREATE'


models = [test1(), test2()]'''


class DoubleModelMakeMigrations:
    def __init__(self, app):
        self.test_name = 'DoubleModelMakeMigrations'
        self.app = app

    def run(self):
        if os.path.isdir('migrations'):
            shutil.rmtree('migrations')
        if os.path.isfile(self.app.config['DB_PATH']):
            os.remove(self.app.config['DB_PATH'])
        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            name = StringColumn()

        class Test2(Model):
            id = PrimaryKeyColumn()
            test_1_id = ForeignKeyColumn(Test1)

        self.db.register_model(Test1)
        self.db.register_model(Test2)

        path = self.db.make_migrations(test=True)
        self.db.session.stop()
        with open(path, 'r') as f:
            migrations_file_data = f.read()
        migrations_file_data = migrations_file_data.replace(migrations_file_data.split('\n')[0], '')
        if migrations_file_data == double_model_make_migrations_correct:
            return True
        return False


single_model_update_make_migrations_correct = '''
from sql_cable.migrations import Migration


class test1(Migration):
    def __init__(self):
        self.table_name = 'test1'
        self.table_creation_str = 'CREATE TABLE test1 ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [cd] STRING DEFAULT [correct value], [name] STRING NOT NULL, [password] STRING(3, 16), [unique] STRING UNIQUE)'
        self.changes = ["cd's default value is meant to be [correct value] not notcorrect", 'name is meant have not_null', 'password is meant to have a type of STRING(3, 16) not STRING (1, 8)']
        self.columns = ['cd', 'id', 'name', 'password', 'unique']
        self.action = 'UPDATE'


models = [test1()]'''


class SingleModelUpdateMakeMigrations:
    def __init__(self, app):
        self.test_name = 'SingleModelUpdateMakeMigrations'
        self.app = app

    def run(self):
        if os.path.isdir('migrations'):
            shutil.rmtree('migrations')
        if os.path.isfile(self.app.config['DB_PATH']):
            os.remove(self.app.config['DB_PATH'])
        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("CREATE TABLE test1 (id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, password STRING (1, 8), [unique] STRING UNIQUE, cd STRING DEFAULT notcorrect);")
        conn.commit()
        conn.close()

        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            name = StringColumn(not_null=True)
            password = StringColumn(min_length=3, max_length=16)
            unique = StringColumn(unique=True)
            cd = StringColumn(default='correct value')

        self.db.register_model(Test1)
        path = self.db.make_migrations(test=True)
        self.db.session.stop()
        with open(path, 'r') as f:
            migrations_file_data = f.read()
        migrations_file_data = migrations_file_data.replace(migrations_file_data.split('\n')[0], '')
        if migrations_file_data == single_model_update_make_migrations_correct:
            return True
        return False


two_model_update_make_migrations_correct = '''
from sql_cable.migrations import Migration


class test1(Migration):
    def __init__(self):
        self.table_name = 'test1'
        self.table_creation_str = 'CREATE TABLE test1 ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [password] STRING, [username] STRING UNIQUE)'
        self.changes = ['password is meant to have a type of STRING not STRING (1, 8)', 'username does not exist']
        self.columns = ['id', 'password', 'username']
        self.action = 'UPDATE'


class test2(Migration):
    def __init__(self):
        self.table_name = 'test2'
        self.table_creation_str = 'CREATE TABLE test2 ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [test1_id] INTEGER REFERENCES test1 (id)  ON DELETE CASCADE)'
        self.changes = ["test1_id's on_delete is meant to be CASCADE but is SET NULL", "test1_id's on_update is meant to be NONE but is SET DEFAULT"]
        self.columns = ['id', 'test1_id']
        self.action = 'UPDATE'


models = [test1(), test2()]'''


class TwoModelUpdateMakeMigrations:
    def __init__(self, app):
        self.test_name = 'TwoModelUpdateMakeMigrations'
        self.app = app

    def run(self):
        if os.path.isdir('migrations'):
            shutil.rmtree('migrations')
        if os.path.isfile(self.app.config['DB_PATH']):
            os.remove(self.app.config['DB_PATH'])
        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("CREATE TABLE test1 (id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, password STRING (1, 8), [unique] STRING UNIQUE, cd STRING DEFAULT notcorrect);")
        c.execute("CREATE TABLE test2 (id INTEGER PRIMARY KEY AUTOINCREMENT, test1_id INTEGER REFERENCES test1 (id) ON DELETE SET NULL ON UPDATE SET DEFAULT);")
        conn.commit()
        conn.close()

        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            username = StringColumn(unique=True)
            password = StringColumn()

        class Test2(Model):
            id = PrimaryKeyColumn()
            test1_id = ForeignKeyColumn(Test1)

        self.db.register_model(Test1)
        self.db.register_model(Test2)
        path = self.db.make_migrations(test=True)
        self.db.session.stop()
        with open(path, 'r') as f:
            migrations_file_data = f.read()
        migrations_file_data = migrations_file_data.replace(migrations_file_data.split('\n')[0], '')
        if migrations_file_data == two_model_update_make_migrations_correct:
            return True
        return False


class MakeMigrationTests:
    def __init__(self, app):
        self.name = 'MakeMigrationTests'
        self.app = app
        self.tests = [SingleModelMakeMigrations(self.app, StringColumn),
                      SingleModelMakeMigrations(self.app, IntegerColumn),
                      SingleModelMakeMigrations(self.app, FloatColumn),
                      SingleModelMakeMigrations(self.app, BooleanColumn),
                      DoubleModelMakeMigrations(self.app),
                      SingleModelUpdateMakeMigrations(self.app),
                      TwoModelUpdateMakeMigrations(self.app)]

    def run(self):
        output = ""
        tests_run = 0
        tests_passed = 0
        for test in self.tests:
            tests_run += 1
            try:
                result = test.run()
                output += get_test_str(test.test_name, result)
                if result:
                    tests_passed += 1
            except Exception as e:
                test.run()
        return output, tests_run, tests_passed
