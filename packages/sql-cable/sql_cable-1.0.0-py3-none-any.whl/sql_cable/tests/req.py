from colorama import Fore, init, Back
init()
passed = Fore.GREEN + 'Passed' + Fore.RESET
failed = Fore.RED + 'Failed' + Fore.RESET


def get_default_value(column):
    column = column()
    if column.python_type == str:
        return 'test-string'
    if column.python_type == int:
        return 1234567890
    if column.python_type == float:
        return 100.001
    if column.python_type == bool:
        return False


def passed_str(str):
    return Fore.GREEN + str + Fore.RESET


def failed_str(str):
    return Fore.RED + str + Fore.RESET


def get_test_str(test_name, passed_test):
    return f" - {test_name} - {passed if passed_test else failed}\n"
