
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ram455@#",
    database="zomato_db"
)

# Restaurants by city
query = """
SELECT City, COUNT(*) AS Restaurant_Count
FROM restaurants
GROUP BY City
ORDER BY Restaurant_Count DESC;
"""

df = pd.read_sql(query, connection)

plt.figure(figsize=(10, 5))

plt.bar(df["City"], df["Restaurant_Count"])

plt.title("Number of Restaurants by City")
plt.xlabel("City")
plt.ylabel("Number of Restaurants")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

connection.close()