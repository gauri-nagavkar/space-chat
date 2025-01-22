from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import FunctionCallingAgentWorker
from data_access import fetch_apod_data, fetch_mars_rover_photos 

class Agent:
  """A class to interact with the large language model and fetch data from NASA APIs."""

  def __init__(self):
    self.llm = OpenAI(model="gpt-4o")

    self.apod_tool = FunctionTool.from_defaults(fn=fetch_apod_data, name="fetch_apod_data", description="Fetch Astronomy Picture of the Day.")
    self.mars_rover_tool = FunctionTool.from_defaults(fn=fetch_mars_rover_photos, name="fetch_mars_rover_photos", description="Fetch Mars Rover Photos.")

    self.agent_worker = FunctionCallingAgentWorker.from_tools(
        [self.apod_tool, self.mars_rover_tool], llm=self.llm, verbose=True, allow_parallel_tool_calls=False)
    
    self.agent = self.agent_worker.as_agent()

  def chat(self, query):
    """
    Sends a query to the large language model and returns the response.

    Args:
        query: The user's query.

    Returns:
        A dictionary containing the response from the large language model.
    """
    return self.agent_worker.chat(query)