import mysql.connector
import pandas as pd

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ram455@#",
    database="zomato_db"
)

query = "SELECT * FROM restaurants"

df = pd.read_sql(query, connection)

print("\nZomato Data:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

connection.close()