# Import required modules and libraries
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- Classes Definitions ---
class Lodging:
    def __init__(self, date, name, category, type, rating, price, average_revenue):
        self.unique_id = id(self)
        self.date = date
        self.name = name
        self.category = category
        self.type = type
        self.rating = rating
        self.price = price
        self.average_revenue = average_revenue

    def __str__(self):
        return f"{self.unique_id},{self.date},{self.name},{self.category},{self.type},{self.rating},{self.price},{self.average_revenue}"

class Travel(Lodging):
    def __init__(self, date, name, category, rating, price, average_revenue):
        super().__init__(date, name, category, "Travel", rating, price, average_revenue)

class Vacation(Lodging):
    def __init__(self, date, name, category, rating, price, average_revenue):
        super().__init__(date, name, category, "Vacation", rating, price, average_revenue)

class HotelRoom(Travel):
    def __init__(self, date, name, rating, price, average_revenue):
        super().__init__(date, name, "HotelRoom", rating, price, average_revenue)

class Cottage(Vacation):
    def __init__(self, date, name, rating, price, average_revenue):
        super().__init__(date, name, "Cottage", rating, price, average_revenue)

class BeachHouse(Vacation):
    def __init__(self, date, name, rating, price, average_revenue):
        super().__init__(date, name, "BeachHouse", rating, price, average_revenue)

# --- Data Loading ---
with open('Lodgingpkl638250102.dat', 'rb') as file:
    objects = pickle.load(file)

# --- Data Preparation ---
data = {
    'unique_id': [obj.unique_id for obj in objects],
    'date': [obj.date for obj in objects],
    'name': [obj.name for obj in objects],
    'category': [obj.category for obj in objects],
    'type': [obj.type for obj in objects],
    'rating': [obj.rating for obj in objects],
    'price': [obj.price for obj in objects],
    'average_revenue': [obj.average_revenue for obj in objects]
}

df = pd.DataFrame(data)

# Convert 'date' to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Convert numerical columns to numeric types and handle missing values
numerical_cols = ['price', 'average_revenue', 'rating']
for col in numerical_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(df[col].median())

# Handle missing values for categorical variables
categorical_cols = ['date', 'name', 'category', 'type']
for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# Save the cleaned DataFrame to a new CSV file
df.to_csv('lodging_data_cleaned.csv', index=False)

# --- Visualizations ---

sns.set(style="whitegrid")

# 1. Bar Chart: Total Average Revenue by Lodging Category
plt.figure(figsize=(8, 6))
category_revenue = df.groupby('category')['average_revenue'].sum().sort_values(ascending=False)
category_revenue.plot(kind='bar', color='skyblue')
plt.title('Figure 1: Total Average Revenue by Lodging Category')
plt.xlabel('Lodging Category')
plt.ylabel('Total Average Revenue (USD)')
plt.tight_layout()
plt.savefig('BarChart.pdf')
plt.show()

# 2. Boxplot: Distribution of Prices by Lodging Type
plt.figure(figsize=(8, 8))
sns.boxplot(x='type', y='price', data=df, hue='type', palette=['skyblue', 'dimgrey'], dodge=False, legend=False)
plt.title('Figure 2: Boxplot - Price Distribution by Lodging Type')
plt.xlabel('Lodging Type')
plt.ylabel('Price (USD)')
plt.tight_layout()
plt.savefig('Boxplot.pdf')
plt.show()

# 3. Line Plot: Average Revenue Over Time
plt.figure(figsize=(10, 6))
df_sorted = df.sort_values('date')
sns.lineplot(x='date', y='average_revenue', data=df_sorted, marker='o', color='dimgrey', markersize=3)
plt.axvspan(pd.Timestamp('2022-10-01'), pd.Timestamp('2022-12-31'), color='yellow', alpha=0.2, label='Holiday Season')
plt.title('Figure 3: Line Plot - Average Revenue Over Time')
plt.xlabel('Date')
plt.ylabel('Average Revenue (USD)')
plt.tight_layout()
plt.savefig('LinePlot.pdf')
plt.show()

# 4. Scatter plot: Average Revenue vs. Price
df['price_jittered'] = df['price'] + np.random.uniform(-0.5, 0.5, size=len(df))
df['average_revenue_jittered'] = df['average_revenue'] + np.random.uniform(-500, 500, size=len(df))
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="price_jittered", y="average_revenue_jittered", hue="type", palette="deep", alpha=0.7)
plt.title("Average Revenue vs. Price by Lodging Type")
plt.xlabel("Price (USD)")
plt.ylabel("Average Revenue (USD)")
plt.tight_layout()
plt.savefig('Scatter_AverageRevenue_vs_Price.pdf')
plt.show()

# 5. Histogram: Distribution of Ratings
plt.figure(figsize=(8, 6))
counts, edges = np.histogram(df['rating'], bins=np.arange(1, 7))
plt.bar(edges[:-1], counts, width=1, color='navy', edgecolor='white', align='edge')
plt.title('Figure 5: Histogram - Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('Histogram.pdf')
plt.show()

# 6. Pie Chart: Proportion of Lodging Types
plt.figure(figsize=(8, 6))
df['type'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['skyblue', 'dimgrey'])
plt.title('Figure 6: Pie Chart - Proportion of Lodging Types')
plt.tight_layout()
plt.savefig('PieChart.pdf')
plt.show()

# 7. Heatmap: Lodging Type vs. Rating
df['rating'] = df['rating'].astype(str)
pivot_table = df.pivot_table(index='type', columns='rating', values='unique_id', aggfunc='count', fill_value=0)
plt.figure(figsize=(10, 6))
sns.heatmap(pivot_table, annot=True, cmap='Blues', fmt='d')
plt.title('Figure 7: Heat Map - Lodging Type vs. Rating')
plt.xlabel('Rating')
plt.ylabel('Lodging Type')
plt.tight_layout()
plt.savefig('Heatmap.pdf')
plt.show()