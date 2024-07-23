import streamlit as st
from openai import OpenAI
import json
from prompts.key_topics import key_topics_prompt
from prompts.learning_context import learning_context_prompt
from prompts.quiz_topic_questions import questions_prompt

@st.cache_data(persist="disk")
def generate_key_topics(*, source_material, model, _openai_api_key):
    client = OpenAI(api_key=_openai_api_key)
    prompt = key_topics_prompt(source_material = source_material)
    response = client.chat.completions.create(
        model= model,
          response_format={ "type": "json_object" },
          messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
          ],
        temperature=0
    )
    body = response.choices[0].message.content
    topics = json.loads(body)["topics"] # prompt schema asks for this key
    topics.insert(0, "Overview") # insert "overview" as first topic
    return topics

@st.cache_data(persist="disk")
def generate_learning_context(*, goals, skills, model, _openai_api_key):
    client = OpenAI(api_key=_openai_api_key)
    prompt = learning_context_prompt(goals=goals, skills=skills)
    response = client.chat.completions.create(
        model= model,
          messages=[
            {"role": "user", "content": prompt}
          ],
        temperature=0.4
    )
    learning_context = response.choices[0].message.content
    return learning_context

@st.cache_data(persist="disk")
def generate_questions(*, for_key_topic, learning_context, source_material, model, _openai_api_key):
    client = OpenAI(api_key=_openai_api_key)
    prompt = questions_prompt(for_key_topic=for_key_topic, learning_context=learning_context, source_material=source_material)
    response = client.chat.completions.create(
        model= model,
          response_format={ "type": "json_object" },
          messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
          ],
          #max_tokens= 4096,
        temperature=0.3
    )
    body = response.choices[0].message.content
    questions = json.loads(body)["questions"]
    return questions

