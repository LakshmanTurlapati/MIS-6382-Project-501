import pickle
import pandas as pd
import matplotlib.pyplot as plt

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

# Convert the 'price' and 'average_revenue' columns to numeric (float) types
df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Converts invalid parsing to NaN
df['average_revenue'] = pd.to_numeric(df['average_revenue'], errors='coerce')  # Converts invalid parsing to NaN

# Display the DataFrame to verify it loaded correctly and the conversion worked
print(df.head())

# Write the loaded objects to a new CSV file
with open('lodging_data.csv', 'w') as f:
    # Write the header
    f.write("unique_id,date,name,category,type,rating,price,average_revenue\n")
    # Write each object's data using its __str__ method
    for lodging in objects:
        f.write(str(lodging) + "\n")


# --- Data Visualization ---

# Example Visualization 1: Bar chart for Lodging Categories vs Average Revenue
df.groupby('category')['average_revenue'].sum().plot(kind='bar', color='skyblue')
plt.title('Total Average Revenue by Lodging Category')
plt.xlabel('Lodging Category')
plt.ylabel('Average Revenue (USD)')
plt.xticks(rotation=45)
plt.tight_layout()  # Adjusts plot to prevent label cutoff
plt.show()

# Example Visualization 2: Pie chart for the proportion of Lodging Types
df['type'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'lightcoral'])
plt.title('Proportion of Lodging Types (Travel vs Vacation)')
plt.ylabel('')  # Remove y-label for aesthetics
plt.tight_layout()
plt.show()

# Example Visualization 3: Scatter plot for Price vs Average Revenue
plt.scatter(df['price'], df['average_revenue'], color='purple')
plt.title('Price vs Average Revenue')
plt.xlabel('Price (USD)')
plt.ylabel('Average Revenue (USD)')
plt.tight_layout()
plt.show()