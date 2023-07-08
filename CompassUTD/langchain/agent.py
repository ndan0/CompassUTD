from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain import LLMChain

from CompassUTD.langchain.prompt import zero_shot_prompt


def error_handler(e):
    response = str(e)
    prefix = "Could not parse LLM output: `"
    if not response.startswith(prefix):
        raise e
    response = response.removeprefix(prefix).removesuffix("`")
    return response


class CompassAgent:
    def __init__(self, llm, tools, memory) -> None:
        self.prompt = ZeroShotAgent.create_prompt(
            tools=tools,
            prefix=zero_shot_prompt["prefix"],
            suffix=zero_shot_prompt["suffix"],
            format_instructions=zero_shot_prompt["format_instruction"],
            input_variables=["input", "chat_history", "agent_scratchpad"],
        )
        llm_chain = LLMChain(llm=llm, prompt=self.prompt)
        agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
        self.agent_chain = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=tools,
            verbose=True,
            memory=memory,
            handle_parsing_errors=False,
            early_stopping_method = "generate",
            max_execution_time=10,
        )

    def run(self, input: str) -> str:
        try:
            return self.agent_chain.run(input=input)
        except ValueError as e:
            return error_handler(e)

    async def arun(self, input: str) -> str:
        try:
            return self.agent_chain.arun(input=input)
        except ValueError as e:
            return error_handler(e)
