import anthropic
from step1_read_task import read_file_content
import textwrap
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY is not set in the .env file.")

folder_path = r"C:\Users\jingh\python_code_folder\SQL_developer_AI_assistant"
task_path = os.path.join(folder_path, "New_task.txt")

task_in_hand = read_file_content(task_path)

client = anthropic.Anthropic(
    api_key=anthropic_api_key,
)

categories = textwrap.dedent("""<category> 
    <label>Database_performance</label>
    <content> database not working, slow performance, or other issues related to database speed and efficiency.
    </content> 
</category> 
<category> 
    <label>customer_order_inquiry</label>
    <content> Requests for information about the status of a customer order, including shipping and delivery details.
    </content> 
</category> 
<category> 
    <label>managerial_report</label> 
    <content> reports that provide insights into the performance of a business unit or department, including financial and operational metrics. 
    </content> 
</category> 
""")

def simple_classify(X):
    prompt = textwrap.dedent("""
    You will classify a new task into one of the following categories:
    <categories>
        {{categories}}
    </categories>

    Here is the new task description:
    <ticket>
        {{ticket}}
    </ticket>

    Respond with just the label of the category between category tags.
    """).replace("{{categories}}", categories).replace("{{ticket}}", X)
    response = client.messages.create( 
        messages=[{"role":"user", "content": prompt}, {"role":"assistant", "content": "<category>"}],
        stop_sequences=["</category>"], 
        max_tokens=4096, 
        temperature=0.0,
        model="claude-3-haiku-20240307"
    )
    
    # Extract the result from the response
    result = response.content[0].text.strip()
    return result

if __name__ == "__main__":
    # Example usage
    task_in_hand = read_file_content(r"C:\Users\jingh\python_code_folder\SQL_developer_AI_assistant\New_task.txt")
    print("Task in hand:", task_in_hand)
    category = simple_classify(task_in_hand)
    print("Category:", category)
