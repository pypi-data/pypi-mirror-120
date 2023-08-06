from .. import DB, Model
from ..columns import (PrimaryKeyColumn, ForeignKeyColumn,
                       StringColumn, IntegerColumn,
                       FloatColumn, BooleanColumn)
from .req import get_test_str, get_default_value
import os
import shutil
import sqlite3


class UpdateAllTest:
    def __init__(self, app, commit):
        self.test_name = 'UpdateAllTest'
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
        conn.commit()
        conn.close()

        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            username = StringColumn()
            password = StringColumn()

        self.db.register_model(Test1)

        if self.commit:
            Test1.update(username='username2', commit=True).all()
        else:
            obj = Test1.update(username='username2').all()
            self.db.session.add(obj)
            self.db.session.commit()
        self.db.session.stop()

        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("SELECT * FROM test1")
        data = c.fetchone()
        conn.close()
        if data[1] != 'username2':
            return False
        return True


class UpdateWhereTest:
    def __init__(self, app, commit):
        self.test_name = 'UpdateAllTest'
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
            Test1.update(username='username3', commit=True).where(password='password1')
        else:
            obj = Test1.update(username='username3').where(password='password1')
            self.db.session.add(obj)
            self.db.session.commit()
        self.db.session.stop()

        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("SELECT * FROM test1 WHERE username = ?", ('username3',))
        data = c.fetchall()
        conn.close()
        if len(data) != 1:
            return False
        return True


class Update:
    def __init__(self, app):
        self.name = 'UpdateTests'
        self.app = app
        self.tests = [UpdateAllTest(self.app, True),
                      UpdateAllTest(self.app, False),
                      UpdateWhereTest(self.app, True),
                      UpdateWhereTest(self.app, False)]

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
