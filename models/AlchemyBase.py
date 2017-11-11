# coding:utf-8

import copy
import pandas
import sqlalchemy
from sqlalchemy import Table, MetaData, select, func, and_, desc
import yaml


fixed_column_list = [
    "created_at DATETIME DEFAULT CURRENT_TIMESTAMP",
    "updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
]


class AlchemyBase(object):
    def __init__(self, yaml_file_path="../config/mysql.yml"):
        self.yaml_file_path = yaml_file_path
        self.config = yaml.load(open(yaml_file_path, 'r'))
        self.engine = self.get_engine()
        self.metadata = sqlalchemy.MetaData(self.engine)
        self.metadata.reflect()

        self.tables = dict()
        for table_name in self.config['tables']:
            self.tables[table_name] = None

        # DB内にあるテーブルをインスタンス化して辞書として保持。
        # mysql.yml に記載されてるがテーブルが建っていないものは None
        for table in self.metadata.sorted_tables:
            self.tables[table.description] = table

    def get_engine(self):
        mysql_url = "mysql+pymysql://%s:%s@%s/%s?charset=utf8" % \
                    (self.config["connection"]["user"],
                     self.config["connection"]["pw"],
                     self.config["connection"]["host"],
                     self.config["connection"]["db"])
        engine = sqlalchemy.create_engine(mysql_url, encoding="utf-8", echo=False)
        return engine

    def get_connection(self):
        return self.engine.connect()

    def initialize_db(self):
        for table_name in self.tables.keys():
            self.create_table(table_name)

    def create_table(self, table_name):
        try:
            columns = self.config["tables"][table_name]["columns"]
        except KeyError:
            raise "table %s doesn't exist in config" % table_name

        try:
            additional_config = self.config["tables"][table_name]["additional_config"]
        except KeyError:
            additional_config = None

        raw_columns = []
        for column_item in columns:
            raw_columns.append(column_item.split(" ")[0])

        all_columns = copy.deepcopy(columns)
        all_raw_columns = copy.deepcopy(raw_columns)
        all_columns.extend(fixed_column_list)

        for column_item in fixed_column_list:
            all_raw_columns.append(column_item.split(" ")[0])

        conn = self.get_connection()
        conn.execute("DROP TABLE IF EXISTS %s" % table_name)
        columns_str = ",".join(all_columns)
        if additional_config:
            query = "CREATE TABLE %s (%s) %s" % (table_name, columns_str, additional_config)
        else:
            query = "CREATE TABLE %s (%s)" % (table_name, columns_str)

        conn.execute(query)
        conn.close()
        self.metadata.reflect()
        self.tables[table_name] = self.metadata.tables[table_name]

    def execute_query(self, query):
        return self.engine.execute(query).fetchall()
