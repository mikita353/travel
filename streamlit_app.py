import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

def question1():
    """
    Ask the first question to plan the vacation
    
    Returns:
    A question for the user
    """

    prompt_template_name = PromptTemplate(
        input_variables=[],
        template="""You are planning an entire vacation for me. Ask me five detailed questions to 
        provide me a tentative trip plan. Ask me one at a time; wait for me to respond and then
        proceed with the next question. Assume I don't know where I want to go and suggest a spot.
        Then tell me the "tentative" trip.""")

    name_chain = LLMChain(llm=llm,
                          prompt=prompt_template_name,
                          output_key='travel')

    test = 'vacation'
    chain = SequentialChain(
        chains=[name_chain],
        input_variables=['test'],
        output_variables=['travel']
     )    

    response = chain({'test': test})
    return response


    
def generate_travel(prompt1: str) -> list[str]:
    """
    Generate a list of movie suggestions

    Parameters:
    prompt1 (str): prompt 1

    Returns:
    list: Tentative trip plan.
    """

    prompt_template_name = PromptTemplate(
        input_variables=['gender', 'nationality'],
        template="""You are planning an entire vacation for me. Ask me five detailed questions to 
        provide me a tentative trip plan. Ask me one at a time; wait for me to respond and then
        proceed with the next question. Assume I don't know where I want to go and suggest a spot.
        Then tell me the "tentative" trip.""")

    name_chain = LLMChain(llm=llm,
                          prompt=prompt_template_name,
                          output_key='travel')

    chain = SequentialChain(
        chains=[name_chain],
        input_variables=['favorite_movies'],
        output_variables=['travel']
     )    

    response = chain({'favorite_movies': favorite_movies})
    return response

# main code
st.title('Travel Suggestions')

# DO NOT CHANGE BELOW ----


# get open AI key from user
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    
# initialize Open AI
import os
os.environ['OPENAI_API_KEY'] = openai_api_key
llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature = 0.6)
 
# DO NOT CHANGE ABOVE ----

response = question1()
prompt = response['travel'].strip().split(",")
st.write(prompt)


'''

# ask user for what they want
prompt = generate_xxx()

# for loop
p1 = st.text_input(prompt)

# get the answer from LLM
if favorite_movies:
    response = generate_travel(favorite_movies)
    prompt = response['travel'].strip().split(",")
    '''
