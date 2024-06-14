import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

def generate_movie_suggestions(favorite_movies: str) -> list[str]:
    """
    Generate a list of movie suggestions

    Parameters:
    favorite_movies (str): Favorite movies

    Returns:
    list: list of movie suggestions
    """

    prompt_template_name = PromptTemplate(
        input_variables=['gender', 'nationality'],
        template="""Based on these movies: {favorite_movies}, create a list of movies you would recommend.
        The list should have at least 3 movies and at most 7 movies. The list should neat and concise, 
        providing a short 1-3 sentence summary on the movie. There shouldn't be a lot of unnecessary
        modifiers and words in general. A thirteen year old should be able to understand your vocabulary."""
                )

    name_chain = LLMChain(llm=llm,
                          prompt=prompt_template_name,
                          output_key='Movie_suggestions')

    chain = SequentialChain(
        chains=[name_chain],
        input_variables=['favorite_movies'],
        output_variables=['Movie_suggestions']
     )    

    response = chain({'favorite_movies': favorite_movies})
    return response

# main code
st.title('Movie Suggestions')

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

# ask user for what they want
favorite_movies = st.textbox()

# get the answer from LLM
response = generate_movie_suggestions(favorite_movies)
Movie_suggestions = response['Movie Suggestions: '].strip().split(",")

for name in Movie_suggestions:
    st.write("--", name)
