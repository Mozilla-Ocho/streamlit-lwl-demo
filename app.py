import streamlit as st
import datetime
from pipeline import run_pipeline
import json
from streamlit_inspector import inspect

st.set_page_config(page_title="Streamlit Chat App", page_icon="🧊", layout="wide")


st.title("Learning Companion Concept Explorer")

if "openai_model" not in st.session_state:
    st.session_state.model = "gpt-4o"
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ''
if 'goals' not in st.session_state:
    st.session_state.goals = ''
if 'skills' not in st.session_state:
    st.session_state.skills = ''
if 'source_material' not in st.session_state:
    st.session_state.source_material = ''

col1, col2 = st.columns([1,3])

with col1:
    with st.form(key='inputs'):
        st.text_input("OpenAI API key (not saved)", key='openai_api_key')
        st.subheader("Learning Goals")
        goals = st.text_area("What are your learning goals? This will help the AI know what's most relevant to you.", key='goals')
        st.subheader("Current Skills Level")
        skills = st.text_area("Describe your experience level. The AI can use this to tailor its responses.", key='skills')
        st.subheader("Source Material")
        source_material = st.text_area("Enter the source material here. Using Firefox's reader view on a web page is recommended, then just copy+paste:", key='source_material')
        submit_source_material = st.form_submit_button("Submit")
    
def quiz_ui():
    placeholder = st.empty()
    goals = st.session_state.goals
    skills = st.session_state.skills
    source_material = st.session_state.source_material
    openai_api_key = st.session_state.openai_api_key
    model = st.session_state.model
    [key_topics, learning_context, quiz] = run_pipeline(goals=goals, skills=skills, source_material=source_material, model=model, openai_api_key=openai_api_key, placeholder=placeholder)
    placeholder.empty()
    quiz_data = json.loads(quiz)
    for s_idx, section in enumerate(quiz_data["keyTopics"]):
        st.subheader(section["keyTopic"])
        for q_idx, question in enumerate(section["questions"]):
            with st.expander(question["questionTitle"]):
                options = question["answers"]
                correct_index = question["answerIndex"]
                # Use a form to prevent automatic reruns when a selection is made
                with st.form(key=f"question_{s_idx}_{q_idx}"):
                    selected_index = st.radio("Select an answer:", options, key=f"answer_{s_idx}_{q_idx}")
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        # Check if the selected answer is correct
                        if options.index(selected_index) == correct_index:
                            st.success("Correct! 🟢")
                            st.write(question["reasoning"])
                            st.write(question["context_relevance"])
                            st.write(question["follow_up_knowledge"])
                        else:
                            st.error("Incorrect. 🔴")
                            st.write(f"The correct answer is: {options[correct_index]}")
                            st.write(question["reasoning"])
                            st.write(question["context_relevance"])
                            st.write(question["requisite_knowledge"])

with col2:
    goals = st.session_state.goals
    skills = st.session_state.skills
    source_material = st.session_state.source_material
    openai_api_key = st.session_state.openai_api_key
    if goals == '' or skills == '' or source_material == '' or openai_api_key == '':
        st.warning("Please fill in all fields.")
    else:
        quiz_ui()

