import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Base class Lodging
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

# Subclasses for Travel and Vacation
class Travel(Lodging):
    def __init__(self, date, name, category, rating, price, average_revenue):
        super().__init__(date, name, category, "Travel", rating, price, average_revenue)

class Vacation(Lodging):
    def __init__(self, date, name, category, rating, price, average_revenue):
        super().__init__(date, name, category, "Vacation", rating, price, average_revenue)

# Additional subclasses for HotelRoom, Cottage, BeachHouse
class HotelRoom(Travel):
    def __init__(self, date, name, rating, price, average_revenue):
        super().__init__(date, name, "HotelRoom", rating, price, average_revenue)

class Cottage(Vacation):
    def __init__(self, date, name, rating, price, average_revenue):
        super().__init__(date, name, "Cottage", rating, price, average_revenue)

class BeachHouse(Vacation):
    def __init__(self, date, name, rating, price, average_revenue):
        super().__init__(date, name, "BeachHouse", rating, price, average_revenue)

# Load the .dat file (which contains pickled objects)
with open('Lodgingpkl638250102.dat', 'rb') as file:
    objects = pickle.load(file)

# Convert the list of objects into a pandas DataFrame
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

# Convert numerical columns to numeric types
numerical_cols = ['price', 'average_revenue', 'rating']
for col in numerical_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Convert the 'rating' column to integers after ensuring it's numeric
df['rating'] = df['rating'].fillna(0).astype(int)

# Handle missing values
## For numerical variables: fill missing values with the median
for col in numerical_cols:
    median_value = df[col].median()
    df[col].fillna(median_value, inplace=True)

## For categorical variables: fill missing values with the mode
categorical_cols = ['date', 'name', 'category', 'type']
for col in categorical_cols:
    mode_value = df[col].mode()[0]
    df[col].fillna(mode_value, inplace=True)

# Display the DataFrame to verify it loaded correctly
print(df.head())

# Save the cleaned DataFrame to a new CSV file
df.to_csv('lodging_data.csv', index=False)

# --- Data Visualization ---

# Setting a seaborn style for better aesthetics
sns.set(style="whitegrid")

# 1. Bar Chart: Total Average Revenue by Lodging Category
plt.figure(figsize=(8, 6))
category_revenue = df.groupby('category')['average_revenue'].sum().sort_values(ascending=False)
category_revenue.plot(kind='bar', color='navy')
for index, value in enumerate(category_revenue):
    plt.text(index, value, str(round(value)), ha='center', va='bottom')
plt.title('Figure 1: Total Average Revenue by Lodging Category')
plt.xlabel('Lodging Category')
plt.ylabel('Total Average Revenue (USD)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('BarChart.pdf')
plt.show()

# 2. Boxplot: Distribution of Prices by Lodging Type
plt.figure(figsize=(8, 8))
sns.boxplot(x='type', y='price', data=df, hue='type', dodge=False, palette='Set2', legend=False)
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
plt.title('Figure 3: Line Plot - Average Revenue Over Time')
plt.axvspan(pd.Timestamp('2022-10-01'), pd.Timestamp('2022-12-31'), color='yellow', alpha=0.2, label='Holiday Season')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Average Revenue (USD)', fontsize=12)
plt.tight_layout()
plt.savefig('lineplot.pdf')
plt.show()

# Scatter Plot: Rating vs. Price
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="price", y="rating", hue="type", palette="deep", alpha=0.7)
plt.title("Rating vs. Price by Lodging Type", fontsize=16)
plt.xlabel("Price (USD)", fontsize=12)
plt.ylabel("Rating", fontsize=12)
plt.grid(alpha=0.3)
plt.legend(title='Lodging Type')
plt.tight_layout()
plt.savefig('Scatter.pdf')
plt.show()

# 5. Histogram: Distribution of Ratings
plt.figure(figsize=(8, 6))
counts, edges = np.histogram(df['rating'], bins=np.arange(1, 7))  # Adjust bins as per your data
plt.bar(edges[:-1], counts, width=1, color='navy', edgecolor='white', align='edge')
for count, edge in zip(counts, edges[:-1]):
    plt.text(edge + 0.5, count + 1, str(count), ha='center', va='bottom')
plt.title('Figure 5: Histogram - Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.xticks([1, 2, 3, 4, 5])  # Set ticks at the center of the bars
plt.tight_layout()
plt.savefig('Histogram.pdf')
plt.show()

# 6. Pie Chart: Proportion of Lodging Types
plt.figure(figsize=(8, 6))
df['type'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['skyblue', 'dimgrey'])
plt.title('Figure 6: Pie Chart - Proportion of Lodging Types')
plt.ylabel('')
plt.tight_layout()
plt.savefig('Pie.pdf')
plt.show()

# 7. Heat Map: Correlation Matrix
plt.figure(figsize=(8, 6))
corr = df[numerical_cols].corr()
sns.heatmap(corr, annot=True, cmap='cividis', fmt='.2f')
plt.title('Figure 7: Heat Map - Correlation Matrix of Numerical Features')
plt.tight_layout()
plt.savefig('Heatmap.pdf')
plt.show()