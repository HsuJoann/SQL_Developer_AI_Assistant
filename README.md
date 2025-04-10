# SQL Developer AI Assistant

This project is an AI-powered assistant designed to help SQL developers automate the process of categorizing tasks, generating SQL queries, executing them, and saving the results in XML format.

## Project Structure

```
.env
customer_order_inquiry.txt
extra_select_and_save_result_in_xml.py
extra_test_connection.py
get_database_ready.sql
managerial_report.txt
New_task.txt
step1_read_task.py
step2_catagorize_task.py
step3_get_sql_ready.py
step4_exec_sql.py
TaskResults.xml
```

### Key Files
- **`step1_read_task.py`**: Reads the task description from the `New_task.txt` file.
- **`step2_catagorize_task.py`**: Classifies the task into one of the predefined categories.
- **`step3_get_sql_ready.py`**: Generates SQL queries based on the task description and example files.
- **`step4_exec_sql.py`**: Executes the generated SQL query, retrieves the results, and appends them to an XML file (`TaskResults.xml`).
- **`New_task.txt`**: Contains the task description to be processed.
- **`TaskResults.xml`**: Stores the results of processed tasks in XML format.
- **`customer_order_inquiry.txt`**, **`managerial_report.txt`**: Example files used to guide SQL generation for specific categories.
- **`get_database_ready.sql`**: SQL script to set up the database schema and populate it with sample data.

### Optional Files
- **`extra_test_connection.py`**: A utility script to test database connections and execute SQL commands. Not required for the main process.
- **`extra_select_and_save_result_in_xml.py`**: A utility script to query the database and save results in XML and CSV formats. Not required for the main process.

## Prerequisites

1. **Python 3.8+**: Ensure Python is installed on your system.
2. **PostgreSQL**: The project uses a PostgreSQL database.
3. **Environment Variables**: Create a `.env` file in the root directory with the following content:
   ```
   ANTHROPIC_API_KEY=<your_api_key>
   DB_HOST=<your_database_host>
   DB_NAME=<your_database_name>
   DB_USER=<your_database_user>
   DB_PASSWORD=<your_database_password>
   DB_PORT=<your_database_port>
   ```

4. **Install Dependencies**: Run the following command to install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## How to Use

1. **Set Up the Database**:
   - Use the `get_database_ready.sql` script to set up the database schema and populate it with sample data.

2. **Add a Task**:
   - Write the task description in the `New_task.txt` file.

3. **Run the Main Script**:
   - Execute the `step4_exec_sql.py` script to process the task:
     ```bash
     python step4_exec_sql.py
     ```

4. **View Results**:
   - The results of the task will be appended to the `TaskResults.xml` file.

## Example Workflow

1. Add the following task to `New_task.txt`:
   ```
   the revenue aggregate by months and products for Product A and Product B and for January and Feb 2025, and then pivot the result so that the columns represent products and the rows represent year-month
   ```

2. Run the main script:
   ```bash
   python step4_exec_sql.py
   ```

3. Check the `TaskResults.xml` file for the generated SQL query and its results.

## Notes

- The `extra_test_connection.py` and `extra_select_and_save_result_in_xml.py` files are utility scripts used for testing and are not required for the main process.
- Ensure the database is properly set up and accessible before running the scripts.

## Troubleshooting

- If you encounter issues with missing environment variables, ensure the `.env` file is correctly configured.
- For database connection errors, verify the credentials and database availability.

## License

This project is licensed under the MIT License.

