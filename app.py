import streamlit as st
import datetime
from pipeline import generate_key_topics, generate_learning_context, generate_questions
import json
from streamlit_inspector import inspect

st.set_page_config(page_title="Streamlit Chat App", page_icon="🧊", layout="wide")

st.title("Learning with LLMs Concept Explorer")

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
if 'quiz' not in st.session_state:
    st.session_state.quiz = {"keyTopics":[]}
if "key_topics" not in st.session_state:
    st.session_state.key_topics = []
if "quiz_active_topic_idx" not in st.session_state:
    st.session_state.quiz_active_topic_idx = 0
if "learning_context" not in st.session_state:
    st.session_state.learning_context = ''

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
  
def quiz_questions():
    s_idx = st.session_state.quiz_active_topic_idx
    quiz = st.session_state.quiz
    section = quiz["keyTopics"][s_idx] if s_idx < len(quiz["keyTopics"]) else None
    if not section:
        return
    for q_idx, question in enumerate(section["questions"]):
        with st.expander(question["questionTitle"]):
            options = question["answers"]
            correct_index = question["answerIndex"]
            with st.form(key=f"question_{s_idx}_{q_idx}"):
                selected_index = st.radio("Select an answer:", options, key=f"answer_{s_idx}_{q_idx}")
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

def current_quiz_section():
    key_topics = st.session_state.key_topics
    if st.session_state.quiz_active_topic_idx >= len(key_topics):
        st.session_state.quiz_active_topic_idx = 0
    s_idx = st.session_state.quiz_active_topic_idx
    active_topic = key_topics[s_idx]
    col1,col2,col3 = st.columns([3,1,1])
    with col1:
        st.subheader(active_topic)
    with col2:
        if s_idx > 0:
            if st.button("Previous topic"):
                st.session_state.quiz_active_topic_idx -= 1
                st.rerun()
    with col3:
        if s_idx < len(st.session_state.key_topics) - 1:
            if st.button("Next topic"):
                st.session_state.quiz_active_topic_idx += 1
                st.rerun()
    quiz = st.session_state.quiz
    section = quiz["keyTopics"][s_idx] if s_idx < len(quiz["keyTopics"]) else None
    if not section:
        st.write(f"Generating questions for {active_topic}...")
        source_material = st.session_state.source_material
        openai_api_key = st.session_state.openai_api_key
        model = st.session_state.model
        learning_context = st.session_state.learning_context
        questions = generate_questions(for_key_topic=active_topic, learning_context=learning_context, source_material=source_material, model=model, _openai_api_key=openai_api_key)
        quiz["keyTopics"].append({"keyTopic": active_topic, "questions": questions})
        st.session_state.quiz = quiz # do i need this?
        st.rerun()
    else:
        quiz_questions()

def quiz():
    st.subheader("Initial context for the quiz:")
    placeholder = st.empty()
    goals = st.session_state.goals
    skills = st.session_state.skills
    source_material = st.session_state.source_material
    openai_api_key = st.session_state.openai_api_key
    model = st.session_state.model

    placeholder.write(f"Generating learning context...")
    st.markdown("First we generate a *learning context* document based on your learning goals and current skills. It asks the LLM to think through a learning trajectory for you with sub goals, topics to focus on, and problems you might encounter:")
    learning_context = generate_learning_context(goals=goals, skills=skills, model=model, _openai_api_key=openai_api_key)
    st.session_state.learning_context = learning_context
    st.expander("Learning Context generated :white_check_mark:").write(learning_context)

    placeholder.write(f"Generating key topics...")
    st.markdown("Next, we generate a set of key topics from the source material you provided to break the quiz into relevant sections:")
    key_topics = generate_key_topics(source_material=source_material, model=model, _openai_api_key=openai_api_key)
    st.session_state.key_topics = key_topics
    st.expander("Key Topics generated :white_check_mark:").write(key_topics)

    placeholder.empty()
    st.markdown("Finally, we generate a set of questions based on each key topic, with each one contextualized for you personally depending on whether your answer was right or wrong:")
    st.header("Quiz:")
    current_quiz_section()

with col2:
    goals = st.session_state.goals
    skills = st.session_state.skills
    source_material = st.session_state.source_material
    openai_api_key = st.session_state.openai_api_key
    if goals == '' or skills == '' or source_material == '' or openai_api_key == '':
        st.warning("Please fill in all fields.")
    else:
        quiz()

