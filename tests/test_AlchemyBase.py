# coding: utf-8
import unittest
from lagavulin.models.AlchemyBase import AlchemyBase
import sqlalchemy


class TestAlchemyBase(unittest.TestCase):
    def setUp(self):
        self.base = AlchemyBase()

    def test_get_engine(self):
        self.assertIsInstance(self.base.engine, sqlalchemy.engine.base.Engine)

        engine = self.base.get_engine()
        self.assertIsInstance(engine, sqlalchemy.engine.base.Engine)

    def test_get_connection(self):
        conn = self.base.get_connection()
        self.assertTrue(conn.connection.is_valid)
        conn.close()

    def test_create_table(self):
        self.base.create_table("test1")
        element = self.base.execute_query("DESC test1")
        answer = [
            ('test_id', 'int(11)', 'NO', 'PRI', None, 'auto_increment'),
            ('test_text', 'text', 'YES', '', None, ''),
            ('test_score', 'float', 'YES', '', None, ''),
            ('created_at', 'datetime', 'YES', '', 'CURRENT_TIMESTAMP', ''),
            ('updated_at', 'datetime', 'YES', '', 'CURRENT_TIMESTAMP', 'on update CURRENT_TIMESTAMP')]
        self.assertListEqual(answer, element)

    def test_initialize_db(self):
        self.base.initialize_db()
        table_names = self.base.execute_query("SHOW TABLES")
        answer = [('test1',), ('test2',)]
        self.assertListEqual(table_names, answer)

    def tearDown(self):
        del self.base


if __name__ == '__main__':
    unittest.main()
