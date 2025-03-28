import pyodbc

# Define DSN (Replace with your DSN name)
dsn_name = "PostgreSQL35W"

try:
    # Connect to PostgreSQL ODBC
    conn = pyodbc.connect(f"DSN={dsn_name};")
    cursor = conn.cursor()

    # Execute a test query
    cursor.execute("SELECT version();")
    row = cursor.fetchone()

    print("Connected to:", row[0])

    # Close the connection
    cursor.close()
    conn.close()

except Exception as e:
    print("Error:", e)
