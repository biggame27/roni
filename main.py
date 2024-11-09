import streamlit as st

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime

data = pd.read_csv("april_2024.csv", delimiter=',')
df = pd.DataFrame(data)
# , "may_2024.csv", "june_2024.csv", "july_2024.csv", "august_2024.csv", "september_2024.csv", "october_2024.csv"

#"June",
option = st.selectbox(
    "Choose month to analyze! ",
    ("All Time", "April", "May", "June", "July", "August", "September", "October"),
    index=None,
    placeholder="Select Time Frame..",
)
month_to_file = {"April" : 0, "May" : 1, "July": 2, "August": 3, "September": 4, "October": 5}
csv_files = ["april_2024.csv", "may_2024.csv", "july_2024.csv", "august_2024.csv", "september_2024.csv", "october_2024.csv"]

df = []
if option not in month_to_file:
    # Create an empty list to store DataFrames
    dfs = []

    # Loop through each file and read it into a DataFrame
    for file in csv_files:
        df = pd.read_csv(file)
        dfs.append(df)

    # Concatenate all DataFrames into a single DataFrame
    df = pd.concat(dfs, ignore_index=True)
else:
    df = pd.read_csv(csv_files[month_to_file[option]])

# day of the week
df["Sent Date"] = pd.to_datetime(df["Sent Date"])

# Add a new column with the day of the week
df["Day of Week"] = df["Sent Date"].dt.strftime("%A")
days = df["Day of Week"]
df["Hour"] = df["Sent Date"].dt.hour

# Classify time into time frames
def classify_time(hour):
    if 11 <= hour < 13:
        return "Lunch"
    elif 13 <= hour <= 18:
        return "Brunch"
    else:
        return "Dinner"

# Apply the classification function
df["Time Frame"] = df["Hour"].apply(classify_time)

def sales_per_day():
  day_counts = df["Day of Week"].value_counts()

  # Ensure the order of days is correct
  ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
  day_counts = day_counts[ordered_days]
  tmp = [day_counts["Monday"],day_counts["Tuesday"],day_counts["Wednesday"],day_counts["Thursday"],day_counts["Friday"],day_counts["Saturday"],day_counts["Sunday"]]
  print(tmp)
  ans = pd.DataFrame({
      "days": ordered_days,
      "sales": [day_counts["Monday"],day_counts["Tuesday"],day_counts["Wednesday"],day_counts["Thursday"],day_counts["Friday"],day_counts["Saturday"],day_counts["Sunday"]]
  })
  # Display bar chart in Streamlit
  st.title("Sales per day")
  st.bar_chart(ans, x="days", y="sales")


def time_of_day():
  days = df["Day of Week"]
  df["Hour"] = df["Sent Date"].dt.hour
  st.title("Most popular time during the day")
  hours = df["Hour"].value_counts()
  st.bar_chart(hours)


def purchases():
  df["Year-Month-Day"] = df["Sent Date"].dt.strftime("%Y-%m-%d")

  # Group by "Year-Month-Day" and count the number of orders (purchases) for each day
  purchases_per_day = df.groupby("Year-Month-Day").size().reset_index(name="Purchases")

  # Group by "Year-Month" to get the total number of purchases for each day within each month
  purchases_per_day_per_month = df.groupby([df["Sent Date"].dt.to_period("M"), "Year-Month-Day"]).size().reset_index(name="Purchases")

  # Display the number of purchases per day per month
  # print(purchases_per_day_per_month)
  if option not in month_to_file:
    st.title("Purchases every day since opening")
  else:
     st.title("Purchases on " + option)
  st.line_chart(purchases_per_day_per_month["Purchases"])

def items():
    # menu orders
    st.title("Check out the popular items!")
    menu = data["Parent Menu Selection"]
    orders = menu.value_counts()
    option2 = st.selectbox(
      "Choose food items to see!",
      ("Meats", "Toppings", "Drizzles", "Cheese", "Drink", "Noods"),
      index=None,
      placeholder="Select Food Type...",)
    if option2 != None:
      if option2 != "Noods":
        st.write(df.loc[df["Option Group Name"] == "Choose Your " + option2]["Modifier"].value_counts())
      else:
        st.write(df.loc[df["Option Group Name"] == "Noods"]["Modifier"].value_counts())

    


purchases()
sales_per_day()
time_of_day()
items()