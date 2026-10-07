import mysql.connector
import pandas as pd

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ram455@#",
    database="zomato_db"
)

# 1. Top 10 restaurants
query1 = """
SELECT Restaurant_Name, City, Rating, Votes
FROM restaurants
ORDER BY Rating DESC
LIMIT 10;
"""

top_restaurants = pd.read_sql(query1, connection)

print("\n===== TOP 10 RESTAURANTS =====")
print(top_restaurants)


# 2. Restaurants by city
query2 = """
SELECT City, COUNT(*) AS Restaurant_Count
FROM restaurants
GROUP BY City
ORDER BY Restaurant_Count DESC;
"""

city_analysis = pd.read_sql(query2, connection)

print("\n===== RESTAURANTS BY CITY =====")
print(city_analysis)


# 3. Average rating by city
query3 = """
SELECT City,
       ROUND(AVG(Rating), 2) AS Average_Rating
FROM restaurants
GROUP BY City
ORDER BY Average_Rating DESC;
"""

rating_analysis = pd.read_sql(query3, connection)

print("\n===== AVERAGE RATING BY CITY =====")
print(rating_analysis)


# 4. Online delivery
query4 = """
SELECT Online_Delivery,
       COUNT(*) AS Restaurant_Count
FROM restaurants
GROUP BY Online_Delivery;
"""

delivery_analysis = pd.read_sql(query4, connection)

print("\n===== ONLINE DELIVERY =====")
print(delivery_analysis)


# 5. Average cost
query5 = """
SELECT City,
       ROUND(AVG(Average_Cost_for_Two), 2) AS Average_Cost
FROM restaurants
GROUP BY City
ORDER BY Average_Cost DESC;
"""

cost_analysis = pd.read_sql(query5, connection)

print("\n===== AVERAGE COST BY CITY =====")
print(cost_analysis)


connection.close()

print("\n===== REPORT COMPLETED =====")
