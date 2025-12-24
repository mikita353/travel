import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# -----------------------------------
# Streamlit setup
# -----------------------------------

st.set_page_config(page_title="AI Travel Planner", layout="centered")
st.title("✈️ AI-Powered Travel Planner")

# -----------------------------------
# OpenAI API Key (Streamlit Cloud)
# -----------------------------------

if "OPENAI_API_KEY" not in st.secrets:
    st.error("OpenAI API key not found. Please add it in Streamlit Secrets.")
    st.stop()

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# -----------------------------------
# Initialize LLM
# -----------------------------------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
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
You are a professional travel planner.

Based on the following questions and answers:
{history}

Create a detailed **Tentative Vacation Plan** including:
- Suggested destination(s)
- Length of trip
- Activities and experiences
- Travel style and budget assumptions

Be clear, practical, and well structured.
"""
)

next_question_chain = next_question_prompt | llm
final_plan_chain = final_plan_prompt | llm

# -----------------------------------
# Display Previous Q&A
# -----------------------------------

if st.session_state.qa_history:
    st.subheader("Your Answers So Far")
    for i, (q, a) in enumerate(st.session_state.qa_history, start=1):
        st.markdown(f"**Q{i}:** {q}")
        st.markdown(f"*A:* {a}")

st.divider()

# -----------------------------------
# Main Flow
# -----------------------------------

if st.session_state.final_plan:
    st.subheader("🗺️ Your Tentative Vacation Plan")
    st.markdown(st.session_state.final_plan)

    if st.button("Start Over"):
        st.session_state.clear()
        st.rerun()

else:
    st.subheader(f"Question {st.session_state.step + 1} of 5")
    st.markdown(f"**{st.session_state.current_question}**")

    user_answer = st.text_input("Your answer:")

    if st.button("Submit Answer"):
        if not user_answer.strip():
            st.warning("Please provide an answer before continuing.")
        else:
            # Save answer
            st.session_state.qa_history.append(
                (st.session_state.current_question, user_answer.strip())
            )
            st.session_state.step += 1

            # Build conversation history text
            history_text = "\n".join(
                [f"Q: {q}\nA: {a}" for q, a in st.session_state.qa_history]
            )

            # Decide next action
            if st.session_state.step < 5:
                next_q = next_question_chain.invoke(
                    {"history": history_text}
                )
                st.session_state.current_question = next_q.content.strip()
            else:
                final_plan = final_plan_chain.invoke(
                    {"history": history_text}
                )
                st.session_state.final_plan = final_plan.content.strip()

            st.rerun()
