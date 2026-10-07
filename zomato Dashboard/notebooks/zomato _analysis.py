import pandas as pd
from pathlib import Path

# Find project folder
project_folder = Path(__file__).resolve().parent.parent

# CSV location
csv_file = project_folder / "dataset" / "zomato.csv"

print("CSV file location:")
print(csv_file)

print("\nFile exists:", csv_file.exists())

# Read CSV
df = pd.read_csv(csv_file, sep="\t")

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

# =========================
# DATA CLEANING
# =========================

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

# Remove duplicates
df = df.drop_duplicates()

# Remove rows with missing important values
df = df.dropna(
    subset=["Restaurant_Name", "City", "Cuisines", "Rating"]
)

# Convert numeric columns
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df["Votes"] = pd.to_numeric(df["Votes"], errors="coerce")
df["Average_Cost_for_Two"] = pd.to_numeric(
    df["Average_Cost_for_Two"],
    errors="coerce"
)

print("\nAfter cleaning:")
print(df.shape)

print("\nCleaned data:")
print(df.head())
# =========================
# DATA ANALYSIS
# =========================

# 1. Top 10 restaurants by rating
print("\nTop 10 Restaurants by Rating:")

top_restaurants = df.sort_values(
    by="Rating",
    ascending=False
)[["Restaurant_Name", "City", "Rating", "Votes"]].head(10)

print(top_restaurants)


# 2. Average rating
average_rating = df["Rating"].mean()

print("\nAverage Restaurant Rating:")
print(round(average_rating, 2))


# 3. Most popular cuisines
print("\nMost Popular Cuisines:")

popular_cuisines = df["Cuisines"].value_counts().head(10)

print(popular_cuisines)


# 4. Restaurants by city
print("\nRestaurants by City:")

city_count = df["City"].value_counts()

print(city_count)


# 5. Average cost for two
average_cost = df["Average_Cost_for_Two"].mean()

print("\nAverage Cost for Two:")
print(round(average_cost, 2))


# 6. Online delivery
print("\nOnline Delivery:")
print(df["Online_Delivery"].value_counts())
# =========================
# DATA VISUALIZATION
# =========================

import matplotlib.pyplot as plt
import seaborn as sns

# 1. Restaurants by City
plt.figure(figsize=(10, 5))

city_count = df["City"].value_counts()

sns.barplot(
    x=city_count.index,
    y=city_count.values
)

plt.title("Number of Restaurants by City")
plt.xlabel("City")
plt.ylabel("Number of Restaurants")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 2. Rating Distribution
plt.figure(figsize=(8, 5))

sns.histplot(
    df["Rating"],
    bins=10,
    kde=True
)

plt.title("Restaurant Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of Restaurants")
plt.tight_layout()
plt.show()


# 3. Top 10 Cuisines
plt.figure(figsize=(10, 5))

cuisine_count = df["Cuisines"].value_counts().head(10)

sns.barplot(
    x=cuisine_count.values,
    y=cuisine_count.index
)

plt.title("Top 10 Popular Cuisines")
plt.xlabel("Number of Restaurants")
plt.ylabel("Cuisine")
plt.tight_layout()
plt.show()


# 4. Rating vs Votes
plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=df,
    x="Votes",
    y="Rating"
)

plt.title("Rating vs Votes")
plt.xlabel("Votes")
plt.ylabel("Rating")
plt.tight_layout()
plt.show()