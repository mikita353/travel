import os
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# ------------------------
# Streamlit UI
# ------------------------

st.title("Travel Suggestions")

with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key",
        key="chatbot_api_key",
        type="password"
    )

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()

os.environ["OPENAI_API_KEY"] = openai_api_key

# ------------------------
# Initialize LLM (modern)
# ------------------------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.6
)

# ------------------------
# Prompt
# ------------------------

travel_prompt = PromptTemplate(
    input_variables=[],
    template="""
You are a professional travel planner.

1. Suggest a destination for someone who does not know where they want to go.
2. Ask FIVE detailed questions to plan the trip.
3. Then provide a clearly labeled **Tentative Trip Plan**.

Ask clear, practical questions (budget, duration, interests, travel style).
"""
)

# ------------------------
# Chain (LCEL)
# ------------------------

travel_chain = travel_prompt | llm

# ------------------------
# Functions
# ------------------------

def question1() -> str:
    """
    Generate vacation questions and a tentative trip plan
    """
    response = travel_chain.invoke({})
    return response.content


def generate_travel() -> str:
    """
    Generate a tentative trip plan (single-shot)
    """
    response = travel_chain.invoke({})
    return response.content

# ------------------------
# Run
# ------------------------

if st.button("Plan My Vacation"):
    result = question1()
    st.markdown(result)
