import psycopg2
from dotenv import load_dotenv
import os
import xml.etree.ElementTree as ET
import csv
from io import StringIO

# Load environment variables from a .env file
load_dotenv()

def query_to_xml_and_csv(select_query):
    """
    Executes a SELECT query on the PostgreSQL database and returns the result in both XML and CSV formats.
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
        
        # Execute the SELECT query
        cursor.execute(select_query)
        columns = [desc[0] for desc in cursor.description]  # Get column names
        rows = cursor.fetchall()  # Fetch all rows
        
        # Create an XML tree
        root = ET.Element("Results")
        for row in rows:
            row_element = ET.SubElement(root, "Row")
            for col_name, col_value in zip(columns, row):
                col_element = ET.SubElement(row_element, col_name)
                col_element.text = str(col_value) if col_value is not None else "NULL"
        
        # Convert the XML tree to a string
        xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")
        
        # Create a CSV string
        csv_output = StringIO()
        csv_writer = csv.writer(csv_output)
        csv_writer.writerow(columns)  # Write header
        csv_writer.writerows(rows)    # Write rows
        csv_string = csv_output.getvalue()
        csv_output.close()
        
        return xml_string, csv_string
    
    except Exception as e:
        print(f"Failed to execute query: {e}")
        return None, None
    
    finally:
        # Close the connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__": 
    # Query to list all tables
    select_query = """
    SELECT 
    od.order_detail_id,
    od.order_id,
    od.product_id,
    p.product_name,
    od.quantity,
    od.price,
    (od.quantity * od.price) AS total_price,
    oh.order_date,
    oh.total_amount
    FROM 
    order_detail od
    JOIN 
    order_head oh ON od.order_id = oh.order_id
    JOIN 
    product p ON od.product_id = p.product_id
    WHERE 
    oh.customer_id = 5;
    """
    
    # Execute the query and get the result in XML and CSV formats
    xml_result, csv_result = query_to_xml_and_csv(select_query)
    
    if xml_result:
        print("Query Result in XML Format:")
        print(xml_result)
    
    if csv_result:
        print("\nQuery Result in CSV Format:")
        print(csv_result)