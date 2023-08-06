from .. import DB, Model
from ..columns import (PrimaryKeyColumn, ForeignKeyColumn,
                       StringColumn, IntegerColumn,
                       FloatColumn, BooleanColumn)
from .req import get_test_str, get_default_value
import os
import shutil
import sqlite3
import time


two_model_migration = '''
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


class TwoModelMigration:
    def __init__(self, app):
        self.test_name = 'TwoModelMigration'
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

        if not os.path.isdir('migrations'):
            os.mkdir('migrations')
            with open(os.path.join('migrations', '__init__.py'), 'w') as f:
                f.write("\nfrom . import migration_1")
        with open(os.path.join('migrations', 'migration_1.py'), 'w') as f:
            f.write(two_model_migration)
        self.db.migrate()
        self.db.session.stop()

        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("PRAGMA table_info(test1);")
        table_info = c.fetchall()
        if table_info[0][1] == 'id' and table_info[1][1] == 'name':
            c.execute("PRAGMA table_info(test2);")
            table_info = c.fetchall()
            conn.close()
            if table_info[0][1] == 'id' and table_info[1][1] == 'test_1_id':
                return True
        return False


class MigrateTests:
    def __init__(self, app):
        self.name = 'MigrateTests'
        self.app = app
        self.tests = [TwoModelMigration(self.app)]

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
