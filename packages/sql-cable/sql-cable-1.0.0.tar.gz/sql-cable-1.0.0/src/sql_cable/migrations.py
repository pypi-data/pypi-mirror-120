from .queries import SelectObject, InsertObject


class Migration:
    def create(self):
        self.session.add(InsertObject(self.table_creation_str, commit=True))

    def update(self):
        # getting data before removing the table
        table_info = self.session.select(SelectObject(f"PRAGMA table_info({self.table_name});"), fetch_mode='all')
        table_data = self.session.select(SelectObject(f"SELECT * FROM {self.table_name}"), fetch_mode='all')

        # remaking the table
        self.session.add(InsertObject(f"DROP TABLE {self.table_name}", commit=True))
        self.session.add(InsertObject(self.table_creation_str, commit=True))

        # making the query to add all the data back into the table
        columns_str = ""
        values_str = "("
        for column in table_info:
            columns_str += column[1] + ', '
            values_str += '?, '
        values_str = values_str[:-2] + ')'
        f_value_str = ""
        for row in table_info:
            f_value_str += values_str + ', '

        self.session.add(InsertObject(f"INSERT INTO {self.table_name} ({columns_str[:-2]}) VALUES {f_value_str[:-2]};", params=table_data, commit=True))

    def run_migrations(self, db_path, session):
        self.db_path = db_path
        self.session = session
        if self.action == 'CREATE':
            self.create()
        elif self.action == 'UPDATE':
            self.update()
        else:
            print(f"action '{self.action}' is not recognized.")
