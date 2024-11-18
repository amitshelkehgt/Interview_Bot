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
 
# Generate a new interview question
@app.get("/generate_question", response_model=QuestionResponse)
async def generate_question():
    try:
        response = requests.post(
            url="https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_api_key}",
            },
            json={
                "model": "gpt-4",  # Replace with a valid model
                "messages": [
                    {"role": "system", "content": "You are an interviewer asking technical questions."},
                    {"role": "assistant", "content": "Please ask a new interview question."}
                ],
                "temperature": 0.5,
            },
        )
        response.raise_for_status()
        api_response = response.json()
        question = api_response['choices'][0]['message']['content']
        return {"question": question}
 
    except Exception as e:
        return {"error": str(e)}
 
# Evaluate the user's answer and provide feedback
@app.post("/submit_answer")
async def submit_answer(answer_request: AnswerRequest):
    try:
        # Call the OpenAI API
        response = requests.post(
            url="https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_api_key}",
            },
            json={
                "model": "gpt-4",  # Use a valid model
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
 
        # Extract and normalize the evaluation
        evaluation = api_response['choices'][0]['message']['content'].strip().lower()
 
        # Enhanced logic to evaluate the response
        if "yes" in evaluation:
            return {
                "is_correct": True,
                "evaluation": "Correct! Good job.",
                "next_question_allowed": True
            }
        elif "no" in evaluation:
            return {
                "is_correct": False,
                "evaluation": "Incorrect. Please try again.",
                "next_question_allowed": False
            }
        else:
            return {
                "is_correct": False,
                "evaluation": "Unexpected response. Please try again later.",
                "next_question_allowed": False
            }
 
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Unexpected response format: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
 
if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8500, reload=True)