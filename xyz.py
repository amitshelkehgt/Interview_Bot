# import streamlit as st
# import requests

# # Set the FastAPI backend URL
# API_URL = "http://localhost:8500/ask"

# # Streamlit app title
# st.title("QA Chatbot")

# # Input field for the user to enter their question
# question = st.text_input("Enter your question:")

# # Button to submit the question
# if st.button("Ask"):
#     if question:
#         # Send the question to the FastAPI backend
#         try:
#             response = requests.post(API_URL, json={"question": question})
            
#             # Check if the request was successful
#             if response.status_code == 200:
#                 answer = response.json().get("answer", "Error: No answer received")
#                 st.write(f"Answer: {answer}")
#             else:
#                 st.write(f"Error: {response.status_code} - {response.text}")
        
#         except requests.exceptions.RequestException as e:
#             # Handle any errors that occur during the request
#             st.write(f"Error: {e}")
#     else:
#         st.write("Please enter a question.")


# import streamlit as st
# import requests

# API_URL_QUESTION = "http://localhost:8500/generate_question"
# API_URL_ANSWER = "http://localhost:8500/submit_answer"

# st.title("Interview Chatbot")

# # Button to start the interview
# if st.button("Start Interview"):
#     response = requests.get(API_URL_QUESTION)
#     if response.status_code == 200:
#         question = response.json().get("question", "Error: Could not retrieve question")
#         st.session_state["current_question"] = question
#     else:
#         st.write("Error: Could not start interview")

# # Display the current question if it exists in session state
# if "current_question" in st.session_state:
#     st.write(f"Question: {st.session_state['current_question']}")

#     # Input field for the user to answer
#     answer = st.text_input("Your Answer (2-3 lines):")

#     # Button to submit the answer
#     if st.button("Submit Answer"):
#         if answer:
#             # Send the answer to FastAPI
#             response = requests.post(API_URL_ANSWER, json={"answer": answer})
            
#             # Generate the next question after submission
#             next_question_response = requests.get(API_URL_QUESTION)
#             if next_question_response.status_code == 200:
#                 st.session_state["current_question"] = next_question_response.json().get("question", "No further questions available")
#             else:
#                 st.write("Error: Could not retrieve the next question")
#         else:
#             st.write("Please enter an answer.")



# import streamlit as st
# import requests

# API_URL_QUESTION = "http://localhost:8500/generate_question"
# API_URL_ANSWER = "http://localhost:8500/submit_answer"

# st.title("Interview Chatbot")

# # Initialize session state variables
# if "current_question" not in st.session_state:
#     st.session_state["current_question"] = None
# if "answer_feedback" not in st.session_state:
#     st.session_state["answer_feedback"] = ""
# if "next_question_allowed" not in st.session_state:
#     st.session_state["next_question_allowed"] = True

# # Button to start or proceed with the interview
# if st.session_state["next_question_allowed"] and st.button("Start Interview" if not st.session_state["current_question"] else "Next Question"):
#     response = requests.get(API_URL_QUESTION)
#     if response.status_code == 200:
#         question = response.json().get("question", "Error: Could not retrieve question")
#         st.session_state["current_question"] = question
#         st.session_state["answer_feedback"] = ""  # Clear feedback on next question
#         st.session_state["next_question_allowed"] = False  # Disable next until correct answer
#     else:
#         st.error("Error: Could not start interview")

# # Display the current question if available
# if st.session_state["current_question"]:
#     st.subheader(f"Question: {st.session_state['current_question']}")
    
#     # User enters their answer
#     answer = st.text_area("Your Answer (2-3 lines):", max_chars=300)
    
#     # Button to submit the answer
#     if st.button("Submit Answer"):
#         if answer.strip():  # Ensure non-empty answers
#             # API call to evaluate the answer
#             response = requests.post(API_URL_ANSWER, json={"question": st.session_state["current_question"], "answer": answer})
            
#             if response.status_code == 200:
#                 feedback = response.json()
#                 is_correct = feedback.get("is_correct", False)
#                 st.session_state["answer_feedback"] = feedback["evaluation"]

#                 # Color-coded feedback
#                 color = "green" if is_correct else "red"
#                 st.markdown(f"<span style='color: {color};'>{st.session_state['answer_feedback']}</span>", unsafe_allow_html=True)
                
