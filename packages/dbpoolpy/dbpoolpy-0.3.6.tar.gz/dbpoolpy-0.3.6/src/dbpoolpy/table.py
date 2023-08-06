from functools import wraps
from .dbpool import acquire, release
from .dbo import SelectO, InsertO, UpdateO, DeleteO

class TableBase():

    def __init__(self, db):
        self._db = db
        self._conn = None
        self.open_conn()

    def __enter__(self):
        return self

    def __exit__(self):
        ''' 退出时如果没有关闭，则关闭连接 '''
        self.close_conn()

    def __del__(self):
        ''' 变量回收时，关闭连接 '''
        self.close_conn()

    def close_conn(self):
        if self._conn:
            release(self._conn)
            self._conn = None

    def open_conn(self):
        if not self._conn:
            _conn = acquire(self._db)
            self._conn = _conn
            return _conn
        else:
            return _conn

    def sql(self, cls, is_auto_close):
        sql = cls.sql(self)
        if is_auto_close:
            self.close_conn()
        return sql

    def execute(self):
        if not self._conn:
            self.open_conn()
        sql = self.sql(is_auto_close=False)
        res = self._conn.execute(sql)
        self.close_conn()
        return res


class SelectTable(TableBase, SelectO):
    def __init__(self, db, table):
        TableBase.__init__(self, db)
        SelectO.__init__(self, dbo=self._conn, tables=table)

    def sql(self, is_auto_close=True):
        return TableBase.sql(self, SelectO, is_auto_close)

    def all(self, isdict=True):
        if not self._conn:
            self.open_conn()
        sql = self.sql(is_auto_close=False)
        res = self._conn.query(sql, None, isdict=isdict)
        self.close_conn()
        return res

    def first(self, isdict=True):
        if not self._conn:
            self.open_conn()
        sql = self.sql(is_auto_close=False)
        if sql.find('limit') == -1:
            sql += ' limit 1'
        res = self._conn.get(sql, None, isdict=isdict)
        self.close_conn()
        return res

class InsertTable(TableBase, InsertO):
    def __init__(self, db, table):
        TableBase.__init__(self, db)
        InsertO.__init__(self, dbo=self._conn, table=table)

    def sql(self, is_auto_close=True):
        return TableBase.sql(self, InsertO, is_auto_close)

class UpdateTable(TableBase, UpdateO):
    def __init__(self, db, table):
        TableBase.__init__(self, db)
        UpdateO.__init__(self, dbo=self._conn, table=table)

    def sql(self, is_auto_close=True):
        return TableBase.sql(self, UpdateO, is_auto_close)

class DeleteTable(TableBase, DeleteO):
    def __init__(self, db, table):
        TableBase.__init__(self, db)
        DeleteO.__init__(self, dbo=self._conn, table=table)

    def sql(self, is_auto_close=True):
        return TableBase.sql(self, DeleteO, is_auto_close)


