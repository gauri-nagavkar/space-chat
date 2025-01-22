import requests
from pydantic import Field
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.core.base.llms.types import ChatResponse, LLMMetadata
from data_access import fetch_apod_data, fetch_mars_rover_photos

class LocalLLM(FunctionCallingLLM):
    """Wrapper for interacting with a locally hosted Llama 3 model using Ollama."""

    base_url: str = Field(default="http://localhost:11400", description="Base URL for the Ollama server.")
    model: str = Field(default="llama3", description="Model name to use for queries.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._metadata = LLMMetadata(
            context_window=4096,  # Adjust based on your model
            num_output_tokens=512,  # Max tokens the model can generate
            model_name="Llama 3",
            is_function_calling_model=True,  # Enable function calling
        )

    @property
    def metadata(self) -> LLMMetadata:
        """Returns metadata about the LLM."""
        return self._metadata

    def complete(self, prompt: str, **kwargs) -> str:
        """Completes a given prompt using the local model."""
        response = self._query_model(prompt, **kwargs)
        return response

    def chat(self, messages, **kwargs) -> ChatResponse:
        """Handles chat-style messages."""
        prompt = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
        response = self._query_model(prompt, **kwargs)
        return ChatResponse(response=response)

    def _prepare_chat_with_tools(self, messages, functions):
        """
        Prepares a prompt with tools for function calling.

        Args:
            messages: List of chat messages.
            functions: List of available functions.

        Returns:
            A dictionary with prepared `prompt` and `functions`.
        """
        # Prepare the chat context
        prompt = "\n".join(f"{m['role']}: {m['content']}" for m in messages)

        # Append the available function descriptions
        function_descriptions = "\n".join(
            f"Function: {fn['name']} - {fn['description']}" for fn in functions
        )
        prompt += f"\n\nAvailable functions:\n{function_descriptions}"

        # Return the prepared prompt and functions
        return {"prompt": prompt, "functions": functions}

    def _query_model(self, prompt: str, **kwargs) -> str:
        """
        Sends a request to the Ollama server to generate a response.

        Args:
            prompt: The input prompt.
            kwargs: Additional arguments.

        Returns:
            The generated response as a string.
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "options": {"temperature": kwargs.get("temperature", 0.7), "max_length": 512},
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            return f"Error communicating with the model: {e}"


    # Implement abstract methods as no-ops or basic implementations
    def _prepare_chat_with_tools(self, messages, functions):
        """Prepares chat for tool use."""
        raise NotImplementedError("Tool integration is not supported for this local LLM.")

    def achat(self, messages, **kwargs):
        """Asynchronous chat (not implemented)."""
        raise NotImplementedError("Asynchronous chat is not supported for this local LLM.")

    def acomplete(self, prompt: str, **kwargs):
        """Asynchronous completion (not implemented)."""
        raise NotImplementedError("Asynchronous completion is not supported for this local LLM.")

    def astream_chat(self, messages, **kwargs):
        """Asynchronous streaming chat (not implemented)."""
        raise NotImplementedError("Asynchronous streaming chat is not supported for this local LLM.")

    def astream_complete(self, prompt: str, **kwargs):
        """Asynchronous streaming completion (not implemented)."""
        raise NotImplementedError("Asynchronous streaming completion is not supported for this local LLM.")

    def stream_chat(self, messages, **kwargs):
        """Streaming chat (not implemented)."""
        raise NotImplementedError("Streaming chat is not supported for this local LLM.")

    def stream_complete(self, prompt: str, **kwargs):
        """Streaming completion (not implemented)."""
        raise NotImplementedError("Streaming completion is not supported for this local LLM.")

class Agent:
  """A class to interact with the large language model and fetch data from NASA APIs."""

  def __init__(self):
    self.llm = LocalLLM()

    # Define tools for NASA APIs
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