from .make_migrations import MakeMigrationTests
from .migrate import MigrateTests
from .select import Select
from .insert import Insert
from .update import Update
from .delete import Delete
from flask import Flask
import os
import shutil
from .req import passed_str


def reset(app):
    if os.path.isdir('migrations'):
        shutil.rmtree('migrations')
    if os.path.isfile(app.config['DB_PATH']):
        os.remove(app.config['DB_PATH'])


def run():
    app = Flask(__name__)
    app.config['DB_PATH'] = 'db.db'

    # tests = [Delete(app)]
    tests = [MakeMigrationTests(app), MigrateTests(app), Select(app), Insert(app), Update(app), Delete(app)]
    output = ""
    total_tests_run = 0
    total_tests_passed = 0
    for test in tests:
        output += test.name + ':\n'
        test_output, tests_run, tests_passed = test.run()
        output += test_output
        tests_passed_fraction = passed_str(f"{tests_passed}/{tests_run}")
        tests_passed_percent = passed_str(f"{(round(tests_passed / tests_run, 4) if tests_passed > 0 else 0) * 100}%")
        output += f" - {test.name} Tests Passed {tests_passed_fraction} or {tests_passed_percent}\n"
        total_tests_run += tests_run
        total_tests_passed += tests_passed
        reset(app)
    os.system('cls')
    tests_passed_fraction = passed_str(f"{total_tests_passed}/{total_tests_run}")
    tests_passed_percent = passed_str(f"{(round(total_tests_passed / total_tests_run, 4) if total_tests_passed > 0 else 0) * 100}%")
    output += f"Tests Passed {tests_passed_fraction} or {tests_passed_percent}\n"

    return output
