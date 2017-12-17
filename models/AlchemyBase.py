# coding:utf-8

import sqlalchemy
import yaml

fixed_column_list = [
    "created_at DATETIME DEFAULT CURRENT_TIMESTAMP",
    "updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
]


class AlchemyBase(object):
    def __init__(self, yaml_file_path="../config/mysql.yml"):
        yaml_file_path = yaml_file_path
        config_file = open(yaml_file_path, 'r')
        self.config = yaml.load(config_file)
        config_file.close()

        self.engine = self._get_engine()
        self.metadata = sqlalchemy.MetaData(self.engine)
        self.metadata.reflect()

        self.tables = dict()
        for table_name in self.config['tables']:
            self.tables[table_name] = None

        # DB内にあるテーブルをインスタンス化して辞書として保持。
        # mysql.yml に記載されてるがテーブルが建っていないものは None
        for table in self.metadata.sorted_tables:
            self.tables[table.description] = table

    def _get_engine(self):
        mysql_url = "mysql+pymysql://%s:%s@%s/%s?charset=utf8" % \
                    (self.config["connection"]["user"],
                     self.config["connection"]["pw"],
                     self.config["connection"]["host"],
                     self.config["connection"]["db"])
        if 'ssl' in self.config['connection']:
            ssl_args = {
                'ssl': {
                    'ca': self.config['connection']['ssl']
                }
            }
            engine = sqlalchemy.create_engine(mysql_url, encoding="utf-8", echo=False, connect_args=ssl_args)
        else:
            engine = sqlalchemy.create_engine(mysql_url, encoding="utf-8", echo=False)
        return engine

    def get_connection(self):
        return self.engine.connect()

    def initialize_db(self):
        for table_name in self.tables.keys():
            if table_name in self.config["tables"]:
                self.create_table(table_name)
            else:
                print(SystemError(
                    "There is a table in DB which is not in the config file.\ntable_name: %s is Ignored." % table_name))

    def create_table(self, table_name):
        try:
            columns = self.config["tables"][table_name]["columns"]
        except KeyError:
            raise "table %s doesn't exist in config" % table_name

        try:
            additional_config = self.config["tables"][table_name]["additional_config"]
        except KeyError:
            additional_config = None

        columns.extend(fixed_column_list)

        conn = self.get_connection()
        conn.execute("DROP TABLE IF EXISTS %s" % table_name)
        columns_str = ",".join(columns)
        if additional_config:
            query = "CREATE TABLE %s (%s) %s" % (table_name, columns_str, additional_config)
        else:
            query = "CREATE TABLE %s (%s)" % (table_name, columns_str)

        conn.execute(query)
        conn.close()
        self.metadata.reflect()
        self.tables[table_name] = self.metadata.tables[table_name]

    def execute_query(self, query):
        conn = self.get_connection()
        res = conn.execute(query).fetchall()
        conn.close()
        return res

    def get_column_names(self, table_name):
        try:
            columns = self.config["tables"][table_name]["columns"]
        except KeyError:
            raise "table %s doesn't exist in config" % table_name

        column_names = [line.split(" ")[0] for line in columns]
        return column_names

    def insert_dataframe(self, data_frame, table_name, if_exist="append"):
        conn = self.get_connection()
        data_frame.to_sql(con=conn, name=table_name, if_exists=if_exist, index=None)
        conn.close()
