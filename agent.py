from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import FunctionCallingAgentWorker
from data_access import (
    fetch_apod_data,
    fetch_mars_rover_photos,
    fetch_moon_phase_and_weather,
    fetch_iss_location,
    fetch_people_in_space,
    fetch_space_weather,
)

class Agent:
    """
    A class to interact with the large language model and fetch data from NASA APIs.
    """

    def __init__(self):
        # Initialize the large language model
        self.llm = OpenAI(model="gpt-4o")

        # Define tools with appropriate descriptions
        self.apod_tool = FunctionTool.from_defaults(
            fn=fetch_apod_data,
            name="fetch_apod_data",
            description="Fetch Astronomy Picture of the Day data from NASA's API.",
        )
        self.mars_rover_tool = FunctionTool.from_defaults(
            fn=fetch_mars_rover_photos,
            name="fetch_mars_rover_photos",
            description="Fetch photos taken by Mars rovers.",
        )
        self.moon_phase_tool = FunctionTool.from_defaults(
            fn=fetch_moon_phase_and_weather,
            name="fetch_moon_phase",
            description="Fetch the current moon phase, illumination, and weather details for a specific location.",
        )
        self.iss_tool = FunctionTool.from_defaults(
            fn=fetch_iss_location,
            name="fetch_iss_location",
            description="Fetch the current location of the International Space Station (ISS).",
        )
        self.people_in_space_tool = FunctionTool.from_defaults(
            fn=fetch_people_in_space,
            name="fetch_people_in_space",
            description="Fetch the list of people currently in space and their respective spacecraft.",
        )
        self.space_weather_tool = FunctionTool.from_defaults(
            fn=fetch_space_weather,
            name="fetch_space_weather",
            description="Fetch recent space weather events from NASA's DONKI API.",
        )

        # List of tools for the agent
        tools = [
            self.apod_tool,
            self.mars_rover_tool,
            self.moon_phase_tool,
            self.iss_tool,
            self.people_in_space_tool,
            self.space_weather_tool,
        ]

        # Create an agent worker with tools
        self.agent_worker = FunctionCallingAgentWorker.from_tools(
            tools=tools,
            llm=self.llm,
            verbose=True,
            allow_parallel_tool_calls=False,
        )

        # Initialize the agent
        self.agent = self.agent_worker.as_agent()

    def chat(self, query: str, history: list) -> dict:
        """
        Sends a query to the language model along with conversation history and returns the response.

        Args:
            query (str): The user's query.
            history (list): List of past conversation messages.

        Returns:
            dict: A dictionary containing the response from the language model.
        """
        # Combine the conversation history into a single context string
        context = "\n".join(
            [f"{msg['role'].capitalize()}: {msg['content']}" for msg in history]
        )
        # Append the current query to the context
        full_query = f"{context}\nUser: {query}"

        # Get the response using the agent
        return self.agent.chat(full_query)
