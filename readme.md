# [CompassUTD🧭](https://compass-utd.vercel.app/)

An unofficial advisor chatbot that provide accurate and up-to-date information about The University of Texas at Dallas powered by Langchain 🦜️🔗 and Google's PaLM 2.

## Features

You can do all of this with CompassUTD🧭

- Search for courses using natural language and short-hand name
- Get rating for professors at UT Dallas from RateMyProfessors.com
- Get information about UT Dallas' offered majors and minors
- Get UT Dallas general information like tech support, parking, and more
- Get information about staff, school and department(e.g. contact infromation, office location, hours, etc.)
- Be informed about the latest news and events at UT Dallas
- And more to come!

## Architecture

### High level architecture diagram

![image](static/architecture_diagram.png)

### How does it work

1. The user first interacts with the chatbot through the web app.
2. The web app sends the user's message and a sessionId token to the FastAPI server deployed on Cloud Run.
3. The FastAPI then check MongoDB to see if the user has previous message in the database.
4. Vertex AI's PaLM 2 mode will receive the current message and previous message stored in MongoDB.
5. With the current and previous message, it will design the plan to achieve the response
6. Vertex AI's PaLM 2 will then execute it's plan through Langchain's microservices deployed on same Cloud Run instance.
7. If the response is not sastifiable, step 5-6 will be repeated until the response is sastifiable or timeout.
8. The response will be sent back to the FastAPI server and the webapp can call the FastAPI server for result.

By doing this, the chatbot achieve a very high accuracy. It also able to remember the context of the conversation and able to provide a more personalized experience.

## Getting started with local testing

If you are interested in the frontend, check out [Arihan's frontend github repo](https://github.com/arihanv/CompassUTD)

Here are the steps to run this project locally or deploy it to Google Cloud Platform

1. Create a Google Cloud Platform account and enable Vertex AI and the required APIs for the project. Then create a service account, and save it API service account key as `google_key.json` and put it in `train-and-finetune` and `fast_api_app/app` folder.

2. Create a MongoDB Atlas account and create a cluster Save the connection string as `MONGODB_LOGIN` and `MONGODB_LOCATION` for later.

3. Get the API key to perform the search. Then create 3 search engines that match the following and save individual `Search Engine ID`:

|                | Course Search <img width=200/>| Degree Search <img width=200/>| Random Search <img width=200/>|
|----------------|--------------------------|-------------------------------|-------------------------------|
| Search sites   | - catalog.utdallas.edu/<br/>\*/\*/courses/***** | - catalog.utdallas.edu/<br/>202*/\*/programs/\*/*  | - catalog.utdallas.edu/\*/\*/home/* <br/> - bpb-us-e2.wpmucdn.com/sites.utdallas.edu/* <br/> - \*.utdallas.edu/* |
| Excluded sites | - catalog.utdallas.edu/<br/>\*/\*/courses/school/*  | *None* | - dox.utdallas.edu/syl*<br/>- catalog.utdallas.edu/* |

4. You have all the required information to create a `.env` file. Create a .env file in the `fast_api_app/app` and `train-and-finetune` folder with the following content. Replace the values with your own.

```
MONGODB_LOGIN = `REPLACE`
MONGODB_LOCATION = `REPLACE`

GOOGLE_APPLICATION_CREDENTIALS = google_key.json
GOOGLE_SEARCH_API = `REPLACE`
COURSE_SEARCH_ID = `REPLACE`
RANDOM_SEARCH_ID = `REPLACE`
DEGREE_SEARCH_ID = `REPLACE`
```

5. Now you should be able to run the project locally in `train-and-finetune/ai_sandbox.ipynb`.

6. If you would like to run the FastAPI server. Run the following commands in the terminal.

```
cd fast_api_app

# For in browser testing
uvicorn app.main:app --reload

# For Docker Container testing
local_docker_test.cmd

# For Google Cloud Run deployment
deploy_to_cloud_run.cmd
```

7. Have fun! Open a GitHub issue if you have any questions.
