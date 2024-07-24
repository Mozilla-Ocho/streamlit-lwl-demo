import streamlit as st
import datetime
from pipeline import generate_key_topics, generate_learning_context, generate_questions
import json
from streamlit_inspector import inspect

st.set_page_config(page_title="Learn with LLMs explorer", page_icon="🧊", layout="wide", initial_sidebar_state="collapsed")

st.title("Learning with LLMs Concept Explorer")

model_options = ["gpt-4o", "gpt-4o-mini"]

if "openai_model" not in st.session_state:
    st.session_state.model = model_options[1]
if "has_saved_openai_key" not in st.session_state:
    st.session_state.has_saved_openai_key = False
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ''
if 'goals' not in st.session_state:
    st.session_state.goals = ''
if 'skills' not in st.session_state:
    st.session_state.skills = ''
if 'source_material' not in st.session_state:
    st.session_state.source_material = ''
if "active_topic_idx" not in st.session_state:
    st.session_state.active_topic_idx = 0
if "blank_out_questions_nav_trick" not in st.session_state:
    st.session_state.blank_out_questions_nav_trick = 0


if "a" in st.query_params and st.query_params["a"] == st.secrets.query_auth_secret:
    # when the query auth param is present and matches, it will allow the api key secret to be loaded automatically.
    if st.secrets.openai_api_key:
        st.session_state.openai_api_key = st.secrets.openai_api_key
        st.session_state.has_saved_openai_key = True

col1, col2 = st.columns([1,3])

# some dev debugging and state clearing
#st.cache_data.clear()
debug_area = None
if st.secrets.show_debug_area:
    debug_area = st.container()
    debug_area.markdown("----\n#### Debugging / Logging Area:")
def debug(label, thing):
    if debug_area:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        debug_area.expander(f"{timestamp} {label}").write(thing)

with col1:
    with st.form(key='inputs'):
        if not st.session_state.has_saved_openai_key:
            # collect an api key if the secrets file doesn't have one.
            st.text_input("OpenAI API key (not saved)", key='openai_api_key', placeholder="sk-...")
            st.caption("Mozillians please contact @jwhiting on slack for access")
        if False:
            # temporarily disable this feature. always using 4o-mini for now.
            st.selectbox("Model (4o mini highly recommended for cost effectiveness)", model_options, key='model')
        st.subheader("Learning Goals")
        goals = st.text_area("What are your learning goals? This will help the AI know what's most relevant to you.", key='goals')
        st.subheader("Current Skills Level")
        skills = st.text_area("Describe your experience level. The AI can use this to tailor its responses.", key='skills')
        st.subheader("Source Material")
        source_material = st.text_area("Enter the source material here. Using Firefox's reader view on a web page is recommended, then just copy+paste:", key='source_material')
        submit_source_material = st.form_submit_button("Submit")
        if submit_source_material:
            # set quiz back to the first topic if regenerating, since the number and nature of the topics can change.
            st.session_state.active_topic_idx = 0
  
def quiz_questions(questions):
    if st.session_state.blank_out_questions_nav_trick != 0:
        # this is a hack when navigating between quiz topic sections to blank out the questions. otherwise streamlit will keep the old questions in the UI in a disabled state while generating new ones, which just looks really bad visually and is hard to understand what is happening.
        # navigation works by setting blank_out_questions_nav_trick to -1 or 1, then rerunning the script. this will cause the questions to be blanked out, then the actual index is updated, which causes new questions will be generated.
        st.session_state.active_topic_idx += st.session_state.blank_out_questions_nav_trick
        st.session_state.blank_out_questions_nav_trick = 0
        st.rerun()
        return
    for q_idx, question in enumerate(questions):
        with st.expander(question["questionTitle"]):
            options = question["answers"]
            correct_index = question["answerIndex"]
            with st.form(key=f"question_{q_idx}"):
                selected_index = st.radio("Select an answer:", options, key=f"answer_{q_idx}")
                submitted = st.form_submit_button("Submit")
                if submitted:
                    if options.index(selected_index) == correct_index:
                        st.success("Correct! 🟢")
                        st.markdown(f'**Why:** {question["reasoning"]}')
                        st.markdown(f'**Relevance to your goals and skills:** {question["context_relevance"]}')
                        st.markdown(f'**What to learn next:** {question["follow_up_knowledge"]}')
                    else:
                        st.error("Incorrect. 🔴")
                        st.markdown(f'**Why:** {question["reasoning"]}')
                        st.markdown(f'**Relevance to your goals and skills:** {question["context_relevance"]}')
                        st.markdown(f'**What to review to get this right:** {question["requisite_knowledge"]}')

def current_quiz_section(topics, learning_context):
    if st.session_state.active_topic_idx >= len(topics):
        st.session_state.active_topic_idx = 0
    s_idx = st.session_state.active_topic_idx
    active_topic = topics[s_idx]
    col1,col2,col3 = st.columns([3,1,1])
    with col1:
        st.subheader(active_topic)
    with col2:
        if s_idx > 0:
            if st.button("Previous topic"):
                st.session_state.blank_out_questions_nav_trick = -1
                st.rerun()
    with col3:
        if s_idx < len(topics) - 1:
            if st.button("Next topic"):
                st.session_state.blank_out_questions_nav_trick = 1
                st.rerun()
    source_material = st.session_state.source_material
    openai_api_key = st.session_state.openai_api_key
    model = st.session_state.model
    [questions, prompt, response] = generate_questions(for_key_topic=active_topic, learning_context=learning_context, source_material=source_material, model=model, _openai_api_key=openai_api_key)
    debug('questions prompt', prompt)
    debug('questions response', response)
    quiz_questions(questions)

def quiz():
    st.subheader("Initial context for the quiz:")
    goals = st.session_state.goals
    skills = st.session_state.skills
    source_material = st.session_state.source_material
    openai_api_key = st.session_state.openai_api_key
    model = st.session_state.model

    st.markdown("First we generate a *learning context* document based on your learning goals and current skills. It asks the LLM to think through a learning trajectory for you with sub goals, topics to focus on, and problems you might encounter:")
    [learning_context,prompt,response] = generate_learning_context(goals=goals, skills=skills, model=model, _openai_api_key=openai_api_key)
    debug('learning context prompt', prompt)
    debug('learning context response', response)
    st.expander("Learning Context generated :white_check_mark:").write(learning_context)

    st.markdown("Next, we generate a set of key topics from the source material you provided to break the quiz into relevant sections:")
    [topics, prompt, response] = generate_key_topics(source_material=source_material, model=model, _openai_api_key=openai_api_key)
    debug('key topics prompt', prompt)
    debug('key topics response', response)
    debug('key topics object', topics)
    st.expander("Key Topics generated :white_check_mark:").write(topics)

    st.markdown("Finally, we generate a set of questions based on each key topic, with each one contextualized for you personally depending on whether your answer was right or wrong:")
    st.header("Quiz:")
    current_quiz_section(topics, learning_context)

with col2:
    goals = st.session_state.goals
    skills = st.session_state.skills
    source_material = st.session_state.source_material
    openai_api_key = st.session_state.openai_api_key
    if goals == '' or skills == '' or source_material == '' or openai_api_key == '':
        st.warning("Please fill in all fields.")
    else:
        quiz()