#                 # Update the state based on correctness
#                 st.session_state["next_question_allowed"] = is_correct
#             else:
#                 st.error("Error: Could not evaluate the answer.")
#         else:
#             st.warning("Please provide a valid answer.")

# import streamlit as st
# import requests

# API_URL_QUESTION = "http://localhost:8500/generate_question"
# API_URL_ANSWER = "http://localhost:8500/submit_answer"

# st.title("Interview Chatbot")

# # Initialize session state variables
# if "current_question" not in st.session_state:
#     st.session_state["current_question"] = None
# if "answer_feedback" not in st.session_state:
#     st.session_state["answer_feedback"] = ""
# if "next_question_allowed" not in st.session_state:
#     st.session_state["next_question_allowed"] = True

# # Display the Start or Next Question button only if allowed
# if st.session_state["next_question_allowed"]:
#     if st.button("Start Interview" if not st.session_state["current_question"] else "Next Question"):
#         response = requests.get(API_URL_QUESTION)
#         if response.status_code == 200:
#             question = response.json().get("question", "Error: Could not retrieve question")
#             st.session_state["current_question"] = question
#             st.session_state["answer_feedback"] = ""  # Clear feedback
#             st.session_state["next_question_allowed"] = False  # Lock until correct answer
#         else:
#             st.error("Error: Could not start the interview")

# # Display the current question if available
# if st.session_state["current_question"]:
#     st.subheader(f"Question: {st.session_state['current_question']}")
    
#     # User input for the answer
#     answer = st.text_area("Your Answer (2-3 lines):", max_chars=300)
    
#     # Button to submit the answer
#     if st.button("Submit Answer"):
#         if answer.strip():  # Ensure non-empty answer
#             # API call to evaluate the answer
#             response = requests.post(API_URL_ANSWER, json={"question": st.session_state["current_question"], "answer": answer})
            
#             if response.status_code == 200:
#                 feedback = response.json()
#                 is_correct = feedback.get("is_correct", False)
#                 st.session_state["answer_feedback"] = feedback["evaluation"]

#                 # Display color-coded feedback
#                 color = "green" if is_correct else "red"
#                 st.markdown(f"<span style='color: {color};'>{st.session_state['answer_feedback']}</span>", unsafe_allow_html=True)
                
#                 # Update state based on correctness
#                 st.session_state["next_question_allowed"] = is_correct
#             else:
#                 st.error("Error: Could not evaluate the answer.")
#         else:
#             st.warning("Please provide a valid answer.")

#     # Display feedback
#     if st.session_state["answer_feedback"]:
#         st.write(st.session_state["answer_feedback"])


# import streamlit as st
# import requests

# API_URL_QUESTION = "http://localhost:8500/generate_question"
# API_URL_ANSWER = "http://localhost:8500/submit_answer"

# st.title("Interview Chatbot")

# # Initialize session state variables
# if "current_question" not in st.session_state:
#     st.session_state["current_question"] = None
# if "answer_feedback" not in st.session_state:
#     st.session_state["answer_feedback"] = ""
# if "next_question_allowed" not in st.session_state:
#     st.session_state["next_question_allowed"] = True

# # Display the "Start Interview" button only when no question has been asked
# if not st.session_state["current_question"] and st.button("Start Interview", key="start_interview"):
#     response = requests.get(API_URL_QUESTION)
#     if response.status_code == 200:
#         question = response.json().get("question", "Error: Could not retrieve question")
#         st.session_state["current_question"] = question
#         st.session_state["answer_feedback"] = ""  # Clear feedback on next question
#         st.session_state["next_question_allowed"] = False  # Disable next until correct answer
#     else:
#         st.error("Error: Could not start interview")

# # Display the current question if available
# if st.session_state["current_question"]:
#     st.subheader(f"Question: {st.session_state['current_question']}")
    
#     # User enters their answer
#     answer = st.text_area("Your Answer (2-3 lines):", max_chars=300)
    
#     # Button to submit the answer
#     if st.button("Submit Answer", key="submit_answer"):
#         if answer.strip():  # Ensure non-empty answers
#             # API call to evaluate the answer
#             response = requests.post(API_URL_ANSWER, json={"question": st.session_state["current_question"], "answer": answer})
            
