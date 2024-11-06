import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # For enhanced visualizations like heat maps

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
category_revenue.plot(kind='bar', color='skyblue')
plt.title('Figure 1: Bar Chart - Total Average Revenue by Lodging Category')
plt.xlabel('Lodging Category')
plt.ylabel('Total Average Revenue (USD)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Boxplot: Distribution of Prices by Lodging Type
plt.figure(figsize=(8, 6))
sns.boxplot(x='type', y='price', data=df, palette='pastel')
plt.title('Figure 2: Boxplot - Price Distribution by Lodging Type')
plt.xlabel('Lodging Type')
plt.ylabel('Price (USD)')
plt.tight_layout()
plt.show()

# 3. Line Plot: Average Revenue Over Time
plt.figure(figsize=(10, 6))
df_sorted = df.sort_values('date')
sns.lineplot(x='date', y='average_revenue', data=df_sorted, marker='o', color='green')
plt.title('Figure 3: Line Plot - Average Revenue Over Time')
plt.xlabel('Date')
plt.ylabel('Average Revenue (USD)')
plt.tight_layout()
plt.show()

# 4. Scatter Plot: Price vs Average Revenue
plt.figure(figsize=(8, 6))
plt.scatter(df['price'], df['average_revenue'], color='purple', alpha=0.7)
plt.title('Figure 4: Scatter Plot - Price vs Average Revenue')
plt.xlabel('Price (USD)')
plt.ylabel('Average Revenue (USD)')
plt.tight_layout()
plt.show()

# 5. Histogram: Distribution of Ratings
plt.figure(figsize=(8, 6))
df['rating'].hist(bins=10, color='orange', edgecolor='black')
plt.title('Figure 5: Histogram - Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# 6. Pie Chart: Proportion of Lodging Types
plt.figure(figsize=(8, 6))
df['type'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
plt.title('Figure 6: Pie Chart - Proportion of Lodging Types')
plt.ylabel('')
plt.tight_layout()
plt.show()

# 7. Heat Map: Correlation Matrix
plt.figure(figsize=(8, 6))
corr = df[numerical_cols].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Figure 7: Heat Map - Correlation Matrix of Numerical Features')
plt.tight_layout()
plt.show()