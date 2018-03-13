# coding: utf-8
import unittest
from lagavulin.models.AlchemyBase import AlchemyBase
import sqlalchemy


class TestAlchemyBase(unittest.TestCase):
    def setUp(self):
        self.base = AlchemyBase(yaml_file_path="../../config/mysql.yml")

    def test_get_engine(self):
        self.assertIsInstance(self.base.engine, sqlalchemy.engine.base.Engine)

        engine = self.base._get_engine()
        self.assertIsInstance(engine, sqlalchemy.engine.base.Engine)

    def test_get_connection(self):
        conn = self.base.get_connection()
        self.assertTrue(conn.connection.is_valid)
        conn.close()

    def test_create_table(self):
        self.base.create_table("test1")
        element = self.base.execute_query("DESC test1")
        element = element.fetchall()
        answer = [
            ("test_id", "int(11)", "NO", "PRI", None, "auto_increment"),
            ("test_text", "text", "YES", "", None, ""),
            ("test_score", "float", "YES", "", None, ""),
            ("created_at", "datetime", "YES", "", "CURRENT_TIMESTAMP", ""),
            ("updated_at", "datetime", "YES", "", "CURRENT_TIMESTAMP", "on update CURRENT_TIMESTAMP")]
        self.assertListEqual(element, answer)

    def test_initialize_db(self):
        self.base.initialize_db()
        table_names = self.base.execute_query("SHOW TABLES")
        answer = [("performance_test",), ("test1",), ("test2",), ("dummy",)]
        self.assertListEqual(sorted(table_names), sorted(answer))

    def test_get_column_names(self):
        col_names = self.base.get_column_names("test1")
        answer = ["test_id", "test_text", "test_score"]
        self.assertListEqual(col_names, answer)

    def test_insert_dataframe(self):
        import pandas as pd
        self.base.create_table("test2")
        df = pd.DataFrame([[1, 'lagavulin'], [2, 'laphroaig']], columns=['test_id', 'test_content'])
        self.base.insert_dataframe(df, 'test2')

        res = self.base.execute_query("SELECT test_id, test_content FROM test2")
        res = res.fetchall()
        answer = [(1, 'lagavulin'), (2, 'laphroaig')]
        self.assertListEqual(res, answer)

    def tearDown(self):
        del self.base


if __name__ == "__main__":
    unittest.main()