#             if response.status_code == 200:
#                 feedback = response.json()
#                 is_correct = feedback.get("is_correct", False)
#                 st.session_state["answer_feedback"] = feedback["evaluation"]

#                 # Color-coded feedback
#                 color = "green" if is_correct else "red"
#                 st.markdown(f"<span style='color: {color};'>{st.session_state['answer_feedback']}</span>", unsafe_allow_html=True)
                
#                 # Update the state based on correctness
#                 st.session_state["next_question_allowed"] = is_correct
#             else:
#                 st.error("Error: Could not evaluate the answer.")
#         else:
#             st.warning("Please provide a valid answer.")

#     # Show "Next Question" button only after a correct answer
#     if st.session_state["next_question_allowed"]:
#         if st.button("Next Question", key="next_question"):
#             response = requests.get(API_URL_QUESTION)
#             if response.status_code == 200:
#                 question = response.json().get("question", "Error: Could not retrieve question")
#                 st.session_state["current_question"] = question
#                 st.session_state["answer_feedback"] = ""  # Clear feedback
#                 st.session_state["next_question_allowed"] = False
#             else:
#                 st.error("Error: Could not retrieve the next question.")



# import streamlit as st
# import requests

# API_URL_QUESTION = "http://localhost:8500/generate_question"
# API_URL_ANSWER = "http://localhost:8500/submit_answer"

# st.title("Interview Chatbot")

# # Initialize session state variables
# if "current_question" not in st.session_state:
#     st.session_state["current_question"] = None
# if "answer_feedback" not in st.session_state:
#     st.session_state["answer_feedback"] = ""
# if "next_question_allowed" not in st.session_state:
#     st.session_state["next_question_allowed"] = True
# if "correct_answers" not in st.session_state:
#     st.session_state["correct_answers"] = 0
# if "questions_asked" not in st.session_state:
#     st.session_state["questions_asked"] = 0
# if "remaining_questions" not in st.session_state:
#     st.session_state["remaining_questions"] = 10  # Default total questions

# if not st.session_state["current_question"] and st.button("Start Interview", key="start_interview"):
#     response = requests.get(API_URL_QUESTION)
#     if response.status_code == 200:
#         question = response.json().get("question", "Error: Could not retrieve question")
#         st.session_state["current_question"] = question
#         st.session_state["answer_feedback"] = ""  # Clear feedback on next question
#         st.session_state["next_question_allowed"] = False  # Disable next until correct answer
#     else:
#         st.error("Error: Could not start interview")

# if st.session_state["current_question"]:
#     st.subheader(f"Question: {st.session_state['current_question']}")
#     answer = st.text_area("Your Answer (2-3 lines):", max_chars=300)
    
#     if st.button("Submit Answer", key="submit_answer"):
#         if answer.strip():
#             response = requests.post(API_URL_ANSWER, json={"question": st.session_state["current_question"], "answer": answer})
#             if response.status_code == 200:
#                 feedback = response.json()
#                 st.session_state["correct_answers"] = feedback["correct_answers"]
#                 st.session_state["questions_asked"] = feedback["questions_asked"]
#                 st.session_state["remaining_questions"] = feedback["remaining_questions"]
#                 st.session_state["answer_feedback"] = feedback["evaluation"]
#                 is_correct = feedback.get("is_correct", False)
#                 color = "green" if is_correct else "red"
#                 st.markdown(f"<span style='color: {color};'>{st.session_state['answer_feedback']}</span>", unsafe_allow_html=True)
#                 st.session_state["next_question_allowed"] = is_correct
#             else:
#                 st.error("Error: Could not evaluate the answer.")
#         else:
#             st.warning("Please provide a valid answer.")

#     if st.session_state["next_question_allowed"]:
#         if st.button("Next Question", key="next_question"):
#             response = requests.get(API_URL_QUESTION)
#             if response.status_code == 200:
#                 question = response.json().get("question", "Error: Could not retrieve question")
#                 st.session_state["current_question"] = question
#                 st.session_state["answer_feedback"] = ""
#                 st.session_state["next_question_allowed"] = False
#             else:
#                 st.error("Error: Could not retrieve the next question.")

