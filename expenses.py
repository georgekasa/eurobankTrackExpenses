import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt


def pie_chart():
# Pie chart
    plt.figure(figsize=(8, 8))
    colors = plt.cm.Paired(np.linspace(0, 1, len(spending_by_merchant)))
    spending_by_merchant.plot.pie(
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        label='',
        wedgeprops={"edgecolor": "black"}
    )
    plt.title("Spending Breakdown by Merchant")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()

# Load the CSV file
file_path = r"/home/georgekasa/Documents/python/may.csv"
df = pd.read_csv(file_path, encoding="utf-8")

# Clean column names
df.rename(columns=lambda x: x.strip(), inplace=True)

# Convert 'price' column to absolute numeric values
df["price"] = np.abs(pd.to_numeric(df["price"], errors="coerce"))

# Normalize merchant details
def normalize_details(detail):
    detail = str(detail).strip().upper()
    detail = re.sub(r'\s+', ' ', detail)
    detail = detail.replace('GLYFA', 'GLIFA')
    return detail

df["normalized_details"] = df["details"].fillna("").apply(normalize_details)

# Define merchant grouping rules
merchant_groups = {
    "Amazon": ["AMAZON", "AMZN"],
    "Shell": ["SHELL", "ERMIS AE SARON"],
    "Supermarket": ["AB", "VASILOPOULOS", "SKLAVENITIS", "LIDL", "MY MARKET", "MASOUTIS", "KREOΠOΛI LAGON"],
    "McDonald's": ["MC DONALD", "MCDONALD"],
    "Coffee": ["COFFEE ISLAND", "COFFEE ISLANDS", "DUENDE"],
    "Clothes": ["ZARA", "H&M", "BERSHKA", "PULL AND BEAR", "STRADIVARIUS", "MANGO", "about you", "adidas", "nike", "puma", "MARTIN", "OXFORD"],
    "Unnecessary Purchases": ["NOMONO", "PERIPTER"],
}

# Function to assign a general merchant name
def categorize_merchant(detail):
    for merchant, keywords in merchant_groups.items():
        if any(keyword in detail for keyword in keywords):
            return merchant
    return detail  # Keep original if no match

df["general_merchant"] = df["normalized_details"].apply(categorize_merchant)

# Group spending
spending_by_merchant = df.groupby("general_merchant")["price"].sum().sort_values(ascending=False)

# Display categorized spending
print("\n🔹 Total Spent per Merchant Category:")
for merchant, total in spending_by_merchant.items():
    print(f"Total spent at {merchant}: €{total:.2f}")

# Calculate purchases under €5
under_5 = df[df["price"] < 5]["price"].sum()
print(f"\n🔸 Total spent on purchases under €5: €{under_5:.2f}")

# Budget calculation
salary = 1750
revolut = 400
mother = 150
expenses = spending_by_merchant.sum()
remaining_balance = salary - (revolut + mother + expenses)

print(f"\n💰 Total expenses: €{expenses:.2f}")
print(f"💵 Remaining balance after expenses: €{remaining_balance:.2f}")

pie_chart()
