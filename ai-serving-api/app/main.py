import os
import secrets

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain.memory import MongoDBChatMessageHistory




load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/inference/")
async def inference(request: Request):
    TOKEN_LENGTH = 16
    token = request.query_params.get("token")
    token = token if token and len(token) == TOKEN_LENGTH else secrets.token_urlsafe(TOKEN_LENGTH)
    
    
    
    
    return {"message": "Hello World"}