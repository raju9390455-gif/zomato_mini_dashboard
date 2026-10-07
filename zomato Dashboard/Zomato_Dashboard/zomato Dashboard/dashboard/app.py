from flask import Flask, render_template, Response
import mysql.connector
import csv
import io


app = Flask(__name__)


def get_data():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ram455@#",
        database="zomato_db"
    )

    cursor = connection.cursor(dictionary=True)

    # =========================================
    # 1. RESTAURANTS BY CITY
    # =========================================

    cursor.execute("""
        SELECT City, COUNT(*) AS Restaurant_Count
        FROM restaurants
        GROUP BY City
        ORDER BY Restaurant_Count DESC
    """)

    city_data = cursor.fetchall()


    # =========================================
    # 2. TOP RATED RESTAURANTS
    # =========================================

    cursor.execute("""
        SELECT Restaurant_Name, City, Rating, Votes
        FROM restaurants
        ORDER BY Rating DESC, Votes DESC
        LIMIT 10
    """)

    top_restaurants = cursor.fetchall()


    # =========================================
    # 3. ALL RESTAURANTS
    # =========================================

    cursor.execute("""
        SELECT
            Restaurant_ID,
            Restaurant_Name,
            City,
            Location,
            Cuisines,
            Rating,
            Votes,
            Average_Cost_for_Two,
            Online_Delivery,
            Table_Booking
        FROM restaurants
        ORDER BY Rating DESC, Votes DESC
    """)

    all_restaurants = cursor.fetchall()


    # =========================================
    # 4. ONLINE DELIVERY
    # =========================================

    cursor.execute("""
        SELECT Online_Delivery, COUNT(*) AS Restaurant_Count
        FROM restaurants
        GROUP BY Online_Delivery
    """)

    delivery_data = cursor.fetchall()


    # =========================================
    # 5. AVERAGE RATING BY CITY
    # =========================================

    cursor.execute("""
        SELECT City,
               ROUND(AVG(Rating), 2) AS Average_Rating
        FROM restaurants
        GROUP BY City
        ORDER BY Average_Rating DESC
    """)

    rating_data = cursor.fetchall()


    # =========================================
    # 6. AVERAGE COST BY CITY
    # =========================================

    cursor.execute("""
        SELECT City,
               ROUND(AVG(Average_Cost_for_Two), 2) AS Average_Cost
        FROM restaurants
        GROUP BY City
        ORDER BY Average_Cost DESC
    """)

    cost_data = cursor.fetchall()


    # =========================================
    # 7. KPI - TOTAL RESTAURANTS
    # =========================================

    cursor.execute("""
        SELECT COUNT(*) AS Total_Restaurants
        FROM restaurants
    """)

    total_restaurants = cursor.fetchone()["Total_Restaurants"]


    # =========================================
    # 8. KPI - TOTAL CITIES
    # =========================================

    cursor.execute("""
        SELECT COUNT(DISTINCT City) AS Total_Cities
        FROM restaurants
    """)

    total_cities = cursor.fetchone()["Total_Cities"]


    # =========================================
    # 9. KPI - OVERALL AVERAGE RATING
    # =========================================

    cursor.execute("""
        SELECT ROUND(AVG(Rating), 2) AS Average_Rating
        FROM restaurants
    """)

    average_rating = cursor.fetchone()["Average_Rating"]


    # =========================================
    # 10. KPI - OVERALL AVERAGE COST
    # =========================================

    cursor.execute("""
        SELECT ROUND(AVG(Average_Cost_for_Two), 2) AS Average_Cost
        FROM restaurants
    """)

    average_cost = cursor.fetchone()["Average_Cost"]


    # =========================================
    # CLOSE DATABASE
    # =========================================

    cursor.close()
    connection.close()


    # =========================================
    # CONVERT DATABASE VALUES
    # =========================================

    for row in city_data:
        row["Restaurant_Count"] = int(row["Restaurant_Count"])


    for row in delivery_data:
        row["Restaurant_Count"] = int(row["Restaurant_Count"])


    for row in rating_data:
        row["Average_Rating"] = float(row["Average_Rating"])


    for row in cost_data:
        row["Average_Cost"] = float(row["Average_Cost"])


    for row in top_restaurants:

        row["Rating"] = float(row["Rating"])

        row["Votes"] = int(row["Votes"])


    # =========================================
    # CONVERT ALL RESTAURANT VALUES
    # =========================================

    for row in all_restaurants:

        row["Rating"] = float(row["Rating"])

        row["Votes"] = int(row["Votes"])

        row["Average_Cost_for_Two"] = float(
            row["Average_Cost_for_Two"]
        )


    # =========================================
    # RETURN ALL DATA
    # =========================================

    return (
        city_data,
        top_restaurants,
        all_restaurants,
        delivery_data,
        rating_data,
        cost_data,
        total_restaurants,
        total_cities,
        float(average_rating),
        float(average_cost)
    )


# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():

    (
        city_data,
        top_restaurants,
        all_restaurants,
        delivery_data,
        rating_data,
        cost_data,
        total_restaurants,
        total_cities,
        average_rating,
        average_cost
    ) = get_data()


    return render_template(
        "index.html",

        city_data=city_data,

        top_restaurants=top_restaurants,

        all_restaurants=all_restaurants,

        delivery_data=delivery_data,

        rating_data=rating_data,

        cost_data=cost_data,

        total_restaurants=total_restaurants,

        total_cities=total_cities,

        average_rating=average_rating,

        average_cost=average_cost
    )


# =========================================
# EXPORT RESTAURANT DATA
# =========================================

@app.route("/export")
def export_data():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ram455@#",
        database="zomato_db"
    )

    cursor = connection.cursor()


    cursor.execute("""
        SELECT
            Restaurant_ID,
            Restaurant_Name,
            City,
            Location,
            Cuisines,
            Rating,
            Votes,
            Average_Cost_for_Two,
            Online_Delivery,
            Table_Booking
        FROM restaurants
    """)


    rows = cursor.fetchall()


    columns = [
        "Restaurant_ID",
        "Restaurant_Name",
        "City",
        "Location",
        "Cuisines",
        "Rating",
        "Votes",
        "Average_Cost_for_Two",
        "Online_Delivery",
        "Table_Booking"
    ]


    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow(columns)

    writer.writerows(rows)


    cursor.close()

    connection.close()


    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )


    response.headers["Content-Disposition"] = (
        "attachment; filename=zomato_restaurants.csv"
    )


    return response


# =========================================
# RUN FLASK
# =========================================

if __name__ == "__main__":
    app.run(debug=True)