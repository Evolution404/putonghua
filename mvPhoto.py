import pymysql
import shutil

db= pymysql.connect(host="10.245.130.83",user="root",
 	password="root",db="putonghua")

cur=db.cursor()
sql="select * from application"
cur.execute(sql)
rs=cur.fetchall()
for r in rs:
    fileName = r[1] + '.jpg'
    shutil.copyfile('./photo/'+fileName, './applyPhoto/'+fileName)
