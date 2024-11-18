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
# if "percentage_score" not in st.session_state:
#     st.session_state["percentage_score"] = 0

# # Calculate pass/fail and percentage after completing 10 questions
# def calculate_result():
#     total_questions = st.session_state["questions_asked"]
#     correct_answers = st.session_state["correct_answers"]
    
#     # Calculate percentage
#     st.session_state["percentage_score"] = (correct_answers / total_questions) * 100
#     pass_status = "Pass" if st.session_state["percentage_score"] >= 60 else "Fail"
    
#     return pass_status

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
#                 st.session_state["next_question_allowed"] = True
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

# # Once all 10 questions are asked, display the result.
# if st.session_state["questions_asked"] == 10:
#     pass_status = calculate_result()
#     st.markdown("<h3 style='color: green;'>Interview Completed!</h3>", unsafe_allow_html=True)

# st.sidebar.markdown("### Progress")
# st.sidebar.write(f"Questions Asked: {st.session_state['questions_asked']} / 10")
# st.sidebar.write(f"Correct Answers: {st.session_state['correct_answers']}")
# st.sidebar.write(f"Percentage Score: {st.session_state['percentage_score']:.2f}%")
# if st.session_state["questions_asked"] == 10:
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
# if "correct_answers" not in st.session_state:
#     st.session_state["correct_answers"] = 0
# if "questions_asked" not in st.session_state:
#     st.session_state["questions_asked"] = 0
# if "remaining_questions" not in st.session_state:
#     st.session_state["remaining_questions"] = 10  # Default total questions
# if "percentage_score" not in st.session_state:
#     st.session_state["percentage_score"] = 0
# if "answer_input" not in st.session_state:
#     st.session_state["answer_input"] = ""  # To store the text area input
# if "next_question_triggered" not in st.session_state:
#     st.session_state["next_question_triggered"] = False  # Prevent double handling of "Next Question"

# # Calculate pass/fail and percentage after completing 10 questions
# def calculate_result():
#     total_questions = st.session_state["questions_asked"]
#     correct_answers = st.session_state["correct_answers"]

#     # Calculate percentage
#     st.session_state["percentage_score"] = (correct_answers / total_questions) * 100
#     pass_status = "Pass" if st.session_state["percentage_score"] >= 60 else "Fail"

#     return pass_status

# # Fetch a new question
# def fetch_next_question():
#     response = requests.get(API_URL_QUESTION)
#     if response.status_code == 200:
#         data = response.json()
#         question = data.get("question", "Error: Could not retrieve question")
#         questions_asked = data.get("questions_asked", 0)

#         # Update session state
#         st.session_state["current_question"] = question
#         st.session_state["questions_asked"] = questions_asked
#         st.session_state["answer_feedback"] = ""
#         st.session_state["answer_input"] = ""  # Clear input for the next question
#         st.session_state["next_question_triggered"] = False  # Reset flag
#     else:
#         st.error("Error: Could not retrieve the next question.")

# if not st.session_state["current_question"] and st.button("Start Interview", key="start_interview"):
#     fetch_next_question()

# if st.session_state["questions_asked"] < 10 and st.session_state["current_question"]:
#     st.subheader(f"Question: {st.session_state['current_question']}")
#     st.session_state["answer_input"] = st.text_area(
#         "Your Answer (2-3 lines):",
#         value=st.session_state["answer_input"],
#         max_chars=300,
#     )

#     if st.button("Submit Answer", key="submit_answer"):
#         if st.session_state["answer_input"].strip():
#             response = requests.post(
#                 API_URL_ANSWER,
#                 json={"question": st.session_state["current_question"], "answer": st.session_state["answer_input"]},
#             )
#             if response.status_code == 200:
#                 feedback = response.json()
#                 st.session_state["correct_answers"] = feedback["correct_answers"]
#                 st.session_state["questions_asked"] = feedback["questions_asked"]
#                 st.session_state["remaining_questions"] = feedback["remaining_questions"]
#                 st.session_state["answer_feedback"] = feedback["evaluation"]
#                 is_correct = feedback.get("is_correct", False)
#                 color = "green" if is_correct else "red"
#                 st.markdown(
#                     f"<span style='color: {color};'>{st.session_state['answer_feedback']}</span>",
#                     unsafe_allow_html=True,
#                 )
#                 st.session_state["next_question_triggered"] = True  # Mark as ready for the next question
#                     if st.session_state["next_question_triggered"]:
#                         if st.button("Next Question", key="next_question"):
#                             fetch_next_question()
#             else:
#                 st.error("Error: Could not evaluate the answer.")
#         else:
#             st.warning("Please provide a valid answer.")

#     # Single "Next Question" button logic
    

# # Once all 10 questions are asked, display the result.
# if st.session_state["questions_asked"] == 10:
#     pass_status = calculate_result()
#     st.markdown("<h3 style='color: green;'>Interview Completed!</h3>", unsafe_allow_html=True)

# st.sidebar.markdown("### Progress")
# st.sidebar.write(f"Questions Asked: {st.session_state['questions_asked']} / 10")
# st.sidebar.write(f"Correct Answers: {st.session_state['correct_answers']}")
# st.sidebar.write(f"Percentage Score: {st.session_state['percentage_score']:.2f}%")
# if st.session_state["questions_asked"] == 10:
#     st.sidebar.markdown(f"### Result: **{pass_status}**")




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
if "answer_input" not in st.session_state:
    st.session_state["answer_input"] = ""  # To store the text area input

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
        st.session_state["answer_input"] = ""  # Clear the text area
    else:
        st.error("Error: Could not start interview")

if st.session_state["questions_asked"] < 10 and st.session_state["current_question"]:
    st.subheader(f"Question: {st.session_state['current_question']}")
    st.session_state["answer_input"] = st.text_area("Your Answer (2-3 lines):", value=st.session_state["answer_input"], max_chars=300)
    
    if st.button("Submit Answer", key="submit_answer"):
        if st.session_state["answer_input"].strip():
            response = requests.post(API_URL_ANSWER, json={"question": st.session_state["current_question"], "answer": st.session_state["answer_input"]})
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
                    st.session_state["answer_input"] = ""  # Clear the text area for the next question
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
