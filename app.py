from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os, uvicorn, requests
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
 
app = FastAPI()

db_url = os.getenv("db_url")
db_name = os.getenv("db_name")
db_client = MongoClient(db_url)
db = db_client[db_name]
 
# CORS setup
origins = ["http://localhost", "http://localhost:8501"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
 
# Request and response models
class AnswerRequest(BaseModel):
    question: str
    answer: str
 
class QuestionResponse(BaseModel):
    question: str
 
user_progress = {
    "total_questions": 10,
    "questions_asked": 0,
    "correct_answers": 0,
    "question_list": []
}
 
 
@app.get("/generate_question", response_model=dict)
async def generate_question():
    try:
        if user_progress["questions_asked"] >= 10:  # Stop if 10 questions have been asked

            document ={
                "total_questions":user_progress["total_questions"],
                "correct_answers":user_progress["correct_answers"],
                "questions_asked": user_progress["questions_asked"],
                "session_id":None
            }
            db["interview_status"].insert_one(document)

            return {
                "question": "You have completed the interview!",
                "questions_asked": user_progress["questions_asked"]
            }
 
        response = requests.post(
            url="https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_api_key}",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are an interviewer asking technical questions."},
                    {"role": "assistant", "content": "Please ask a new interview question. please do not repeated the same questions"}
                ],
                "temperature": 0.5,
            },
        )
        response.raise_for_status()
        api_response = response.json()
        question = api_response['choices'][0]['message']['content']
        print(question)
       
        user_progress["questions_asked"] += 1  # Increment questions asked
        user_progress["question_list"].append(question)
 
        return {
            "question": question,
            "questions_asked": user_progress["questions_asked"]
        }
 
    except Exception as e:
        return {"error": str(e)}
 
# Evaluate the user's answer and provide feedback
@app.post("/submit_answer")
async def submit_answer(answer_request: AnswerRequest):
    try:
        response = requests.post(
            url="https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_api_key}",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that evaluates answers to interview questions."
                    },
                    {
                        "role": "user",
                        "content": f"Interviewer_Question: {answer_request.question}\n"
                                   f"Candidate_Answer: {answer_request.answer}\n"
                                   "Is the Candidate_Answer correct? Please reply with 'Yes' or 'No'."
                    }
                ],
                "temperature": 0.2,
            },
        )
        response.raise_for_status()
        api_response = response.json()
 
        evaluation = api_response['choices'][0]['message']['content'].strip().lower()
        correct = "yes" in evaluation
 
        if correct:
            user_progress["correct_answers"] += 1  # Increment only for correct answers

        return {
            "is_correct": correct,
            "evaluation": "Correct! Good job." if correct else "Incorrect. Please try again.",
            "questions_asked": user_progress["questions_asked"],
            "correct_answers": user_progress["correct_answers"],
            "remaining_questions": user_progress["total_questions"] - user_progress["questions_asked"]
        }
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
 
if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8500, reload=True)


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import os, uvicorn, requests
# from fastapi.middleware.cors import CORSMiddleware
# from pymongo import MongoClient
# from neo4j import GraphDatabase

# app = FastAPI()

# # MongoDB setup
# db_url = os.getenv("db_url")
# db_name = os.getenv("db_name")
# db_client = MongoClient(db_url)
# db = db_client[db_name]

# # CORS setup
# origins = ["http://localhost", "http://localhost:8501"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # OpenAI API key
# openai_api_key = os.getenv("OPENAI_API_KEY")

# # Request and response models
# class AnswerRequest(BaseModel):
#     question: str
#     answer: str

# sessions ={} 

# neo4jdriver = GraphDatabase.driver(os.getenv("NEO4J_URI"), auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")))

# def get_data(sess,query):
#     result = sess.run(query)
#     record = result.data()
#     return record

# def get_session(session_id: str):
#     if session_id not in sessions:
#         sessions[session_id] = {
#             "total_questions": 10,
#             "questions_asked": 0,
#             "correct_answers": 0,
#             "question_list": []
#         }
#     return sessions[session_id]

