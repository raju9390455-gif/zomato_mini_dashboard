from flask import Flask, render_template, Response
from pathlib import Path
import pandas as pd
import csv
import io
import os

app = Flask(__name__)

# ==========================================
# PROJECT PATH
# ==========================================

# app.py is inside:
# zomato Dashboard/dashboard/app.py

# So we go one level up to "zomato Dashboard"
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Dataset location
csv_file = PROJECT_DIR / "dataset" / "zomato.csv"


# ==========================================
# READ DATA
# ==========================================

def get_dataframe():

    if not csv_file.exists():
        raise FileNotFoundError(
            f"Dataset not found: {csv_file}"
        )

    # Your CSV is tab-separated
    try:
        df = pd.read_csv(csv_file, sep="\t")

        # If only one column was detected,
        # try normal comma-separated CSV
        if len(df.columns) == 1:
            df = pd.read_csv(csv_file)

    except Exception:
        df = pd.read_csv(csv_file)

    # Convert numeric columns
    df["Rating"] = pd.to_numeric(
        df["Rating"],
        errors="coerce"
    )

    df["Votes"] = pd.to_numeric(
        df["Votes"],
        errors="coerce"
    )

    df["Average_Cost_for_Two"] = pd.to_numeric(
        df["Average_Cost_for_Two"],
        errors="coerce"
    )

    return df


# ==========================================
# DASHBOARD DATA
# ==========================================

def get_data():

    df = get_dataframe()

    # Restaurants by city
    city_data = (
        df.groupby("City")
        .size()
        .reset_index(name="Restaurant_Count")
        .sort_values(
            "Restaurant_Count",
            ascending=False
        )
        .to_dict("records")
    )

    # Top 10 restaurants
    top_restaurants = (
        df.sort_values(
            ["Rating", "Votes"],
            ascending=[False, False]
        )
        .head(10)
        .to_dict("records")
    )

    # All restaurants
    all_restaurants = df.to_dict("records")

    # Online delivery
    delivery_data = (
        df.groupby("Online_Delivery")
        .size()
        .reset_index(name="Restaurant_Count")
        .to_dict("records")
    )

    # Average rating by city
    rating_data = (
        df.groupby("City")["Rating"]
        .mean()
        .round(2)
        .reset_index(name="Average_Rating")
        .sort_values(
            "Average_Rating",
            ascending=False
        )
        .to_dict("records")
    )

    # Average cost by city
    cost_data = (
        df.groupby("City")["Average_Cost_for_Two"]
        .mean()
        .round(2)
        .reset_index(name="Average_Cost")
        .sort_values(
            "Average_Cost",
            ascending=False
        )
        .to_dict("records")
    )

    # KPIs
    total_restaurants = len(df)

    total_cities = df["City"].nunique()

    average_rating = round(
        df["Rating"].mean(),
        2
    )

    average_cost = round(
        df["Average_Cost_for_Two"].mean(),
        2
    )

    return (
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
    )


# ==========================================
# HOME PAGE
# ==========================================

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


# ==========================================
# EXPORT CSV
# ==========================================

@app.route("/export")
def export_data():

    df = get_dataframe()

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow(df.columns)

    writer.writerows(
        df.values.tolist()
    )

    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )

    response.headers[
        "Content-Disposition"
    ] = (
        "attachment; "
        "filename=zomato_restaurants.csv"
    )

    return response


# ==========================================
# RUN APP
# ==========================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )