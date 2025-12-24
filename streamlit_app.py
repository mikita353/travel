import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# -----------------------------------
# Streamlit setup
# -----------------------------------

st.set_page_config(page_title="AI Travel Planner", layout="centered")
st.title("✈️ AI-Powered Travel Planner")

# -----------------------------------
# OpenAI API Key (USER INPUT)
# -----------------------------------

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please enter your OpenAI API key to continue.")
    st.stop()

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
    st.session_state.qa_history = []

if "current_question" not in st.session_state:
    st.session_state.current_question = None  # IMPORTANT

if "final_plan" not in st.session_state:
    st.session_state.final_plan = None

# -----------------------------------
# Prompts (SYSTEM-ONLY)
# -----------------------------------

first_question_prompt = PromptTemplate(
    input_variables=[],
    template="""
You are a professional travel planner.
Ask the FIRST detailed question needed to plan a vacation.
Assume the user does not know where they want to go.
Ask only ONE clear, specific question.
Return only the question text.
"""
)

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

# -----------------------------------
# Generate FIRST question (once)
# -----------------------------------

if st.session_state.current_question is None:
    llm = get_llm()
    chain = first_question_prompt | llm
    result = chain.invoke({})
    st.session_state.current_question = result.content.strip()

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
            st.session_state.qa_history.append(
                (st.session_state.current_question, user_answer.strip())
            )
            st.session_state.step += 1

            history_text = "\n".join(
                [f"Q: {q}\nA: {a}" for q, a in st.session_state.qa_history]
            )

            llm = get_llm()

            if st.session_state.step < 5:
                chain = next_question_prompt | llm
                next_q = chain.invoke({"history": history_text})
                st.session_state.current_question = next_q.content.strip()
            else:
                chain = final_plan_prompt | llm
                final_plan = chain.invoke({"history": history_text})
                st.session_state.final_plan = final_plan.content.strip()

            st.rerun()
