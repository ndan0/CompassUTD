import os
import secrets

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain.memory import ReadOnlySharedMemory, MongoDBChatMessageHistory, ConversationBufferWindowMemory
from langchain.schema.messages import AIMessage, HumanMessage

load_dotenv()

from CompassUTD import CompassInference


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


TOKEN_LENGTH = 16

connection_string = f"mongodb+srv://{str(os.getenv('MONGODB_LOGIN'))}@{str(os.getenv('MONGODB_LOCATION'))}"

LocalCompassInference = CompassInference()


@app.post("/inference/")
async def inference(request: Request):
    """_summary_

    Args:
        request (Request): 2 parameters: token(not required but needed for history) and user_message(always required)

    Raises:
        HTTPException: If user_message is empty or invalid

    Returns:
        JSON: token number (if not provided, it will be generated), and bot message
    """

    token = request.query_params.get("token")
    user_message = request.query_params.get("user_message")

    # Check if message is valid and not just empty or whitespace
    user_message = (
        user_message if user_message and len(user_message.strip()) > 0 else None
    )

    if not user_message:
        raise HTTPException(status_code=400, detail="Empty or invalid message")

    # Check if there is token, if not, generate one
    token = (
        token
        if token and len(token) == TOKEN_LENGTH
        else secrets.token_urlsafe(TOKEN_LENGTH)
    )
    # get the first 16 characters of the token
    token = token[:TOKEN_LENGTH]

    #Make sure the message is not too long
    
    
    # Connect to MongoDB
    message_history = MongoDBChatMessageHistory(
        connection_string=connection_string, session_id=token
    )
    
    memmory_store = ConversationBufferWindowMemory(memory_key="chat_history",chat_memory=message_history)

    read_only_memory = ReadOnlySharedMemory(memory=memmory_store)

    try:
        bot_message = LocalCompassInference.run(user_message, read_only_memory)
    except Exception as e:
        bot_message = "Something go wrong. Try again later! Error: " + str(e)
        
    if bot_message == "MALICIOUS":
        user_message = "REDACTED - Reason: Malicious or inappropriate content"
        bot_message = "Please do not use this tool for inappropriate purposes. If you believe this is a mistake, please contact the developers."
    elif bot_message == "TOO_LONG":
        user_message = "REDACTED - Reason: Too long"
        bot_message = "Your query is too long. Could you kindly repharse your question?."
        
    message_history.add_user_message(user_message)
    message_history.add_ai_message(bot_message)
    

    return {"token": token, "bot_message": bot_message}


@app.get("/get_messages/{token}")
async def get_messages(token: str):
    # Connect to MongoDB

    message_history = MongoDBChatMessageHistory(
        connection_string=connection_string, session_id=token
    )

    results = []
    for message in message_history.messages:
        if isinstance(message, AIMessage):
            results.append({"bot_message": message.content})
        elif isinstance(message, HumanMessage):
            results.append({"user_message": message.content})

    return results
