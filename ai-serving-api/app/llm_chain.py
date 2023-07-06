import os
from dotenv import load_dotenv
from langchain_agent import run_langchain_agent
from langchain.memory import ConversationBufferMemory, MongoDBChatMessageHistory
from langchain.schema.messages import (
    AIMessage,
    HumanMessage,
) 

load_dotenv()

def llm_inference(user_message, message_history):

    bot_memory = ConversationBufferMemory(memory_key="chat_history")

    for message in message_history.messages:
        if isinstance(message, AIMessage):
            bot_memory.chat_memory.add_ai_message(message.content)
        elif isinstance(message, HumanMessage):
            bot_memory.chat_memory.add_user_message(message.content)
    
    bot_message = run_langchain_agent(user_message, bot_memory)
    
    
    return bot_message
