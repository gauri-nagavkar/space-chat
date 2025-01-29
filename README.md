# 🚀 Space Chat: Agentic Retrieval-Augmented Generation (RAG) in Action 🌌

Space Chat is an interactive application that demonstrates how Large Language Models (LLMs) can be enhanced with **Retrieval-Augmented Generation (RAG)** and **function calling agents**. By integrating LlamaIndex with APIs such as NASA's and Open Notify, this project bridges the gap between AI reasoning and live data retrieval, offering a practical use case for LLM-based systems.


---

## 🌟 What This Project Shows

This project is designed as a **showcase of cutting-edge LLM skills** and **real-world AI system design**, featuring:

- **Agentic Retrieval-Augmented Generation (RAG):** Retrieval-augmented workflows that combine the reasoning power of LLMs with live data from NASA and other APIs.
- **Function Calling with LlamaIndex:** Dynamically map user queries to API functions for precise, task-specific responses.
- **Autonomous Agents:** Dynamically invoke tools and retrieve relevant data based on user intent, demonstrating tool orchestration and adaptability.
- **Error Handling and Context Retention:** Maintain conversation context and handle edge cases gracefully for a robust experience.
- **Interactive AI Applications:** A Streamlit frontend for an easy user experience.

---

### Demo
Here’s a short video showcasing how Space Chat works:
![Space Chat Demo](./demo_vid.mp4)

---

## 🧠 What You'll Learn from Space Chat

### 🚀 **Agentic RAG for Real-World Applications**
- How to build **agentic workflows** that augment LLMs with real-time API integrations.
- Dynamically map user intent to the appropriate tools using **LlamaIndex's FunctionTool**.

### 🛠️ **Tool-Oriented Agents**
- Integrate multiple APIs (e.g., NASA APIs, ISS tracking, Moon phase data) into an intelligent agent.
- Use **FunctionCallingAgentWorker** for orchestrating tools in a modular and scalable way.

### 🌌 **LLM Applications Beyond Text Generation**
- Leverage **LLMs as reasoning agents** that handle queries, interact with APIs, and return actionable insights.
- Implement conversational memory to maintain context across user interactions.

### 🎨 **Streamlit for AI Frontends**
- Design an easy user-friendly interface that highlight LLM functionality.
- Use custom CSS to create an immersive "NASA-inspired" theme.

---

## 🚀 Core Features of Space Chat

### **1. Astronomy Picture of the Day (APOD)**
Fetch stunning images and descriptions directly from NASA's APOD API.

Example Query:  
_“Show me today’s APOD image.”_

---

### **2. Mars Rover Photos**
Explore breathtaking images captured by NASA’s Mars rovers like Curiosity and Opportunity.

Example Query:  
_“What photos did Curiosity capture on Sol 1000?”_

---

### **3. Moon Phase and Weather**
Retrieve details about the moon phase, illumination percentage, and local weather conditions.

Example Query:  
_“What’s the moon phase in Santa Clara today?”_

---

### **4. ISS Real-Time Tracker**
Track the **International Space Station (ISS)** in real-time and retrieve its current latitude and longitude.

Example Query:  
_“Where is the ISS right now?”_

---

### **5. People in Space**
Fetch a list of astronauts currently in space and their respective spacecraft.

Example Query:  
_“Who is currently in space?”_

---

### **6. Space Weather Events**
Access real-time space weather events like solar flares or geomagnetic storms from NASA's DONKI API.

Example Query:  
_“Tell me about the latest solar flare events.”_

---

## 🛠️ How It Works

1. **Query Understanding with LLMs:**  
   User queries are analyzed by an OpenAI LLM (GPT-4), which dynamically determines the appropriate tool to invoke.

2. **Agentic Workflow Execution:**  
   LlamaIndex maps the user intent to one of the integrated tools (e.g., APOD API, Mars Rover API) and retrieves the required data.

3. **Function Calling Agents:**  
   Through `FunctionCallingAgentWorker`, Space Chat seamlessly invokes APIs and processes the responses to deliver accurate, real-time insights.

4. **Conversation Context Management:**  
   The system maintains context across queries, enabling fluid, coherent conversations.

---

## 💻 Getting Started

### Prerequisites
- Python 3.8 or higher
- API keys for:
  - NASA APIs (`NASA_API_KEY`)
  - Visual Crossing Weather API (`WEATHER_API_KEY`)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/gauri-nagavkar/space-chat.git
   cd space-chat

2. Create a virtual environment (optional)
```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

3. Install requirements
```
pip install -r requirements.txt
```

4. Create a .env file in the root directory and add your API keys
```
NASA_API_KEY=your_nasa_api_key
WEATHER_API_KEY=your_weather_api_key
```

5. Run the app
```
streamlit run app.py
```

6. Open the app in your browser at http://localhost:8501

### 📜 File Structure
```
.
├── app.py                # Main Streamlit app
├── agent.py              # Agent setup with LlamaIndex and tools
├── data_access.py        # API integration functions
├── styles.css            # Custom CSS for the frontend
├── requirements.txt      # Project dependencies
├── README.md             # Documentation
├── .env                  # API keys (not included in the repo)
└── demo_video.mp4        # Video demo of the app
```

### requirements.txt
```
llama-index
openai
streamlit
python-dotenv
requests
```

## 🤝 Let’s Connect

If you're interested in LLM-based systems, RAG workflows, and API integration, or have suggestions to improve this project, feel free to reach out!

- Email: gauri.nagavkar@gmail.com
- LinkedIn: https://www.linkedin.com/in/gauri-nagavkar-371746151

🚀 Try it out, explore the code, and feel free to suggest or contribute improv