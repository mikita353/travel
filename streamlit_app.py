import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

st.set_page_config(page_title="Dynamic AI Vacation Planner", layout="centered")
st.title("🌴 Dynamic AI Vacation Planner")

# Sidebar: OpenAI key input
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()

# Initialize LLM
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=openai_api_key
)

# Session state for conversation
if "conversation" not in st.session_state:
    st.session_state.conversation = []  # stores tuples (question, answer)
if "next_question" not in st.session_state:
    st.session_state.next_question = (
        "You are a travel planner AI. Ask me the first detailed question "
        "to plan a vacation. Assume I don't know where I want to go."
    )
if "final_plan" not in st.session_state:
    st.session_state.final_plan = None

# Display previous Q&A
for i, (q, a) in enumerate(st.session_state.conversation):
    st.markdown(f"**Q{i+1}: {q}**")
    st.markdown(f"*Your answer:* {a}")

# If we already have the final plan, display it
if st.session_state.final_plan:
    st.subheader("📝 Tentative Vacation Plan")
    st.write(st.session_state.final_plan)
else:
    # Show the next question
    st.markdown(f"**Next Question:** {st.session_state.next_question}")
    user_input = st.text_input("Your answer:", key="current_answer")

    if st.button("Submit Answer"):
        if user_input.strip() != "":
            # Save the answer
            st.session_state.conversation.append((st.session_state.next_question, user_input.strip()))

            # Prepare conversation context
            conversation_text = "\n".join(
                [f"Q: {q}\nA: {a}" for q, a in st.session_state.conversation]
            )

            # Decide whether to ask next question or generate final plan
            if len(st.session_state.conversation) < 5:
                prompt_template = ChatPromptTemplate.from_template(
                    """You are a helpful travel planner AI.

                    The user has provided the following answers:
                    {conversation}

                    Ask the next relevant question for planning their vacation. 
                    Keep it specific and actionable. Only provide the question text."""
                )

                chain = LLMChain(llm=llm, prompt=prompt_template)
                next_q = chain.run(conversation=conversation_text)
                st.session_state.next_question = next_q.strip()
            else:
                # Generate final vacation plan
                prompt_template = ChatPromptTemplate.from_template(
                    """You are a travel planner AI.

                    Based on the following user answers:
                    {conversation}

                    Generate a complete, detailed, tentative vacation plan, including destination suggestions, activities, duration, and other recommendations."""
                )
                chain = LLMChain(llm=llm, prompt=prompt_template)
                final_plan = chain.run(conversation=conversation_text)
                st.session_state.final_plan = final_plan.strip()
                st.session_state.next_question = None

            st.experimental_rerun()
        else:
            st.warning("Please provide an answer before proceeding.")
