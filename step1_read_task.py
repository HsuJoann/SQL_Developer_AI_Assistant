def read_file_content(file_path):
    """
    Reads the content of the New_task.txt file and returns it as a string.
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        file_path = r"C:\Users\jingh\python_code_folder\SQL_developer_AI_assistant\New_task.txt"
        content = read_file_content(file_path)
        # Example usage: print the content (can be removed if not needed)
        print(content)
    except Exception as e:
        print(e)