# @app.get("/generate_question", response_model=dict)
# async def generate_question(email=None):
#     try:
#         if email==None:
#             return "Missing Data"
#         session = neo4jdriver.session()
#         with session.begin_transaction() as tx:
#             squery = f"""MATCH (p:Person {{email:"{email}"}})-[:HAS_SKILL]-(s:Skill) RETURN s.name"""
#             tx.run(squery)
#             skills = get_data(sess=session, query=squery)
#             print(skills)
#         user_progress = get_session(email)

#         if user_progress["questions_asked"] >= 10:            
#              # Stop if 10 questions have been asked
#             document = {
#                 "total_questions": user_progress["total_questions"],
#                 "correct_answers": user_progress["correct_answers"],
#                 "questions_asked": user_progress["questions_asked"],
#                 "email": email 
#             }
#             db["interview_status"].insert_one(document)

#             # del sessions[session_id]
#             return {
#                 "question": "You have completed the interview!",
#                 "questions_asked": user_progress["questions_asked"]
#             }

#         response = requests.post(
#             url="https://api.openai.com/v1/chat/completions",
#             headers={
#                 "Content-Type": "application/json",
#                 "Authorization": f"Bearer {openai_api_key}",
#             },
#             json={
#                 "model": "gpt-4o-mini",
#                 "messages": [
#                     {"role": "system", "content": f"You are an interviewer asking questions for a person with technical skills {skills}."},
#                     {"role": "assistant", "content": "Please ask a new interview question. Please do not repeat the same questions."}
#                 ],
#                 "temperature": 0.5,
#             },
#         )
#         response.raise_for_status()
#         api_response = response.json()
#         question = api_response['choices'][0]['message']['content']

#         user_progress["questions_asked"] += 1
#         user_progress["question_list"].append(question)

#         # Insert the question into the QA collection
#         db["QA"].insert_one({
#             "question": question,
#             "answer": None,
#             "status": "unanswered",
#             "email": email 
#         })

#         return {
#             "question": question,
#             "questions_asked": user_progress["questions_asked"]
#         }

#     except Exception as e:
#         return {"error": str(e)}

# @app.post("/submit_answer")
# async def submit_answer(answer_request: AnswerRequest,email):

#     try:
#         user_progress = get_session(email)
#         response = requests.post(
#             url="https://api.openai.com/v1/chat/completions",
#             headers={
#                 "Content-Type": "application/json",
#                 "Authorization": f"Bearer {openai_api_key}",
#             },
#             json={
#                 "model": "gpt-4o-mini",
#                 "messages": [
#                     {
#                         "role": "system",
#                         "content": "You are a helpful assistant that evaluates answers to interview questions."
#                     },
#                     {
#                         "role": "user",
#                         "content": f"Interviewer_Question: {answer_request.question}\n"
#                                    f"Candidate_Answer: {answer_request.answer}\n"
#                                    "Is the Candidate_Answer correct? Please reply with 'Yes' or 'No'."
#                     }
#                 ],
#                 "temperature": 0.2,
#             },
#         )
#         response.raise_for_status()
#         api_response = response.json()

#         evaluation = api_response['choices'][0]['message']['content'].strip().lower()
#         correct = "yes" in evaluation

#         if correct:
#             user_progress["correct_answers"] += 1

#         # Update the QA collection with the user's answer and evaluation
#         db["QA"].update_one(
#             {"question": answer_request.question},  # Match the question
#             {
#                 "$set": {
#                     "answer": answer_request.answer,
#                     "is_correct": correct,
#                     "evaluation": "Correct" if correct else "Incorrect",
#                     "status": "answered"
#                 }
#             }
#         )

#         return {
#             "is_correct": correct,
#             "evaluation": "Correct! Good job." if correct else "Incorrect. Please try again.",
#             "questions_asked": user_progress["questions_asked"],
#             "correct_answers": user_progress["correct_answers"],
#             "remaining_questions": user_progress["total_questions"] - user_progress["questions_asked"]
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="localhost", port=8500, reload=True)






