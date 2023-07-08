from CompassUTD.langchain.agent import CompassAgent
from CompassUTD.langchain.toolkit import CompassToolkit
from CompassUTD.prompt import filter_template, result_template


from google.cloud import aiplatform

from langchain import PromptTemplate, LLMChain
from langchain.llms import VertexAI
from langchain.memory import ReadOnlySharedMemory


class CompassInference:
    def __init__(self, llm=None) -> None:
        if not llm:
            aiplatform.init(project="aerobic-gantry-387923", location="us-central1")

            self.llm = VertexAI(temperature=0, max_tokens=1024, top_p=0.95, top_k=40)

        self.tools = CompassToolkit().get_tools()

    def run(self, user_message: str, read_only_memory: ReadOnlySharedMemory) -> str:

        self._setup_langchain(read_only_memory)

        filter_answer = (
            self.filter_chain.run(user_message=user_message)
        ) 

        if "ENARC!" not in filter_answer:
            return filter_answer
        
        agent_action_result = self.langchain_agent.run(user_message)
        

        result = (
            self.result_chain.run(user_message=user_message, research_result=agent_action_result)
        ) 

        bot_message = result

        return bot_message

    def _setup_langchain(self, read_only_memory):

        self.filter_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template(filter_template),
            memory=read_only_memory,
        )

        self.langchain_agent = CompassAgent(
            llm=self.llm, tools=self.tools, memory=read_only_memory
        )

        self.result_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template(result_template),
            memory=read_only_memory,
        )
