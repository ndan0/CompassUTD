from CompassUTD.langchain.agent import CompassAgent
from CompassUTD.langchain.toolkit import CompassToolkit
from CompassUTD._secret import google_key_path

from google.cloud import aiplatform

from langchain.llms import VertexAI
from langchain.memory import ConversationBufferMemory, MongoDBChatMessageHistory
from langchain.schema.messages import AIMessage, HumanMessage


class CompassInference:
    def __init__(self, llm = None) -> None:
        if not llm:
            aiplatform.init(project="aerobic-gantry-387923", location="us-central1")

            self.llm = VertexAI(temperature=0, max_tokens=1024, top_p=0.95, top_k=40)

        self.tools = CompassToolkit().get_tools()

    def run(self, user_message: str, mongodb_past_history=None) -> str:
        clone_memory = self._clone_message_history(mongodb_past_history)
        agent = CompassAgent(llm=self.llm, tools=self.tools, memory=clone_memory)

        bot_message = agent._run(user_message)

        return bot_message

    def _clone_message_history(
        self, message_history: MongoDBChatMessageHistory
    ) -> ConversationBufferMemory:
        memory_clone = ConversationBufferMemory(memory_key="chat_history")
        if message_history:
            for message in message_history.messages:
                if isinstance(message, AIMessage):
                    memory_clone.chat_memory.add_ai_message(message.content)
                elif isinstance(message, HumanMessage):
                    memory_clone.chat_memory.add_user_message(message.content)

        return memory_clone
