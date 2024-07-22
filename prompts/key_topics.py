import json

json_example = '{"topics":["Survey of modern coffee roasting techniques","Roasting at high volume",...]}'

json_schema = '''
{
    "type": "object",
    "properties": {
        "topics": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "minItems": 3,
            "maxItems": 10
        }
    },
    "required": ["topics"]
}
'''
json_schema = json.dumps(json.loads(json_schema)) # compact whitespace

def key_topics_prompt(*, source_material):
    return f"""
Extract a list of key topics from the following source material. Limit to 10 topics, using higher-level topics as necessary to ensure coverage if there are more than that.

Respond with JSON with this schema:
{json_schema}

Example JSON:
{json_schema}

<sourceMaterial>
{source_material}
</sourceMaterial>"""
