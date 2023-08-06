from .. import DB, Model
from ..columns import (PrimaryKeyColumn, ForeignKeyColumn,
                       StringColumn, IntegerColumn,
                       FloatColumn, BooleanColumn)
from .req import get_test_str, get_default_value
import os
import shutil
import sqlite3


class NonCommitInsertTest:
    def __init__(self, app):
        self.test_name = 'NonCommitInsertTest'
        self.app = app

    def run(self):
        if os.path.isdir('migrations'):
            shutil.rmtree('migrations')
        if os.path.isfile(self.app.config['DB_PATH']):
            os.remove(self.app.config['DB_PATH'])
        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("CREATE TABLE test1 (id INTEGER PRIMARY KEY AUTOINCREMENT, username STRING, password STRING);")
        conn.commit()
        conn.close()

        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            username = StringColumn()
            password = StringColumn()

        self.db.register_model(Test1)

        obj = Test1.insert(username='username1', password='password1')
        self.db.session.add(obj)
        self.db.session.commit()
        self.db.session.stop()

        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("SELECT * FROM test1")
        data = c.fetchone()
        conn.close()
        if data[1] != 'username1' or data[2] != 'password1':
            return False
        return True


class NonCommitMultipoolInsertTest:
    def __init__(self, app):
        self.test_name = 'NonCommitMultipoolInsertTest'
        self.app = app

    def run(self):
        if os.path.isdir('migrations'):
            shutil.rmtree('migrations')
        if os.path.isfile(self.app.config['DB_PATH']):
            os.remove(self.app.config['DB_PATH'])
        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("CREATE TABLE test1 (id INTEGER PRIMARY KEY AUTOINCREMENT, username STRING, password STRING);")
        conn.commit()
        conn.close()

        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            username = StringColumn()
            password = StringColumn()

        self.db.register_model(Test1)

        obj = Test1.insert(username='username1', password='password1')
        self.db.session.add(obj)
        obj = Test1.insert(username='username2', password='password2')
        self.db.session.add(obj)
        obj = Test1.insert(username='username3', password='password3')
        self.db.session.add(obj)
        self.db.session.commit()
        self.db.session.stop()

        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("SELECT * FROM test1")
        data = c.fetchall()
        conn.close()
        for i in range(3):
            if data[i][1] != 'username' + str(i + 1) or data[i][2] != 'password' + str(i + 1):
                return False
        return True


class CommitInsertTest:
    def __init__(self, app):
        self.test_name = 'CommitInsertTest'
        self.app = app

    def run(self):
        if os.path.isdir('migrations'):
            shutil.rmtree('migrations')
        if os.path.isfile(self.app.config['DB_PATH']):
            os.remove(self.app.config['DB_PATH'])
        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("CREATE TABLE test1 (id INTEGER PRIMARY KEY AUTOINCREMENT, username STRING, password STRING);")
        conn.commit()
        conn.close()

        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            username = StringColumn()
            password = StringColumn()

        self.db.register_model(Test1)

        Test1.insert(username='username1', password='password1', commit=True)
        self.db.session.stop()

        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("SELECT * FROM test1")
        data = c.fetchone()
        conn.close()
        if data[1] != 'username1' or data[2] != 'password1':
            return False
        return True


class Insert:
    def __init__(self, app):
        self.name = 'InsertTests'
        self.app = app
        self.tests = [NonCommitInsertTest(self.app),
                      NonCommitMultipoolInsertTest(self.app),
                      CommitInsertTest(self.app)]

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
