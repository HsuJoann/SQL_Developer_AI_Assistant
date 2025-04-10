from anthropic import Anthropic
from step1_read_task import read_file_content
from step2_catagorize_task import simple_classify
from step3_get_sql_ready import generate_sql
from step3_get_sql_ready import generate_prompt
from dotenv import load_dotenv
import os
import psycopg2
import xml.etree.ElementTree as ET
import csv
from io import StringIO


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


def save_task_results(task_in_hand, current_category, sql, xml_result, output_file):
    """
    Appends the task details and results to an existing XML file or creates a new one if it doesn't exist.
    
    Args:
        task_in_hand (str): The task description.
        current_category (str): The category of the task.
        sql (str): The generated SQL query.
        xml_result (str): The query result in XML format.
        output_file (str): The file path to save the results.
    """
    try:
        # Check if the file exists
        if os.path.exists(output_file):
            # Parse the existing XML file
            tree = ET.parse(output_file)
            root = tree.getroot()
        else:
            # Create a new root element if the file doesn't exist
            root = ET.Element("TaskResultsCollection")
        
        # Create a new TaskResults element
        task_result = ET.SubElement(root, "TaskResults")
        
        # Add task_in_hand
        task_element = ET.SubElement(task_result, "TaskInHand")
        task_element.text = task_in_hand
        
        # Add current_category
        category_element = ET.SubElement(task_result, "CurrentCategory")
        category_element.text = current_category
        
        # Add SQL query
        sql_element = ET.SubElement(task_result, "SQLQuery")
        sql_element.text = sql
        
        # Add XML result
        result_element = ET.SubElement(task_result, "XMLResult")
        result_element.text = xml_result
        
        # Write the updated XML tree back to the file
        tree = ET.ElementTree(root)
        with open(output_file, "wb") as file:
            tree.write(file, encoding="utf-8", xml_declaration=True)
        
        print(f"Task results appended to {output_file}")
    
    except Exception as e:
        print(f"Failed to save task results: {e}")


def process_task_and_execute_sql():
    """
    Reads a task, generates SQL, executes it, and appends the results to an XML file.
    """
    # Define file paths
    folder_path = r"C:\Users\jingh\python_code_folder\SQL_developer_AI_assistant"
    task_path = os.path.join(folder_path, "New_task.txt")
    output_file = os.path.join(folder_path, "TaskResults.xml")

    # Read the task description
    task_in_hand = read_file_content(task_path)

    # Classify the task into a category
    current_category = simple_classify(task_in_hand)

    # Read the example file corresponding to the category
    example_path = os.path.join(folder_path, f"{current_category}.txt")
    example = read_file_content(example_path)

    # Generate the prompt
    prompt = generate_prompt(example, task_in_hand)

    # Generate the SQL query
    sql = generate_sql(prompt)

    # Execute the SQL query and get results in XML and CSV formats
    xml_result, csv_result = query_to_xml_and_csv(sql)
    
    # Append the task results to the XML file
    save_task_results(task_in_hand, current_category, sql, xml_result, output_file)


if __name__ == "__main__":
    process_task_and_execute_sql()