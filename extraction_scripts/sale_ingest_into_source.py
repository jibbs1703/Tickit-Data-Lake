import sqlite3
import pandas as pd

# Full or relative path to your SQLite database file
db_path="C:/Users/ameen/OneDrive/Documents/github/Tickit-Data-Lake/data_source/tickit.sqlite3"
# Connect to the SQLite database
connection = sqlite3.connect(db_path)

# Create a cursor to execute SQL commands
cursor = connection.cursor()

# Example: Execute a query
query = "SELECT * FROM venue"
cursor.execute(query)

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# View Query Results as Pandas DataFrame
df = pd.read_sql_query(query, connection)
print(df.head)
print(df.shape)
df.to_csv("C:/Users/ameen/OneDrive/Documents/github/Tickit-Data-Lake/data_source/venue.csv", index=False)

# Close the connection when done
connection.close()