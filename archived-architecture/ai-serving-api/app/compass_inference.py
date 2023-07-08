import os

from compass_agent import CompassAgent
from compass_toolkit import CompassToolkit

from dotenv import load_dotenv

from google.cloud import aiplatform

from langchain.llms import VertexAI
from langchain.memory import ConversationBufferMemory, MongoDBChatMessageHistory
from langchain.schema.messages import AIMessage, HumanMessage

load_dotenv()


class CompassInference:
    def __init__(self) -> None:
        aiplatform.init(project="aerobic-gantry-387923", location="us-central1")
        self.vertex = VertexAI(temperature=0, max_tokens=1024, top_p=0.95, top_k=40)
        self.tools = CompassToolkit().get_tools()

    def _run(self, user_message: str, mongodb_past_history) -> str:
        clone_memory = self.clone_message_history(mongodb_past_history)
        agent = CompassAgent(llm=self.vertex, tools=self.tools, memory=clone_memory)

        bot_message = agent._run(user_message)

        return bot_message

    def clone_message_history(
        self, message_history: MongoDBChatMessageHistory
    ) -> ConversationBufferMemory:
        memory_clone = ConversationBufferMemory(memory_key="chat_history")
        try:
            for message in message_history.messages:
                if isinstance(message, AIMessage):
                    memory_clone.chat_memory.add_ai_message(message.content)
                elif isinstance(message, HumanMessage):
                    memory_clone.chat_memory.add_user_message(message.content)
        except Exception as e:
            pass

        return memory_clone
