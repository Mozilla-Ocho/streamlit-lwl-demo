import json

json_example = """{ "questions": [ {
"questionTitle": "What is the primary subject of the material?", 
"answers": ["cats","outer space","coffee","poetry"], 
"answerIndex": 2, 
"reasoning": "Coffee is the only choice that is mentioned by the document.",
"context_relevance": "Roasting your own coffee is a great way to develop loyal business as a new coffee shop owner",
"requisite_knowledge": "Go back and review the fundamentals of coffee preparation",
"follow_up_knowledge": "Learn next about coffee packaging and branding best practices", }, ... ], }"""

# a json schema specification for the example above:
# gpt4o doesn't actually seem to need this to produce the correct output, the example works and with fewer tokens.
json_schema = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "questionTitle": { "type": "string" },
                    "answers": {
                        "type": "array",
                        "items": { "type": "string" },
                        "minItems": 4,
                        "maxItems": 4
                    },
                    "answerIndex": { "type": "integer" },
                    "reasoning": { "type": "string" },
                    "context_relevance": { "type": "string" },
                    "requisite_knowledge": { "type": "string" },
                    "follow_up_knowledge": { "type": "string" }
                },
                "required": ["questionTitle", "answers", "answerIndex", "reasoning", "context_relevance", "requisite_knowledge", "follow_up_knowledge"]
            },
            "minItems": 3,
            "maxItems": 6
        }
    },
    "required": ["questions"]
}
json_schema = json.dumps(json_schema) # compact whitespace

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
 
Example JSON output is as follows: {json_example}"""