# st.sidebar.markdown("### Progress")
# st.sidebar.write(f"Questions Asked: {st.session_state['questions_asked']} / 10")
# st.sidebar.write(f"Correct Answers: {st.session_state['correct_answers']}")
# if st.session_state["questions_asked"] == 10:
#     pass_status = "Pass" if st.session_state["correct_answers"] > 5 else "Fail"
#     st.sidebar.markdown(f"### Result: **{pass_status}**")


# import streamlit as st
# import requests

# API_URL_QUESTION = "http://localhost:8500/generate_question"
# API_URL_ANSWER = "http://localhost:8500/submit_answer"

# st.title("Interview Chatbot")

# # Initialize session state variables
# if "current_question" not in st.session_state:
#     st.session_state["current_question"] = None
# if "answer_feedback" not in st.session_state:
#     st.session_state["answer_feedback"] = ""
# if "next_question_allowed" not in st.session_state:
#     st.session_state["next_question_allowed"] = True
# if "correct_answers" not in st.session_state:
#     st.session_state["correct_answers"] = 0
# if "questions_asked" not in st.session_state:
#     st.session_state["questions_asked"] = 0
# if "remaining_questions" not in st.session_state:
#     st.session_state["remaining_questions"] = 10  # Default total questions

# if not st.session_state["current_question"] and st.button("Start Interview", key="start_interview"):
#     response = requests.get(API_URL_QUESTION)
#     if response.status_code == 200:
#         data = response.json()
#         question = data.get("question", "Error: Could not retrieve question")
#         questions_asked = data.get("questions_asked", 0)

#         st.session_state["current_question"] = question
#         st.session_state["questions_asked"] = questions_asked  # Update questions asked
#         st.session_state["answer_feedback"] = ""  # Clear feedback for new question
#         st.session_state["next_question_allowed"] = False
#     else:
#         st.error("Error: Could not start interview")

# if st.session_state["questions_asked"] < 10 and st.session_state["current_question"]:
#     st.subheader(f"Question: {st.session_state['current_question']}")
#     answer = st.text_area("Your Answer (2-3 lines):", max_chars=300)
    
#     if st.button("Submit Answer", key="submit_answer"):
#         if answer.strip():
#             response = requests.post(API_URL_ANSWER, json={"question": st.session_state["current_question"], "answer": answer})
#             if response.status_code == 200:
#                 feedback = response.json()
#                 st.session_state["correct_answers"] = feedback["correct_answers"]
#                 st.session_state["questions_asked"] = feedback["questions_asked"]
#                 st.session_state["remaining_questions"] = feedback["remaining_questions"]
#                 st.session_state["answer_feedback"] = feedback["evaluation"]
#                 is_correct = feedback.get("is_correct", False)
#                 color = "green" if is_correct else "red"
#                 st.markdown(f"<span style='color: {color};'>{st.session_state['answer_feedback']}</span>", unsafe_allow_html=True)
#                 st.session_state["next_question_allowed"] = is_correct
#             else:
#                 st.error("Error: Could not evaluate the answer.")
#         else:
#             st.warning("Please provide a valid answer.")

#     if st.session_state["next_question_allowed"]:
#         if st.button("Next Question", key="next_question"):
#             if st.session_state["questions_asked"] < 10:  # Check limit before fetching new question
#                 response = requests.get(API_URL_QUESTION)
#                 if response.status_code == 200:
#                     data = response.json()
#                     question = data.get("question", "Error: Could not retrieve question")
#                     questions_asked = data.get("questions_asked", 0)

#                     st.session_state["current_question"] = question
#                     st.session_state["questions_asked"] = questions_asked  # Update questions asked
#                     st.session_state["answer_feedback"] = ""
#                     st.session_state["next_question_allowed"] = False
#                 else:
#                     st.error("Error: Could not retrieve the next question.")

# st.sidebar.markdown("### Progress")
# st.sidebar.write(f"Questions Asked: {st.session_state['questions_asked']} / 10")
# st.sidebar.write(f"Correct Answers: {st.session_state['correct_answers']}")
# if st.session_state["questions_asked"] == 10:
#     pass_status = "Pass" if st.session_state["correct_answers"] > 5 else "Fail"
#     st.sidebar.markdown(f"### Result: **{pass_status}**")
#     st.markdown("<h3 style='color: green;'>Interview Completed!</h3>", unsafe_allow_html=True)



import streamlit as st
import requests

