import datetime
import os
import sys
import litellm
import pytz
import yaml
from smolagents import CodeAgent, LiteLLMModel, tool
from Gradio_UI import GradioUI
from tools.final_answer import FinalAnswerTool
from tools.visit_webpage import VisitWebpageTool

# Very useful to see the actual interaction with the LLM at a level below the huggingface wrapper
# litellm._turn_on_debug()

if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable")
    sys.exit(1)

openai_api_key = os.getenv("OPENAI_API_KEY")

# Below is an example of a tool that does nothing. Amaze us with your creativity !
@tool
def my_custom_tool(arg1:str, arg2:int)-> str: #it's import to specify the return type
    #Keep this format for the description / args / args description but feel free to modify the tool
    """A tool that prints the arg1 parameter arg2 times. 
    Args:
        arg1: the string to print
        arg2: the number of times to print the string
    """
    rvalue = []
    for i in range(arg2):
        rvalue.append(arg1)
    return str.join(" ", rvalue)

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


# duck_duck_go_search = DuckDuckGoSearchTool()

model = LiteLLMModel(
    model_id="openai/gpt-4o-mini",
    api_base="https://api.openai.com/v1",
    api_key=openai_api_key
)

# Import tool from Hub
# image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("prompts.yaml", 'r', encoding='utf-8') as stream:
    prompt_templates = yaml.safe_load(stream)

agent = CodeAgent(
    model=model,
    tools=[FinalAnswerTool(), VisitWebpageTool(), get_current_time_in_timezone], ## add your tools here (don't remove final answer)
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates,
    additional_authorized_imports=["requests", "markdownify"],
)

# If you don't want to run this as a gradio app, just use the following line
response = agent.run("What is the next event posted on hsv.ai?")

# GradioUI(agent).launch()
