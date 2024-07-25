def learning_context_prompt(*, goals, skills):
    return f"""
I'm engaged in a learning project. My goals and my current skill level are below. Given these, please think through some sub-goals, essential skills and topics to focus on, and problems that I might encounter. Skip preamble and jump right into the outline.

<goals>
{goals}
</goals>

<current_skill_level>
{skills}
</current_skill_level
"""
