import os
import psycopg2
import csv
from psycopg2 import sql

# --- Database Configuration ---
# Replace with your PostgreSQL connection details
# It's recommended to use environment variables for sensitive data
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "Welcometosangiro@123")
DB_NAME = "company_db"
TABLE_NAME = "employees"
CSV_FILE = "employees.csv"

def setup_database():
    """
    Connects to PostgreSQL, creates a new database, enables the pgvector extension,
    and creates a table for employee data.
    """
    conn = None
    try:
        # Connect to the default 'postgres' database to create a new database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if the database already exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        if not cursor.fetchone():
            print(f"Creating database: {DB_NAME}")
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        else:
            print(f"Database '{DB_NAME}' already exists.")

        cursor.close()
        conn.close()

        # Connect to the newly created database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        cursor = conn.cursor()

        # Enable the pgvector extension
        print("Enabling pgvector extension...")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        conn.commit()
        print("pgvector extension enabled.")

        # Create the employees table
        print(f"Creating table: {TABLE_NAME}")
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            position VARCHAR(255) NOT NULL,
            salary INTEGER NOT NULL
        );
        """)
        conn.commit()
        print("Table created successfully.")

    except psycopg2.Error as e:
        print(f"Error setting up database: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def ingest_data_from_csv():
    """
    Ingests data from a CSV file into the specified PostgreSQL table.
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        cursor = conn.cursor()

        with open(CSV_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                cursor.execute(
                    f"INSERT INTO {TABLE_NAME} (id, name, position, salary) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING",
                    row
                )
        conn.commit()
        print(f"Data from '{CSV_FILE}' ingested successfully into '{TABLE_NAME}'.")

    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILE}' was not found.")
    except psycopg2.Error as e:
        print(f"Error ingesting data: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def validate_data():
    """
    Connects to the database and retrieves all records from the employees table.
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        cursor = conn.cursor()

        print("\n--- Validating Data in 'employees' table ---")
        cursor.execute(f"SELECT * FROM {TABLE_NAME};")
        rows = cursor.fetchall()

        if not rows:
            print("No data found in the table.")
        else:
            # Get column names from cursor description
            colnames = [desc[0] for desc in cursor.description]
            print(f"Columns: {', '.join(colnames)}")
            print("-" * 40)
            for row in rows:
                print(row)
        print("-" * 40)

    except psycopg2.Error as e:
        print(f"Error validating data: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database()
    ingest_data_from_csv()
    validate_data()
