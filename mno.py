

# from fastapi import FastAPI, Request
# from pydantic import BaseModel
# import openai
# import os, uvicorn, requests
# from fastapi.middleware.cors import CORSMiddleware

# # Initialize FastAPI app
# app = FastAPI()

# # Enable CORS for Streamlit frontend
# origins = [
#     "http://localhost",  # Streamlit default
#     "http://localhost:8501",  # Streamlit default port
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # GPT API Key (Set your OpenAI GPT API Key here)
# openai_api_key = os.getenv("OPENAI_API_KEY")

# # Request model
# class QueryRequest(BaseModel):
#     question: str

# # Route to handle QA
# @app.post("/ask")
# async def ask_question(query: QueryRequest):
#     try:
#         # Use OpenAI GPT API to get a response
#         response = requests.post(
#                     url="https://api.openai.com/v1/chat/completions",
#                     headers={
#                         "Content-Type": "application/json",
#                         "Authorization": f"Bearer {openai_api_key}",
#                     },
#                     json={
#                         "model": "gpt-4o-mini",  # Update to a valid model
#                         "messages": [
#                             {"role": "system", "content": "You are a helpful assistant."},
#                             {"role": "user", "content": query.question},  # Extract question
#                         ],
#                         "temperature": 0.2,
#                     },
#                 )

#         # Log full response for debugging
#         api_response = response.json()
#         print(api_response)  # Debugging log to see the whole response

#         # Extract the generated answer
#         if 'choices' in api_response:
#             answer = api_response['choices'][0]['message']['content']
#             return {"answer": answer}
#         else:
#             # Handle case where 'choices' is missing
#             return {"error": f"Invalid response from OpenAI API: {api_response}"}

#     except Exception as e:
#         return {"error": str(e)}
    
# if __name__ == "__main__":
#     uvicorn.run("app:app", host="localhost", port=8500, reload=True)


# from fastapi import FastAPI
# from pydantic import BaseModel
# import openai
# import os, uvicorn, requests
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

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

# class AnswerRequest(BaseModel):
#     answer: str

# # Endpoint to generate a new interview question
# @app.get("/generate_question")
# async def generate_question():
#     try:
#         response = requests.post(
#             url="https://api.openai.com/v1/chat/completions",
#             headers={
#                 "Content-Type": "application/json",
#                 "Authorization": f"Bearer {openai_api_key}",
#             },
#             json={
#                 "model": "gpt-4o-mini",  # Replace with a valid model
#                 "messages": [
#                     {"role": "system", "content": "You are an interviewer asking technical questions."},
#                     {"role": "assistant", "content": "Please ask a new interview question."}
#                 ],
#                 "temperature": 0.5,
#             },
#         )
#         api_response = response.json()
#         question = api_response['choices'][0]['message']['content']
#         return {"question": question}

#     except Exception as e:
#         return {"error": str(e)}

# # Endpoint to receive user answers
# @app.post("/submit_answer")
# async def submit_answer(answer_request: AnswerRequest):
#     # Here, you could add logic to process the answer if needed
#     return {"message": "Answer received. Preparing next question."}

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="localhost", port=8500, reload=True)



# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import openai
# import os, uvicorn, requests
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

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

# class QuestionResponse(BaseModel):
#     question: str

# # Generate a new interview question
# @app.get("/generate_question", response_model=QuestionResponse)
# async def generate_question():
#     try:
#         response = requests.post(
#             url="https://api.openai.com/v1/chat/completions",
#             headers={
#                 "Content-Type": "application/json",
#                 "Authorization": f"Bearer {openai_api_key}",
#             },
#             json={
#                 "model": "gpt-4",  # Replace with a valid model
#                 "messages": [
#                     {"role": "system", "content": "You are an interviewer asking technical questions."},
#                     {"role": "assistant", "content": "Please ask a new interview question."}
#                 ],
#                 "temperature": 0.5,
#             },
#         )
#         response.raise_for_status()
#         api_response = response.json()
#         question = api_response['choices'][0]['message']['content']
#         return {"question": question}

#     except Exception as e:
#         return {"error": str(e)}

# # Evaluate the user's answer and provide feedback
# @app.post("/submit_answer")
# async def submit_answer(answer_request: AnswerRequest):
#     try:
#         # Call the OpenAI API
#         response = requests.post(
#             url="https://api.openai.com/v1/chat/completions",
#             headers={
#                 "Content-Type": "application/json",
#                 "Authorization": f"Bearer {openai_api_key}",
#             },
#             json={
#                 "model": "gpt-4",  # Use a valid model
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