API_URL_QUESTION = "http://localhost:8500/generate_question"
API_URL_ANSWER = "http://localhost:8500/submit_answer"

st.title("Interview Chatbot")

# Initialize session state variables
if "current_question" not in st.session_state:
    st.session_state["current_question"] = None
if "answer_feedback" not in st.session_state:
    st.session_state["answer_feedback"] = ""
if "next_question_allowed" not in st.session_state:
    st.session_state["next_question_allowed"] = True
if "correct_answers" not in st.session_state:
    st.session_state["correct_answers"] = 0
if "questions_asked" not in st.session_state:
    st.session_state["questions_asked"] = 0
if "remaining_questions" not in st.session_state:
    st.session_state["remaining_questions"] = 10  # Default total questions
if "percentage_score" not in st.session_state:
    st.session_state["percentage_score"] = 0

# Calculate pass/fail and percentage after completing 10 questions
def calculate_result():
    total_questions = st.session_state["questions_asked"]
    correct_answers = st.session_state["correct_answers"]
    
    # Calculate percentage
    st.session_state["percentage_score"] = (correct_answers / total_questions) * 100
    pass_status = "Pass" if st.session_state["percentage_score"] >= 60 else "Fail"
    
    return pass_status

if not st.session_state["current_question"] and st.button("Start Interview", key="start_interview"):
    response = requests.get(API_URL_QUESTION)
    if response.status_code == 200:
        data = response.json()
        question = data.get("question", "Error: Could not retrieve question")
        questions_asked = data.get("questions_asked", 0)

        st.session_state["current_question"] = question
        st.session_state["questions_asked"] = questions_asked  # Update questions asked
        st.session_state["answer_feedback"] = ""  # Clear feedback for new question
        st.session_state["next_question_allowed"] = False
    else:
        st.error("Error: Could not start interview")

if st.session_state["questions_asked"] < 10 and st.session_state["current_question"]:
    st.subheader(f"Question: {st.session_state['current_question']}")
    answer = st.text_area("Your Answer (2-3 lines):", max_chars=300)
    
    if st.button("Submit Answer", key="submit_answer"):
        if answer.strip():
            response = requests.post(API_URL_ANSWER, json={"question": st.session_state["current_question"], "answer": answer})
            if response.status_code == 200:
                feedback = response.json()
                st.session_state["correct_answers"] = feedback["correct_answers"]
                st.session_state["questions_asked"] = feedback["questions_asked"]
                st.session_state["remaining_questions"] = feedback["remaining_questions"]
                st.session_state["answer_feedback"] = feedback["evaluation"]
                is_correct = feedback.get("is_correct", False)
                color = "green" if is_correct else "red"
                st.markdown(f"<span style='color: {color};'>{st.session_state['answer_feedback']}</span>", unsafe_allow_html=True)
                st.session_state["next_question_allowed"] = True
            else:
                st.error("Error: Could not evaluate the answer.")
        else:
            st.warning("Please provide a valid answer.")

    if st.session_state["next_question_allowed"]:
        if st.button("Next Question", key="next_question"):
            if st.session_state["questions_asked"] < 10:  # Check limit before fetching new question
                response = requests.get(API_URL_QUESTION)
                if response.status_code == 200:
                    data = response.json()
                    question = data.get("question", "Error: Could not retrieve question")
                    questions_asked = data.get("questions_asked", 0)

                    st.session_state["current_question"] = question
                    st.session_state["questions_asked"] = questions_asked  # Update questions asked
                    st.session_state["answer_feedback"] = ""
                    st.session_state["next_question_allowed"] = False
                else:
                    st.error("Error: Could not retrieve the next question.")

# Once all 10 questions are asked, display the result.
if st.session_state["questions_asked"] == 10:
    pass_status = calculate_result()
    st.markdown("<h3 style='color: green;'>Interview Completed!</h3>", unsafe_allow_html=True)

st.sidebar.markdown("### Progress")
st.sidebar.write(f"Questions Asked: {st.session_state['questions_asked']} / 10")
st.sidebar.write(f"Correct Answers: {st.session_state['correct_answers']}")
st.sidebar.write(f"Percentage Score: {st.session_state['percentage_score']:.2f}%")
if st.session_state["questions_asked"] == 10:
    st.sidebar.markdown(f"### Result: **{pass_status}**")
