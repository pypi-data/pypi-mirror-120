from .. import DB, Model
from ..columns import (PrimaryKeyColumn, ForeignKeyColumn,
                       StringColumn, IntegerColumn,
                       FloatColumn, BooleanColumn)
from ..queries.query_objects import FilterObject
from .req import get_test_str, get_default_value
import os
import shutil
import sqlite3


class FinalFunctionsTest:
    def __init__(self, app, fetch_mode):
        self.test_name = 'FinalFunctionsTest'
        self.app = app
        self.fetch_mode = fetch_mode

    def run(self):
        if os.path.isdir('migrations'):
            shutil.rmtree('migrations')
        if os.path.isfile(self.app.config['DB_PATH']):
            os.remove(self.app.config['DB_PATH'])
        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("CREATE TABLE test1 (id INTEGER PRIMARY KEY AUTOINCREMENT, username STRING, password STRING);")
        conn.commit()
        value_str = ""
        params = []
        for i in range(8):
            value_str += "(?, ?), "
            params.append('testuser' + str(i + 1))
            params.append('password' + str(i + 1))
        c.execute(f"INSERT INTO test1 (username, password) VALUES {value_str[:-2]}", tuple(params))
        conn.commit()
        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            username = StringColumn()
            password = StringColumn()

        self.db.register_model(Test1)
        if self.fetch_mode == 'all':
            result = Test1.select.all()
            self.db.session.stop()
            if len(result) != 8:
                return False
            for i in range(len(result)):
                if result[i].username != 'testuser' + str(i + 1):
                    return False
                if result[i].password != 'password' + str(i + 1):
                    return False
        if self.fetch_mode == 'one':
            result = Test1.select.one()
            self.db.session.stop()
            if result.username != 'testuser1' and result.password != 'password1':
                return False
        return True


class FinalFunctionsEmptyTest:
    def __init__(self, app, fetch_mode):
        self.test_name = 'FinalFunctionsEmptyTest'
        self.app = app
        self.fetch_mode = fetch_mode

    def run(self):
        if os.path.isdir('migrations'):
            shutil.rmtree('migrations')
        if os.path.isfile(self.app.config['DB_PATH']):
            os.remove(self.app.config['DB_PATH'])
        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("CREATE TABLE test1 (id INTEGER PRIMARY KEY AUTOINCREMENT, username STRING, password STRING);")
        conn.commit()
        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            username = StringColumn()
            password = StringColumn()

        self.db.register_model(Test1)
        if self.fetch_mode == 'all':
            result = Test1.select.all()
            self.db.session.stop()
            if not result:
                return True
        if self.fetch_mode == 'one':
            result = Test1.select.one()
            self.db.session.stop()
            if result.id is None and result.username is None and result.password is None:
                return True
        return False


class ForeignKeySelectTest:
    def __init__(self, app):
        self.test_name = 'ForeignKeySelectTest'
        self.app = app

    def run(self):
        if os.path.isdir('migrations'):
            shutil.rmtree('migrations')
        if os.path.isfile(self.app.config['DB_PATH']):
            os.remove(self.app.config['DB_PATH'])
        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("CREATE TABLE test1 (id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, password STRING);")
        conn.commit()
        c.execute("CREATE TABLE test2 (id INTEGER PRIMARY KEY AUTOINCREMENT, test1_id REFERENCES test1 ([id]) ON DELETE CASCADE);")
        conn.commit()
        c.execute("INSERT INTO test1 (id, name, password) VALUES (?, ?, ?)", (1, 'name1', 'password1'))
        conn.commit()
        c.execute("INSERT INTO test2 (test1_id) VALUES (?)", (1,))
        conn.commit()

        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            name = StringColumn()
            password = StringColumn()

        class Test2(Model):
            id = PrimaryKeyColumn()
            test1_id = ForeignKeyColumn(Test1)

        self.db.register_model(Test1)
        self.db.register_model(Test2)

        select_data = Test2.select.one()
        self.db.session.stop()
        if select_data.test1_id.rows[0].name != 'name1':
            return False
        if select_data.test1_id.rows[0].password != 'password1':
            return False
        if select_data.test1_id.value != 1:
            return False
        return True


class SortByTests:
    def __init__(self, app):
        self.test_name = 'SortByTests'
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
        value_str = ""
        params = []
        for i in range(8):
            value_str += "(?, ?), "
            params.append('testuser' + str(i + 1))
            params.append('password' + str(i + 1))
        c.execute(f"INSERT INTO test1 (username, password) VALUES {value_str[:-2]}", tuple(params))
        conn.commit()

        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            username = StringColumn()
            password = StringColumn()

        self.db.register_model(Test1)

        result = Test1.select.sortby(id='DESC').all()
        self.db.session.stop()
        correct_number = 8
        for i in range(8):
            if result[i].id != correct_number:
                return False
            correct_number -= 1
        return True


class FilterTests:
    def __init__(self, app, fetch_mode):
        self.test_name = 'FilterTests'
        self.app = app
        self.fetch_mode = fetch_mode

    def run(self):
        if os.path.isdir('migrations'):
            shutil.rmtree('migrations')
        if os.path.isfile(self.app.config['DB_PATH']):
            os.remove(self.app.config['DB_PATH'])
        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("CREATE TABLE test1 (id INTEGER PRIMARY KEY AUTOINCREMENT, username STRING, password STRING);")
        conn.commit()
        value_str = ""
        params = []
        for i in range(8):
            value_str += "(?, ?), "
            params.append('testuser' + str(i + 1))
            params.append('password' + str(i + 1))
        c.execute(f"INSERT INTO test1 (username, password) VALUES {value_str[:-2]}", tuple(params))
        conn.commit()
        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            username = StringColumn()
            password = StringColumn()

        self.db.register_model(Test1)

        if self.fetch_mode == 'all':
            result = Test1.select.filter(username='testuser4').all()
            self.db.session.stop()
            if len(result) != 1:
                return False
            if result[0].username != 'testuser4' or result[0].password != 'password4':
                return False
            return True
        elif self.fetch_mode == 'one':
            result = Test1.select.filter(username='testuser4').one()
            self.db.session.stop()
            if result.username != 'testuser4' or result.password != 'password4':
                return False
            return True


