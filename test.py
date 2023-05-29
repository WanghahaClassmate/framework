import psycopg2
class node():
    def __init__(self) -> None:
        self.host = "192.168.24.131"
        self.port = 15432
        self.user = "hubble"
        self.password = "hubble"
        self.database = "db_hilbert_test"

parameter = node()
conn = psycopg2.connect(host=parameter.host,
                        port=parameter.port,
                        user=parameter.user,
                        password=parameter.password,
                        database=parameter.database,)
cur = conn.cursor()
'''执行语句'''
cur.execute("select * from public.demotable limit 10;")
'''获取结果集的每一行'''
rows = cur.fetchall()
'''循环输出结果行'''
for row in  rows:
    print(row)
'''关闭游标'''
conn.close()
