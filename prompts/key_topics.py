json_example = '{"topics":["<INSERT TOPIC 1>","<INSERT TOPIC 2>", ...<ADD MORE TOPICS>...]}'

def key_topics_prompt(*, source_material):
    return f"""
Extract a list of key topics from the following source material. Limit to 10 topics, using higher-level topics as necessary to ensure coverage if there are more than that.

Example JSON output using placeholders:
{json_example}

<sourceMaterial>
{source_material}
</sourceMaterial>"""
