import mysql


with mysql.dbSession() as cursor:
   cursor.execute("SELECT * FROM platforms")
   results = cursor.fetchone()
   print(results)