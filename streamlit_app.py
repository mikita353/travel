import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
#from secret_key import openapi_key

import os
os.environ['OPENAI_API_KEY'] = "12334566"

llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature = 0.6)

def generate_baby_names(gender: str,nationality:str) -> list[str]:
    """
    Generate a list of 5 baby names

    Parameters:
    gender (str): gender of baby
    nationailty (str) : nationailty of baby

    Returns:
    list: list of baby names
    """

    prompt_template_name = PromptTemplate(
        input_variables=['gender', 'nationality'],
        template="""I want to find a name for a {nationality} {gender} baby. 
                    Suggest top 5 popular names for the baby.
                    Return it as a comma separated list """
                )

    name_chain = LLMChain(llm=llm,
                          prompt=prompt_template_name,
                          output_key='baby_names')

    chain = SequentialChain(
        chains=[name_chain],
        input_variables=['gender', 'nationality'],
        output_variables=['baby_names']
    )

    response = chain({'gender': gender,
                      'nationality': nationality})
    return response



st.title('Baby Name Generator')

gender = st.sidebar.selectbox("Choose a gender",
                             ("Girl", "Boy"))
nationality = st.sidebar.selectbox("Choose the nationality", 
                                  ("American", "Indian", "Chinese", 
                                  "Russian")
                                )


if gender and nationality:
    response = langchain_helper.generate_baby_names(gender, nationality)
    baby_names = response['baby_names'].strip().split(",")
    st.write("** Top 5 Baby Names **")

    for name in baby_names:
        st.write("--", name)
