json_example = """{ "questions": [ {
"questionTitle": "<QUESTION TITLE>", 
"answers": ["<ANSWER 1>","<ANSWER 2>","<ANSWER 3>","<ANSWER 4>"], 
"answerIndex": <CORRECT ANSWER INDEX>, 
"reasoning": "<CORRECT ANSWER REASONING>",
"context_relevance": "<LEARNING CONTEXT RELEVANCE>",
"requisite_knowledge": "<HOW TO GET THE RIGHT ANSWER>",
"follow_up_knowledge": "<WHAT TO LEARN NEXT>, }, ... ], }"""

def questions_prompt(*, for_key_topic, learning_context, source_material):
    return f"""
I am engaged in a learing project, the context of which is described below:
<learningContext>
{learning_context}
</learningContext>

I am reading the following source material and would like a quiz to test my understanding:
<sourceMaterial>
{source_material}
</sourceMaterial>

I'm studying a series of topics. For now focus on exclusively this one: "{for_key_topic}"

Using the learning context and the source material, generate 3-6 multiple choice questions. Generate more questions for more complex or important topics in the source material, and fewer questions for less important or less complex topics.

Each question also has four blurbs: 
1. Explain why this is the correct answer versus the other options ("reasoning")
2. Given the learning context, explain why this question is relevant or not. Refer to specifics from the learning context. It motivates me to learn when I see why it matters to my goals. ("context_relevance")
3. If get the wrong answer, describe what I should to to learn the requisite knowledge ("requisite_knowledge")
4. If I get the right answer, describe what I should do next given my learning context ("follow_up_knowledge")
 
Example JSON output using placeholders: {json_example}"""
