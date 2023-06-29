import pandas as pd
import ast
from collections import Counter

# Load the data
df = pd.read_csv("applications.csv")
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date').sort_index()
df['UUIDs'] = df['UUIDs'].apply(ast.literal_eval)

# Create a directory to store output CSVs
import os
if not os.path.exists('output'):
    os.makedirs('output')

# Resample data by start of each week
weekly_data = df.resample('W')

# Calculate and save acceptance rate per week
weekly_acceptance_rate = weekly_data['Status'].apply(lambda x: (x == 'Accepted').sum() / x.count())
weekly_acceptance_rate.to_csv("output/weekly_acceptance_rate.csv")

# Calculate and save total accepted applications per week
weekly_accepted_applications = weekly_data['Status'].apply(lambda x: (x == 'Accepted').sum())
weekly_accepted_applications.to_csv("output/weekly_accepted_applications.csv")

# Expand UUIDs into separate rows
df_exploded = df.explode('UUIDs')

# Calculate and save most active users of all time
all_time_user_activity = df_exploded['UUIDs'].value_counts()
all_time_user_activity.to_frame('Tickets').reset_index().rename(columns={'index': 'UUID'}).to_csv('output/all_time_user_activity.csv', index=False)

# Get top 50 most active UUIDs
top_50_uuids = all_time_user_activity.index[:50]

# Filter the exploded dataframe to include only top 50 UUIDs
df_exploded = df_exploded[df_exploded['UUIDs'].isin(top_50_uuids)]

# Calculate and save ranking of users per week
weekly_user_data = df_exploded['UUIDs'].groupby([df_exploded['UUIDs'], pd.Grouper(freq='W')]).count().unstack().fillna(0)
weekly_user_data.to_csv("output/weekly_user_rankings.csv")

# Calculate and save how often Legundo was mentioned every month
monthly_data = df.resample('M')
monthly_legundo_mentions = monthly_data['Legundo Mentioned'].sum()
monthly_legundo_mentions.to_csv("output/monthly_legundo_mentions.csv")

# Calculate and save total applications per week
weekly_total_applications = weekly_data.size()
weekly_total_applications.to_csv("output/weekly_total_applications.csv")

# Calculate and save ranking of users per month
monthly_user_data = df_exploded['UUIDs'].groupby([df_exploded['UUIDs'], pd.Grouper(freq='M')]).count().unstack().fillna(0)
monthly_user_data.to_csv("output/monthly_user_rankings.csv")

# Calculate and save ranking of users per year
yearly_user_data = df_exploded['UUIDs'].groupby([df_exploded['UUIDs'], pd.Grouper(freq='Y')]).count().unstack().fillna(0)
yearly_user_data.to_csv("output/yearly_user_rankings.csv")

# Load dictionary
dictionary = pd.read_csv("dictionary.csv")
uuid_to_username = dictionary.set_index('UUID')['Username'].to_dict()

# Replace UUIDs with usernames in the CSV files
for filename in ['weekly_user_rankings.csv', 'monthly_user_rankings.csv', 'yearly_user_rankings.csv', 'all_time_user_activity.csv']:
    file_path = os.path.join('output', filename)
    df = pd.read_csv(file_path, index_col=0)
    df.index = df.index.to_series().replace(uuid_to_username)
    df.to_csv(file_path)
