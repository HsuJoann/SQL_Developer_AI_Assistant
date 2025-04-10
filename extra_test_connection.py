import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

def execute_sql(sql_statement):
    """
    Executes a given SQL statement on the connected PostgreSQL database.
    """
    try:
        # Connect to the database using credentials from environment variables
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT", 5432)  # Default to port 5432 if not set
        )
        cursor = connection.cursor()
        
        # Execute the SQL statement
        cursor.execute(sql_statement)
        connection.commit()
        print("SQL executed successfully!")
    
    except Exception as e:
        print(f"Failed to execute SQL: {e}")
    
    finally:
        # Close the connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    # Example SQL statement to create the customer table
    sql_command = """

    UPDATE order_head
    SET order_date = 
    TIMESTAMP '2025-01-01' + 
    (RANDOM() * INTERVAL '90 days');
    """
    
    # Execute the SQL statement
    execute_sql(sql_command)