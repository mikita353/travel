import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# -----------------------------------
# Streamlit setup
# -----------------------------------

st.set_page_config(page_title="AI Travel Planner", layout="centered")
st.title("✈️ AI-Powered Travel Planner")

# -----------------------------------
# OpenAI API Key (USER INPUT — REQUIRED)
# -----------------------------------

with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password"
    )

if not openai_api_key:
    st.info("Please enter your OpenAI API key to continue.")
    st.stop()

# -----------------------------------
# Initialize LLM (KEY PASSED EXPLICITLY)
# -----------------------------------

def get_llm():
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        openai_api_key=openai_api_key
    )

# -----------------------------------
# Session State
# -----------------------------------

if "step" not in st.session_state:
    st.session_state.step = 0

if "qa_history" not in st.session_state:
    st.session_state.qa_history = []  # list of (question, answer)

if "current_question" not in st.session_state:
    st.session_state.current_question = (
        "You are a professional travel planner. "
        "Ask the FIRST detailed question needed to plan a vacation. "
        "Assume the user does not know where they want to go."
    )

if "final_plan" not in st.session_state:
    st.session_state.final_plan = None

# -----------------------------------
# Prompt Templates
# -----------------------------------

next_question_prompt = PromptTemplate(
    input_variables=["history"],
    template="""
You are a professional travel planner.

Conversation so far:
{history}

Ask the NEXT most important question to plan the vacation.
Ask only ONE clear, specific question.
Do not repeat previous questions.
Return only the question text.
"""
)

final_plan_prompt = PromptTemplate(
    input_variables=["history"],
    template="""
You are a professional travel p
