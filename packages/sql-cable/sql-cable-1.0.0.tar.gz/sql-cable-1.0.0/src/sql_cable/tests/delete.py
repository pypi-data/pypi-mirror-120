from .. import DB, Model
from ..columns import (PrimaryKeyColumn, ForeignKeyColumn,
                       StringColumn, IntegerColumn,
                       FloatColumn, BooleanColumn)
from .req import get_test_str, get_default_value
import os
import shutil
import sqlite3


class DeleteAllTest:
    def __init__(self, app, commit):
        self.test_name = 'DeleteAllTest'
        self.app = app
        self.commit = commit

    def run(self):
        if os.path.isdir('migrations'):
            shutil.rmtree('migrations')
        if os.path.isfile(self.app.config['DB_PATH']):
            os.remove(self.app.config['DB_PATH'])
        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("CREATE TABLE test1 (id INTEGER PRIMARY KEY AUTOINCREMENT, username STRING, password STRING);")
        conn.commit()
        c.execute("INSERT INTO test1 (username, password) VALUES (?, ?)", ['username1', 'password1'])
        c.execute("INSERT INTO test1 (username, password) VALUES (?, ?)", ['username2', 'password2'])
        conn.commit()
        conn.close()

        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            username = StringColumn()
            password = StringColumn()

        self.db.register_model(Test1)

        if self.commit:
            Test1.delete(commit=True).all()
        else:
            obj = Test1.delete().all()
            self.db.session.add(obj)
            self.db.session.commit()
        self.db.session.stop()

        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("SELECT * FROM test1")
        data = c.fetchall()
        if data:
            return False
        return True


class DeleteWhereTest:
    def __init__(self, app, commit):
        self.test_name = 'DeleteWhereTest'
        self.app = app
        self.commit = commit

    def run(self):
        if os.path.isdir('migrations'):
            shutil.rmtree('migrations')
        if os.path.isfile(self.app.config['DB_PATH']):
            os.remove(self.app.config['DB_PATH'])
        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("CREATE TABLE test1 (id INTEGER PRIMARY KEY AUTOINCREMENT, username STRING, password STRING);")
        conn.commit()
        c.execute("INSERT INTO test1 (username, password) VALUES (?, ?)", ['username1', 'password1'])
        c.execute("INSERT INTO test1 (username, password) VALUES (?, ?)", ['username2', 'password2'])
        conn.commit()
        conn.close()

        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            username = StringColumn()
            password = StringColumn()

        self.db.register_model(Test1)

        if self.commit:
            Test1.delete(commit=True).where(username='username1')
        else:
            obj = Test1.delete().where(username='username1')
            self.db.session.add(obj)
            self.db.session.commit()
        self.db.session.stop()

        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("SELECT * FROM test1 WHERE username = ?", ('username1',))
        data = c.fetchall()
        conn.close()
        if data:
            return False
        return True


class Delete:
    def __init__(self, app):
        self.name = 'DeleteTests'
        self.app = app
        self.tests = [DeleteAllTest(self.app, True),
                      DeleteAllTest(self.app, False),
                      DeleteWhereTest(self.app, True),
                      DeleteWhereTest(self.app, False)]

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
