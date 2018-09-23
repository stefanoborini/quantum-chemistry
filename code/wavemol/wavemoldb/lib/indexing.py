from django import db 
import types

class ResultObject(object):
    def __init__(self):
        self._where = []
        self._limit = None
        self._offset = None
        self._cursor = None
    def filter(self,where_condition):
        if self._cursor:
            raise Exception("operation on materialized result")
        self._where.append(where_condition)
        return self
    def limit(self, limit):
        if self._cursor:
            raise Exception("operation on materialized result")
        self._limit = limit
        return self
    def offset(self, offset):
        if self._cursor:
            raise Exception("operation on materialized result")
        self._offset = offset
        return self
    def __iter__(self):
        return self
    def next(self):
        if not self._cursor:
            cursor = db.connection.cursor()
            query = "SELECT DISTINCT resource_uri FROM index_table "
            query += self._getLimitingClause()
            cursor.execute(query, [])
            self._cursor = cursor

        row = self._cursor.fetchone()
        if not row:
            raise StopIteration
        return row
    def _getLimitingClause(self):
        query = ""
        if len(self._where):
            query += " WHERE "
            query += " AND ".join(self._where)
        if self._limit:
            query += " LIMIT "+str(self._limit)
        if self._offset:
            query += " OFFSET "+str(self._offset)
        return query
    def count(self):
        cursor = db.connection.cursor()
        query = "SELECT COUNT(DISTINCT resource_uri) FROM index_table "
        query += self._getLimitingClause()
        print query
        cursor.execute(query, [])
        row = cursor.fetchone()
        print row
        return row[0]

 
class DbIndex(object):
    def __init__(self):
        cursor = db.connection.cursor()
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS index_table (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, resource_uri varchar(45) NOT NULL)",[])
        except:
            pass # for now
    def allUris(self):
        return ResultObject() 

    def addIndex(self, name, sql_type):
        cursor = db.connection.cursor()
        try:
            cursor.execute("ALTER TABLE index_table ADD COLUMN `"+str(name)+"` "+str(sql_type))
            cursor.execute("ALTER TABLE index_table ADD INDEX `"+str(name)+"` (`"+str(name)+"`)")
        except:
            pass

    def store(self, resource_uri, data_dict):
        def stringsqlfilter(v):
            if v is None:
                return "NULL"
            elif type(v) == types.StringType:
                return "\""+str(v)+"\""
            else:
                return str(v)
            
        cursor = db.connection.cursor()
        keys, values = zip(*data_dict.items())
        colnames = "( resource_uri, " + ",".join(keys) + ")"
        colvalues = "( \""+str(resource_uri)+"\", "+",".join(map(stringsqlfilter,values)) + ")"
        query = "INSERT INTO index_table "+colnames+" VALUES "+colvalues 
        cursor.execute(query)

    def delete(self, resource_uri):
        cursor = db.connection.cursor()
        # FIXME : I should be concerned with sql injection, but the index is always prepared by our utilities. replace with prepared statements
        query = "DELETE FROM index_table WHERE resource_uri='"+resource_uri+"'";
        cursor.execute(query)
        

    def drop(self):
        cursor = db.connection.cursor()
        try:
            cursor.execute("DROP TABLE index_table",[])
            cursor.execute("CREATE TABLE IF NOT EXISTS index_table (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, resource_uri varchar(45) NOT NULL)",[])
        except:
            pass # for now
        
