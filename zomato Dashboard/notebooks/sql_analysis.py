
import mysql.connector
import pandas as pd

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ram455@#",
    database="zomato_db"
)

query = """
SELECT City,
       ROUND(AVG(Rating), 2) AS Average_Rating,
       COUNT(*) AS Restaurant_Count
FROM restaurants
GROUP BY City
ORDER BY Average_Rating DESC;
"""

df = pd.read_sql(query, connection)

print("\nCity-wise Restaurant Analysis:")
print(df)

connection.close()