#         # Extract and normalize the evaluation
#         evaluation = api_response['choices'][0]['message']['content'].strip().lower()

#         # Enhanced logic to evaluate the response
#         if "yes" in evaluation:
#             return {
#                 "is_correct": True,
#                 "evaluation": "Correct! Good job.",
#                 "next_question_allowed": True
#             }
#         elif "no" in evaluation:
#             return {
#                 "is_correct": False,
#                 "evaluation": "Incorrect. Please try again.",
#                 "next_question_allowed": False
#             }
#         else:
#             return {
#                 "is_correct": False,
#                 "evaluation": "Unexpected response. Please try again later.",
#                 "next_question_allowed": False
#             }

#     except requests.exceptions.RequestException as e:
#         raise HTTPException(status_code=500, detail=f"Request failed: {e}")
#     except KeyError as e:
#         raise HTTPException(status_code=500, detail=f"Unexpected response format: {e}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="localhost", port=8500, reload=True)


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import openai
# import os, uvicorn, requests
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

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

# class QuestionResponse(BaseModel):
#     question: str

# # Track user progress (in-memory storage for simplicity)
# user_progress = {
#     "total_questions": 10,
#     "questions_asked": 0,
#     "correct_answers": 0,
#     "question_list": []
# }

# # Generate a new interview question
# @app.get("/generate_question", response_model=QuestionResponse)
# async def generate_question():
#     try:
#         if user_progress["questions_asked"] >= user_progress["total_questions"]:
#             return {"question": "You have completed the interview!"}

#         response = requests.post(
#             url="https://api.openai.com/v1/chat/completions",
#             headers={
#                 "Content-Type": "application/json",
#                 "Authorization": f"Bearer {openai_api_key}",
#             },
#             json={
#                 "model": "gpt-4",
#                 "messages": [
#                     {"role": "system", "content": "You are an interviewer asking technical questions."},
#                     {"role": "assistant", "content": "Please ask a new interview question."}
#                 ],
#                 "temperature": 0.5,
#             },
#         )
#         response.raise_for_status()
#         api_response = response.json()
#         question = api_response['choices'][0]['message']['content']
        
#         user_progress["questions_asked"] += 1
#         user_progress["question_list"].append(question)

#         return {"question": question}

#     except Exception as e:
#         return {"error": str(e)}

# # Evaluate the user's answer and provide feedback
# @app.post("/submit_answer")
# async def submit_answer(answer_request: AnswerRequest):
#     try:
#         response = requests.post(
#             url="https://api.openai.com/v1/chat/completions",
#             headers={
#                 "Content-Type": "application/json",
#                 "Authorization": f"Bearer {openai_api_key}",
#             },
#             json={
#                 "model": "gpt-4",
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


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os, uvicorn, requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

# Track user progress (in-memory storage for simplicity)
user_progress = {
    "total_questions": 10,
    "questions_asked": 0,
    "correct_answers": 0,
    "question_list": []
}

# # Generate a new interview question
# @app.get("/generate_question", response_model=QuestionResponse)
# async def generate_question():
#     try:
#         if user_progress["questions_asked"] >= user_progress["total_questions"]:
#             return {"question": "You have completed the interview!"}

#         response = requests.post(
#             url="https://api.openai.com/v1/chat/completions",
#             headers={
#                 "Content-Type": "application/json",
#                 "Authorization": f"Bearer {openai_api_key}",
#             },
#             json={
#                 "model": "gpt-4",
#                 "messages": [
#                     {"role": "system", "content": "You are an interviewer asking technical questions."},
#                     {"role": "assistant", "content": "Please ask a new interview question."}
#                 ],
#                 "temperature": 0.5,
#             },
#         )
#         response.raise_for_status()
#         api_response = response.json()
#         question = api_response['choices'][0]['message']['content']
        
#         user_progress["questions_asked"] += 1  # Increment questions asked when a new question is retrieved
#         user_progress["question_list"].append(question)

#         return {"question": question}

#     except Exception as e:
#         return {"error": str(e)}

@app.get("/generate_question", response_model=dict)
async def generate_question():
    try:
        if user_progress["questions_asked"] >= 10:  # Stop if 10 questions have been asked
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
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "You are an interviewer asking technical questions."},
                    {"role": "assistant", "content": "Please ask a new interview question. do not repeated the same questions"}
                ],
                "temperature": 0.5,
            },
        )
        response.raise_for_status()
        api_response = response.json()
        question = api_response['choices'][0]['message']['content']
        
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
                "model": "gpt-4",
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
