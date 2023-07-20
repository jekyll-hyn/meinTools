import streamlit as st
import csv
import random
from datetime import datetime, timedelta
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Generate random data
data = []
start_date = datetime(2023, 1, 1)
for i in range(30):
    date_str = start_date.strftime("%Y-%m-%d")
    hours = [random.randint(0, 1) for j in range(24)]
    data.append([date_str] + hours)
    start_date += timedelta(days=1)

# Write data to CSV file
file_path = os.path.dirname(os.path.abspath(__file__))
daypath = os.path.join(file_path, "dayhour.csv")

if not os.path.isfile(daypath):
    with open(daypath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["OpeDate"] + [f"H{i:02d}" for i in range(24)])
        for row in data:
            writer.writerow(row)

# Read data from CSV file
df = pd.read_csv(daypath)

# Group data by weekday
weekly_usage = df.iloc[:, 1:].groupby(df["OpeDate"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").weekday())).mean()

# Generate color map
cmap = plt.get_cmap("YlOrRd")

# Plot heatmap
fig, ax = plt.subplots(figsize=(8, 4))
im = ax.imshow(weekly_usage, cmap=cmap, aspect="auto")

# Set x-axis tick labels
ax.set_xticks(range(24))
ax.set_xticklabels([f"{i:02d}" for i in range(24)])

# Set y-axis tick labels
yticks = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
ax.set_yticks(np.arange(len(yticks)) + 0.5)
ax.set_yticklabels(yticks)

# Add grid lines
ax.grid(axis='y', which='both', color='white', linestyle='-', linewidth=2)

# Set labels and title
ax.set_xlabel("Hour")
ax.set_ylabel("Weekday")
ax.set_title("Weekday Usage Rate")

# Add colorbar
cbar = plt.colorbar(im)

# Show the plot
#plt.show()
st.write("# 手術室の曜日別稼働率")
st.pyplot(fig)
