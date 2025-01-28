from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import FunctionCallingAgentWorker
from data_access import fetch_apod_data, fetch_mars_rover_photos, fetch_moon_phase_and_weather, fetch_iss_location, fetch_people_in_space, fetch_space_weather

class Agent:
    """A class to interact with the large language model and fetch data from NASA APIs."""

    def __init__(self):
        self.llm = OpenAI(model="gpt-4o")

        self.apod_tool = FunctionTool.from_defaults(
            fn=fetch_apod_data, name="fetch_apod_data", description="Fetch Astronomy Picture of the Day."
        )
        self.mars_rover_tool = FunctionTool.from_defaults(
            fn=fetch_mars_rover_photos, name="fetch_mars_rover_photos", description="Fetch Mars Rover Photos."
        )
        self.fetch_moon_phase_and_weather_tool = FunctionTool.from_defaults(
        fn=fetch_moon_phase_and_weather,
        name="fetch_moon_phase",
        description="Fetch the current moon phase and illumination."
        )
        self.iss_tool = FunctionTool.from_defaults(fn=fetch_iss_location, name="fetch_iss_location", description="Fetch the current location of the ISS.")
        self.people_in_space_tool = FunctionTool.from_defaults(fn=fetch_people_in_space, name="fetch_people_in_space", description="Fetch the list of people currently in space.")
        self.space_weather_tool = FunctionTool.from_defaults(
            fn=fetch_space_weather,
            name="fetch_space_weather",
            description="Fetch recent space weather events from NASA's DONKI API."
        )

        tools = [self.apod_tool, self.mars_rover_tool, self.fetch_moon_phase_and_weather_tool, self.iss_tool, self.people_in_space_tool, self.space_weather_tool]

        self.agent_worker = FunctionCallingAgentWorker.from_tools(tools,
            llm=self.llm,
            verbose=True,
            allow_parallel_tool_calls=False,
        )
        self.agent = self.agent_worker.as_agent()

    def chat(self, query, history):
        """
        Sends a query to the large language model along with conversation history and returns the response.

        Args:
            query: The user's query.
            history: List of past conversation messages.

        Returns:
            A dictionary containing the response from the large language model.
        """
        # Combine the history into a single string for context
        context = "\n".join(
            [f"{msg['role'].capitalize()}: {msg['content']}" for msg in history]
        )
        # Append the current query
        full_query = f"{context}\nUser: {query}"

        # Use the agent's `chat` method
        return self.agent.chat(full_query)
