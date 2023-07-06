
import os

import requests
from dotenv import load_dotenv

from google.cloud import aiplatform
from langchain import LLMChain
from langchain.agents import (AgentExecutor, AgentType, Tool, ZeroShotAgent,
                              initialize_agent)
from langchain.llms import VertexAI
from langchain.memory import ConversationBufferMemory

load_dotenv()

#! Change the following to your own project and location
aiplatform.init(project="aerobic-gantry-387923", location="us-central1")
vertex = VertexAI()



import Tools

agent_tools = Tools.Tools()

tools = [
    
    Tool(
        name = "Degree Search",
        func = agent_tools.get_degrees_from_query,
        description = "This tool allows you to search for UT Dallas' Degrees, Majors, Minors, and Certificates using keywords. It returns multiple titles, snippet and URLs that you can use extract text tool on.",
    ),
    Tool(
        name = "Course Search",
        func = agent_tools.get_courses_from_query,
        description = "This tool enables you to search for UT Dallas' courses using keywords. Use this tool to compare multiple courses. It returns multiple titles, snippet and URLs that you can use extract text tool on.",
    ),

    Tool(
        name = "General Search",
        func = agent_tools.utdallas_search,
        description = "Please use this tool only as a last resort. It performs a comprehensive search across all UT Dallas pages that will not give information about courses or degrees. It returns multipl possible titles, snippet and URLs that you can use extract text tool on.",
    ),
    Tool(
        name = "Extract Text from UT Dallas Site",
        func = agent_tools.access_utdallas_site,
        description = "If you have a URL string containing utdallas.edu, use this function to extract the text content from that page.",
    ),
    Tool(
        name = "Dictionary",
        func = agent_tools.dictionary_search,
        description = "If you need the definition of a word or phrase unrelated to UT Dallas, use this function to retrieve the definition. Do not use for anything related to UT Dallas only information.",
    )
]


prefix = """
You should answer the following questions with up-to-date information or as best as you can. You have access to the following tools:"""

format_instruction = """You must use the following format for all responses or your response will be considered incorrect:

Question: the input question you must answer

Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action in a single sentence
... (this Thought/Action/Action Input/Observation can repeat N times but Question should only appear once)
Thought: I now know the final answer
Final Answer: the final answer to the original input question.
If you do not know the answer, you can say so.
"""

suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}

"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    format_instructions=format_instruction,
    input_variables=["input", "chat_history", "agent_scratchpad"],

)


def run_langchain_agent(user_message: str, mongoDB_memory):
    

    llm_chain = LLMChain(llm=vertex, prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
    agent_chain = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        memory=mongoDB_memory,
        handle_parsing_errors=False,
    )

    try:
        response = agent_chain.run(input=user_message)
    except ValueError as e:
        response = str(e)
        prefix = "Could not parse LLM output: `"
        if not response.startswith("Could not parse LLM output: `"):
            return "There was an error with the agent. Ignore it output."
        response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
    
    return str(response)
