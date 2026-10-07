import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ram455@#",
    database="zomato_db"
)

# 1. Restaurants by City
query1 = """
SELECT City, COUNT(*) AS Restaurant_Count
FROM restaurants
GROUP BY City
ORDER BY Restaurant_Count DESC;
"""

city_df = pd.read_sql(query1, connection)

plt.figure(figsize=(10, 5))
plt.bar(city_df["City"], city_df["Restaurant_Count"])
plt.title("Restaurants by City")
plt.xlabel("City")
plt.ylabel("Number of Restaurants")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 2. Average Rating by City
query2 = """
SELECT City, ROUND(AVG(Rating), 2) AS Average_Rating
FROM restaurants
GROUP BY City
ORDER BY Average_Rating DESC;
"""

rating_df = pd.read_sql(query2, connection)

plt.figure(figsize=(10, 5))
plt.bar(rating_df["City"], rating_df["Average_Rating"])
plt.title("Average Rating by City")
plt.xlabel("City")
plt.ylabel("Average Rating")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 3. Online Delivery
query3 = """
SELECT Online_Delivery, COUNT(*) AS Restaurant_Count
FROM restaurants
GROUP BY Online_Delivery;
"""

delivery_df = pd.read_sql(query3, connection)

plt.figure(figsize=(7, 5))
plt.bar(
    delivery_df["Online_Delivery"],
    delivery_df["Restaurant_Count"]
)
plt.title("Online Delivery Availability")
plt.xlabel("Online Delivery")
plt.ylabel("Number of Restaurants")
plt.tight_layout()
plt.show()


# 4. Average Cost by City
query4 = """
SELECT City,
       ROUND(AVG(Average_Cost_for_Two), 2) AS Average_Cost
FROM restaurants
GROUP BY City
ORDER BY Average_Cost DESC;
"""

cost_df = pd.read_sql(query4, connection)

plt.figure(figsize=(10, 5))
plt.bar(cost_df["City"], cost_df["Average_Cost"])
plt.title("Average Cost for Two by City")
plt.xlabel("City")
plt.ylabel("Average Cost")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

connection.close()

print("Dashboard analysis completed successfully!")
