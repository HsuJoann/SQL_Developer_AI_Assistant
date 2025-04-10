from anthropic import Anthropic
from step1_read_task import read_file_content
from step2_catagorize_task import simple_classify
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY is not set in the .env file.")

client = Anthropic()
MODEL_NAME = "claude-3-5-sonnet-20241022"

def generate_prompt(example, task_in_hand):
    """
    Generates a prompt for the AI model based on the example and task description.
    """
    return f"""
        You are an sql developer who have several example code scripts. You will write sql code for this task
        <task>
        {task_in_hand}
        </task>
        following this thought process:
        <thought_process> 
        1.find the closest example task in the example file . 
        2 modify the corresponding sql code in that example according to your current task description.
        </thought_process>
        
        <example>
        {example}
        </example>

        Provide only the SQL query in your response, enclosed within <sql> tags.
    """

def generate_sql(prompt):
    """
    Sends the prompt to the AI model and retrieves the generated SQL query.
    """
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=1000,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    result = response.content[0].text
    if "<sql>" not in result or "</sql>" not in result:
        raise ValueError("The response does not contain the expected <sql> tags.")
    # print(result)
    # Extract the SQL query from the response
    # Assuming the response is well-formed, we can split by the tags
    sql = result.split('<sql>')[1].split('</sql>')[0].strip()
    return sql

if __name__ == "__main__":
    # Define file paths
    folder_path = r"C:\Users\jingh\python_code_folder\SQL_developer_AI_assistant"
    task_path = os.path.join(folder_path, "New_task.txt")

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
    sql_command = generate_sql(prompt)
  

    # Print the generated SQL query
    print("Generated SQL:")
    print(sql_command)