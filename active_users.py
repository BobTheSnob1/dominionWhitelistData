import pandas as pd
import numpy as np
import ast
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
from matplotlib.ticker import MaxNLocator
from matplotlib.dates import YearLocator, MonthLocator, WeekdayLocator, DateFormatter

# Load your data into a pandas DataFrame
df = pd.read_csv('applications.csv')

# Convert the 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Create a separate DataFrame for the accepted applications
df_accepted = df[df['Status'] == 'Accepted']

# Add 'Month' and 'Week' columns to the 'df_accepted' DataFrame as well
pd.options.mode.chained_assignment = None  # default='warn'
df_accepted['Month'] = df_accepted['Date'].dt.to_period('M')
df_accepted['Week'] = df_accepted['Date'].dt.to_period('W')

# Convert string representation of list to actual list
df['Users'] = df['Users'].apply(ast.literal_eval)
# Flatten the list of lists to get each individual user
all_users = [user for sublist in df['Users'].tolist() for user in sublist]
# Count the occurrence of each user
user_counts = pd.Series(all_users).value_counts()

# Flatten the list of lists to get each individual user
all_users = [user for sublist in df['Users'].tolist() for user in sublist]
# Count the occurrence of each user
user_counts = pd.Series(all_users).value_counts()

# Convert to DataFrame
df_user_counts = user_counts.reset_index()
df_user_counts.columns = ['User', 'Count']

# Write to CSV
df_user_counts.to_csv("user_counts.csv", index=False)