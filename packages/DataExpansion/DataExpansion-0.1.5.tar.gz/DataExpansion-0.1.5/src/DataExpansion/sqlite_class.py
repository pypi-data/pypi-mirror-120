import sqlite3

class IntegerField:
    def __init__(self, name, id):
        """
        整数型フィールドです。int型と対応します。
        Parameters
        ----------
        name : str
            カラム名
        id : int
            プライマリーキーにし、IDとして利用することができます。
            Trueした場合どのような数を代入しても自動で番号が付けられます。
        """
        self.name = name
        self.id = id

class CharField:
    def __init__(self, name):
        """
        文字型フィールドです。str型と対応します。
        Parameters
        ----------
        name : str
            カラム名
        """
        self.name = name

class TextField:
    def __init__(self, name):
        """
        テキスト型フィールド。str型と対応します。
        Parameters
        ----------
        name : str
            カラム名
        """
        self.name = name

class BooleanField:
    def __init__(self, name):
        """
        真偽型フィールド。bool型と対応します。
        Parameters
        ----------
        name : str
            カラム名
        """
        self.name = name

class SQLite_Ex:
    def __init__(self, callback, args : list, fields : list, table_name : str, sql_connection : sqlite3.Connection, **options : dict):
        """
        SQLiteのカーソルを作成し、コールバックを設定します。
        Parameters
        ----------
        callback : function
            レコードからモデルを作成する時に呼び出す関数(クラスの__init__の場合はクラス)
        args : list
            callbackを呼び出す際に渡す引数。
        fields : list
            テーブルのフィールド。callbackを呼び出す際、fields + argsで引数が渡されます。
        table_name : str
            SQLに保存するテーブル名。英数字のみ。
            ※ValueErrorを返します。
        sql_connection : sqlite3.Connection
            SQLiteのカーソルを取得するためのコネクション
        **options : dict
            sqliteのオプション 未実装
        """
        self.__callback = callback
        self.args = args
        for field in fields:
            try:
                a = field.name
            except AttributeError:
                ValueError("Not a field type")
        self.__fields = fields
        
        #テーブルに使える文字か判定
        if table_name.isalnum():
            self.__table_name = table_name
        else:
            raise ValueError("Only alphanumeric characters can be used in the table name.")

        self.sql_connection = sql_connection
        self.sql_cursor = sql_connection.cursor()

    def sql_init(self) -> int:
        """
        SQLiteのテーブルを初期化します。既存のデータは削除されます。
        テーブルを作成していない場合は、model_setメソッド, model_getメソッドを呼び出す前に、このメソッドを呼び出してください。
        Returns
        ----------
        result : int
            結果を数値で返します
            0 正常終了
        """
        self.sql_cursor.execute(f"DROP TABLE IF EXISTS {self.__table_name}")
        sql = f"CREATE TABLE  {self.__table_name}("
        loop = 1
        for field in self.__fields:
            if type(field) == IntegerField:
                sql += f"{field.name} INTEGER"
                if field.id == True:
                    sql += " PRIMARY KEY AUTOINCREMENT"
            elif type(field) == CharField:
                sql += f"{field.name} VARCHAR"
            elif type(field) == TextField:
                sql += f"{field.name} TEXT"
            elif type(field) == BooleanField:
                sql += f"{field.name} BOOLEAN"
            if loop != len(self.__fields):
                sql += ", "
            loop += 1
        
        sql += ")"
        print(sql)
        self.sql_cursor.execute(sql)
        self.sql_connection.commit()
        
    def model_set(self, fields : list):
        """
        SQLiteのカーソルを作成し、コールバックを設定します。
        Parameters
        ----------
        fields : list
            テーブルに追加するレコード、設定したフィールドと対応する型にするようにしてください。
        """
        if len(self.__fields) != len(fields):
            raise ValueError("Does not match the set field")

        sql = f"INSERT INTO {self.__table_name}("
        sql_fields = []
        loop = 1
        for field in self.__fields:
            if type(field) == IntegerField:
                if field.id == True:
                    loop += 1
                    continue
                sql += f"{field.name}"
            elif type(field) == CharField:
                sql += f"{field.name}"
            elif type(field) == TextField:
                sql += f"{field.name}"
            elif type(field) == BooleanField:
                sql += f"{field.name}"
            if loop != len(self.__fields):
                sql += ", "
            loop += 1
        sql += ") VALUES("
        loop = 1
        for field in zip(self.__fields, fields):
            if type(field[0]) == IntegerField and type(field[1]) != int:
                raise ValueError("Does not match the set field")
            elif type(field[0]) == CharField and type(field[1]) != str:
                raise ValueError("Does not match the set field")
            elif type(field[0]) == TextField and type(field[1]) != str:
                raise ValueError("Does not match the set field")
            elif type(field[0]) == BooleanField and type(field[1]) != bool:
                raise ValueError("Does not match the set field")
            if type(field[0]) == IntegerField:
                if field[0].id == True:
                    loop += 1
                    continue
            sql += "?"
            sql_fields.append(field[1])
            if loop != len(self.__fields):
                sql += ", "
            loop += 1

        sql += ")"
        print(sql)
        self.sql_cursor.execute(sql, sql_fields)
        self.sql_connection.commit()

    def model_getall(self):
        """
        すべてのレコードをコールバックの引数にいれて実行します
        Returns
        ----------
        result : None
            コールバックの返り値を返します
        """
        result = []
        self.sql_cursor.execute(f"SELECT * FROM {self.__table_name}")
        for row in self.sql_cursor:
            args = list(row) + self.args
            result.append(self.__callback(*args))
        return result

    def model_getif(self, conditions : str, placeholder : list):
        """
        条件に当てはまるモデルを一つだけ返します。
        Parameters
        ----------
        conditions : str
            条件文
        placeholder : list
            プレースホルダ
        """
        sql = f"SELECT * FROM {self.__table_name} WHERE {conditions} LIMIT 1"
        self.sql_cursor.execute(sql, placeholder)
        if self.sql_cursor.fetchone() == None:
            return None
        args = self.args + list(self.sql_cursor.fetchone())
        return self.__callback(*args)
    
    def model_getif_all(self, conditions : str, placeholder : list):
        """
        条件に当てはまるモデルをすべて返します。
        Parameters
        ----------
        conditions : str
            条件文
        placeholder : list
            プレースホルダ
        """
        sql = f"SELECT * FROM {self.__table_name} WHERE {conditions}"
        print(sql)
        self.sql_cursor.execute(sql, placeholder)
        result = []
        for row in self.sql_cursor:
            args = list(row) + self.args
            result.append(self.__callback(*args))
        return result

