prefix = """
You should answer the following questions with up-to-date information. You have access to the following tools:"""

format_instruction = """You must use the following format for all responses or your response will be considered incorrect:

Question: the input question you must answer

Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action in a single sentence.
... (this Thought/Action/Action Input/Observation can repeat N times but Question should only appear once)
Thought: I now know the final answer
Final Answer: the final answer to the original input question
If you do not know the answer, you can say so.
"""

suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}

"""
zero_shot_prompt = {
    "prefix": prefix,
    "format_instruction": format_instruction,
    "suffix": suffix,
}
