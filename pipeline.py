import streamlit as st
from openai import OpenAI
import json
from prompts.key_topics import key_topics_prompt
from prompts.learning_context import learning_context_prompt
from prompts.quiz_topic_questions import questions_prompt

def run_pipeline(*, goals, skills, source_material, model, openai_api_key, placeholder):
    client = OpenAI(api_key=openai_api_key)
    placeholder.write("Extracting key topics...")
    key_topics = extract_key_topics(source_material=source_material, model=model, _client=client)
    placeholder.write("Generating learning context...")
    learning_context = generate_learning_context(goals=goals, skills=skills, model=model, _client=client)
    placeholder.write("Generating quiz...")
    quiz = generate_quiz(key_topics=key_topics, learning_context=learning_context, source_material=source_material, model=model, _client=client, _placeholder=placeholder)
    return key_topics, learning_context, quiz

@st.cache_data(persist="disk")
def extract_key_topics(*, source_material, model, _client):
    prompt = key_topics_prompt(source_material = source_material)
    response = _client.chat.completions.create(
        model= model,
          response_format={ "type": "json_object" },
          messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
          ],
        temperature=0
    )
    body = response.choices[0].message.content
    with st.expander("key topics extracted :white_check_mark:"):
        st.write(body)
    return body

@st.cache_data(persist="disk")
def generate_learning_context(*, goals, skills, model, _client):
    prompt = learning_context_prompt(goals=goals, skills=skills)
    response = _client.chat.completions.create(
        model= model,
          messages=[
            {"role": "user", "content": prompt}
          ],
        temperature=0.4
    )
    learning_context = response.choices[0].message.content
    with st.expander("learning context generated :white_check_mark:"):
        st.write(learning_context)
    return learning_context

def generate_quiz(*, key_topics, learning_context, source_material, model, _client, _placeholder):
    quiz = {"keyTopics": []}
    parsed_topics = json.loads(key_topics)
    parsed_topics["topics"].insert(0, "Overview") # insert an "overview" topic
    parsed_topics["topics"] = parsed_topics["topics"][:2] # trim to just two topics for testing
    for key_topic in parsed_topics["topics"]:
        _placeholder.write(f"Generating questions for {key_topic}...")
        questions = generate_questions(key_topics=key_topics, for_key_topic=key_topic, learning_context=learning_context, source_material=source_material, model=model, _client=_client)
        parsed_questions = json.loads(questions)
        quiz["keyTopics"].append({"keyTopic": key_topic, "questions": parsed_questions["questions"]})
    body = json.dumps(quiz)
    with st.expander("quiz json generated :white_check_mark:"):
        st.write(body)
    return body

@st.cache_data(persist="disk")
def generate_questions(*, key_topics, for_key_topic, learning_context, source_material, model, _client):
    prompt = questions_prompt(for_key_topic=for_key_topic, learning_context=learning_context, source_material=source_material)
    response = _client.chat.completions.create(
        model= model,
          response_format={ "type": "json_object" },
          messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
          ],
          #max_tokens= 4096,
        temperature=0.3
    )
    json = response.choices[0].message.content
    return json

