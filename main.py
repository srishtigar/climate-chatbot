
import streamlit as st
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

# Load environment variables from .env file
load_dotenv()

st.set_page_config(
    page_title="Climate-Resilient Agriculture System",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Climate-Resilient Agriculture System")
st.markdown("--- ")

st.sidebar.title("Settings")

# API Key Inputs
st.sidebar.subheader("API Keys")
noaa_api_key = st.sidebar.text_input("NOAA CDO API Key", type="password")
copernicus_uid = st.sidebar.text_input("Copernicus CDS UID", type="password")
copernicus_api_key = st.sidebar.text_input("Copernicus CDS API Key", type="password")
nasa_api_key = st.sidebar.text_input("NASA Earth API Key", type="password")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password")

if not all([noaa_api_key, copernicus_uid, copernicus_api_key, nasa_api_key, groq_api_key]):
    st.sidebar.warning("Please enter all required API keys.")
    st.stop()

# Store API keys in environment variables for sub-modules
os.environ["NOAA_API_KEY"] = noaa_api_key
os.environ["COPERNICUS_UID"] = copernicus_uid
os.environ["COPERNICUS_API_KEY"] = copernicus_api_key
os.environ["NASA_API_KEY"] = nasa_api_key
os.environ["GROQ_API_KEY"] = groq_api_key

st.success("All API keys loaded successfully!")

# Initialize LLM
llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

## Initializing the tools
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the Internet to find information on various topics, including climate change, agricultural practices, and environmental science."
)

math_chain = LLMMathChain.from_llm(llm=llm)
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool for answering math related questions. Only input mathematical expression need to be provided."
)

climate_reasoning_prompt = """
You are an AI assistant specialized in climate-resilient agriculture. Your task is to answer user questions related to climate, agriculture, environmental impacts, and sustainable practices. Logically arrive at the solution and provide a detailed explanation, displayed point-wise.

Question:{question}
Answer:
"""

climate_reasoning_template = PromptTemplate(
    input_variables=["question"],
    template=climate_reasoning_prompt
)

climate_reasoning_chain = LLMChain(llm=llm, prompt=climate_reasoning_template)

climate_reasoning_tool = Tool(
    name="ClimateReasoningTool",
    func=climate_reasoning_chain.run,
    description="A tool for answering logic-based and reasoning questions specifically about climate change, agriculture, environmental science, and sustainable farming practices."
)

## Initialize the agent
assistant_agent = initialize_agent(
    tools=[wikipedia_tool, calculator, climate_reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

st.markdown("""
Welcome to the **Climate-Resilient Agriculture System**! This application helps farmers and agricultural policymakers make informed decisions to adapt to climate change.

**Key Features:**
-   **Climate Data Visualization:** Explore historical climate data and future projections.
-   **Crop Suitability Analysis:** Get recommendations for suitable crop varieties based on climate conditions.
-   **Precision Irrigation Guidance:** Optimize water usage with data-driven insights.
-   **Agricultural Hazard Alerts:** Receive early warnings for droughts, floods, and other climate-related risks.
-   **Yield Prediction:** Forecast crop yields under various climate scenarios.

Navigate through the sections using the sidebar to access different functionalities.
""")

# Chatbot Section
st.subheader("Ask the Climate-Resilient Agriculture Assistant")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm your Climate-Resilient Agriculture Assistant. How can I help you today?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question := st.chat_input("Enter your question about climate or agriculture:"):
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    with st.spinner("Generating response..."):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = assistant_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)