class FilterObjectTests:
    def __init__(self, app, fetch_mode):
        self.test_name = 'FilterObjectTests'
        self.app = app
        self.fetch_mode = fetch_mode

    def run(self):
        if os.path.isdir('migrations'):
            shutil.rmtree('migrations')
        if os.path.isfile(self.app.config['DB_PATH']):
            os.remove(self.app.config['DB_PATH'])
        conn = sqlite3.connect(self.app.config['DB_PATH'])
        c = conn.cursor()
        c.execute("CREATE TABLE test1 (id INTEGER PRIMARY KEY AUTOINCREMENT, username STRING, password STRING);")
        conn.commit()
        value_str = ""
        params = []
        for i in range(8):
            value_str += "(?, ?), "
            params.append('testuser' + str(i + 1))
            params.append('password' + str(i + 1))
        c.execute(f"INSERT INTO test1 (username, password) VALUES {value_str[:-2]}", tuple(params))
        conn.commit()
        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            username = StringColumn()
            password = StringColumn()

        self.db.register_model(Test1)

        if self.fetch_mode == 'all':
            result = Test1.select.filter(username1=FilterObject(username='testuser4')).all()
            self.db.session.stop()
            if len(result) != 1:
                return False
            if result[0].username != 'testuser4' or result[0].password != 'password4':
                return False
            return True
        elif self.fetch_mode == 'one':
            result = Test1.select.filter(username1=FilterObject(username='testuser4')).one()
            self.db.session.stop()
            if result.username != 'testuser4' or result.password != 'password4':
                return False
            return True


class MultipoolFiltersTests:
    def __init__(self, app):
        self.test_name = 'MultipoolFiltersTests'
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
        value_str = ""
        params = []
        for i in range(8):
            value_str += "(?, ?), "
            params.append('testuser' + str(i + 1))
            params.append('password' + str(i + 1))
        c.execute(f"INSERT INTO test1 (username, password) VALUES {value_str[:-2]}", tuple(params))
        conn.commit()
        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            username = StringColumn()
            password = StringColumn()

        self.db.register_model(Test1)

        results = Test1.select.filter(username1=FilterObject(username='testuser4'), username2=FilterObject(username='testuser5'), conjunctive_op='OR').all()
        self.db.session.stop()
        if len(results) != 2:
            return False
        for result in results:
            if result.username != 'testuser4' and result.username != 'testuser5':
                return False
        return True


class FilterComparisonOpTest:
    def __init__(self, app):
        self.test_name = 'FilterComparisonOpTest'
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
        value_str = ""
        params = []
        for i in range(8):
            value_str += "(?, ?), "
            params.append('testuser' + str(i + 1))
            params.append('password' + str(i + 1))
        c.execute(f"INSERT INTO test1 (username, password) VALUES {value_str[:-2]}", tuple(params))
        conn.commit()
        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            username = StringColumn()
            password = StringColumn()

        self.db.register_model(Test1)

        results = Test1.select.filter(id=4, comparison_op='>').all()
        self.db.session.stop()
        if len(results) != 4:
            return False
        for result in results:
            if result.id <= 4:
                return False
        return True


class FilterSortTest:
    def __init__(self, app):
        self.test_name = 'FilterSortTest'
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
        value_str = ""
        params = []
        for i in range(8):
            value_str += "(?, ?), "
            params.append('testuser' + str(i + 1))
            params.append('password' + str(i + 1))
        c.execute(f"INSERT INTO test1 (username, password) VALUES {value_str[:-2]}", tuple(params))
        conn.commit()
        self.db = DB(self.app)

        class Test1(Model):
            id = PrimaryKeyColumn()
            username = StringColumn()
            password = StringColumn()

        self.db.register_model(Test1)

        results = Test1.select.filter(username='testuser3', password='password4', conjunctive_op='OR').sortby(id='DESC').all()
        self.db.session.stop()
        correct_number = 4
        if len(results) != 2:
            return False
        for i in range(len(results)):
            if results[i].id != correct_number:
                return False
            if results[i].username != 'testuser3' and results[i].password != 'password4':
                return False
            correct_number -= 1
        return True


class Select:
    def __init__(self, app):
        self.name = 'SelectTests'
        self.app = app
        self.tests = [FinalFunctionsTest(self.app, 'all'),
                      FinalFunctionsTest(self.app, 'one'),
                      FinalFunctionsEmptyTest(self.app, 'all'),
                      FinalFunctionsEmptyTest(self.app, 'one'),
                      ForeignKeySelectTest(self.app),
                      SortByTests(self.app),
                      FilterTests(self.app, 'all'),
                      FilterTests(self.app, 'one'),
                      FilterObjectTests(self.app, 'all'),
                      FilterObjectTests(self.app, 'one'),
                      MultipoolFiltersTests(self.app),
                      FilterComparisonOpTest(self.app),
                      FilterSortTest(self.app)]

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
