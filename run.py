import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Establish connection to your database
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=TRISQL01\SQL2019;'
    'DATABASE=kaizenDB;'
    'UID=Kaizen;'
    'PWD=k@1Z3n@sql;'
)

# SQL Query to fetch the last 7 days of downtime data
query = """
SELECT mo.EXTWST_0 AS 'Line Number', 
       SUM(sl.DURATION) AS Duration
FROM kaizenDB.dbo.SHIFT_LOG sl
INNER JOIN x3.PROD.MFGHEAD mh ON mh.MFGNUM_0 = sl.WORK_TICKET_NO COLLATE DATABASE_DEFAULT
INNER JOIN x3.PROD.MFGOPE mo ON mo.MFGNUM_0 = mh.MFGNUM_0
WHERE sl.ACTIVITY_CODE = 'DOWN'
AND sl.TRANSACTION_DATE >= DATEADD(DAY, -5, GETDATE())  -- Changed to last 5 days
GROUP BY mo.EXTWST_0;
"""

# Fetch the data from the database
df = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Sort data by Line Number to make plotting easier
df = df.sort_values('Line Number')

# Plotting the stacked bar chart
# Group the data by 'Line Number' and sum the durations for each line
lines = df['Line Number']
durations = df['Duration']

# Create a stacked bar chart with a more distinct color palette
fig, ax = plt.subplots(figsize=(12, 8))

# Use the 'tab20' colormap for distinct colors. If there are more than 20 bars, colors will still repeat.
colors = plt.cm.tab20(np.linspace(0, 1, len(df)))  # Assign a different color for each row in df

# Plot the bars for each line with a unique color
bars = ax.bar(df['Line Number'], df['Duration'], color=colors)

# Add labels and title with enhanced styling
ax.set_xlabel('Line Number', fontsize=14, fontweight='bold')
ax.set_ylabel('Downtime (Hours)', fontsize=14, fontweight='bold')
ax.set_title('Downtime per Line (Last 7 Days)', fontsize=16, fontweight='bold', pad=20)

# Add gridlines to make the chart look fancier and clearer
ax.grid(True, which='both', axis='y', linestyle='--', linewidth=0.7, alpha=0.7)

# Improve the xticks styling for clarity
plt.xticks(rotation=45, ha='right', fontsize=12, fontweight='medium')

# Adjust the layout and ensure it doesn't overlap with other elements
plt.tight_layout()

# Show the plot without hover functionality
plt.show()
# Generate a larger list of random colors if you have many bars
colors = plt.cm.get_cmap('tab20b', len(df))  # 'tab20b' gives even more distinct colors

# Assign colors to bars
bars = ax.bar(df['Line Number'], df['Duration'], color=[colors(i) for i in range(len(df))])
