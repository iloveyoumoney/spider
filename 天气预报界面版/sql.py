import pymysql
from config import lists

def insert_data():
    print('连接到mysql服务器...')
    db = pymysql.connect(host='localhost',user='root',password='root',db='weather',charset='utf8')
    print('连接上了!')
    cursor = db.cursor()
    for list in lists:
        c_id = list[0]
        c_name = list[1]
        c_code = list[2]
        sql_insert  = " insert into cityWeather (id,cityName,cityCode)values(%s,%s,%s)"
        cursor.execute(sql_insert,(c_id,c_name,c_code))
        db.commit()
    cursor.close()
    db.close()
    print ('数据插入mysql数据库完成...')


if __name__ == '__main__':
    insert_data()
