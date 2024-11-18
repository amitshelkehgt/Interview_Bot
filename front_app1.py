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
 
# Display the Start or Next Question button only if allowed
if st.session_state["next_question_allowed"]:
    if st.button("Start Interview" if not st.session_state["current_question"] else "Next Question"):
        response = requests.get(API_URL_QUESTION)
        if response.status_code == 200:
            question = response.json().get("question", "Error: Could not retrieve question")
            st.session_state["current_question"] = question
            st.session_state["answer_feedback"] = ""  # Clear feedback
            st.session_state["next_question_allowed"] = False  # Lock until correct answer
        else:
            st.error("Error: Could not start the interview")
 
# Display the current question if available
if st.session_state["current_question"]:
    st.subheader(f"Question: {st.session_state['current_question']}")
   
    # User input for the answer
    answer = st.text_area("Your Answer (2-3 lines):", max_chars=300)
   
    # Button to submit the answer
    if st.button("Submit Answer"):
        if answer.strip():  # Ensure non-empty answer
            # API call to evaluate the answer
            response = requests.post(API_URL_ANSWER, json={"question": st.session_state["current_question"], "answer": answer})
           
            if response.status_code == 200:
                feedback = response.json()
                is_correct = feedback.get("is_correct", False)
                st.session_state["answer_feedback"] = feedback["evaluation"]
 
                # Display color-coded feedback
                color = "green" if is_correct else "red"
                st.markdown(f"<span style='color: {color};'>{st.session_state['answer_feedback']}</span>", unsafe_allow_html=True)
               
                # Update state based on correctness
                st.session_state["next_question_allowed"] = is_correct
            else:
                st.error("Error: Could not evaluate the answer.")
        else:
            st.warning("Please provide a valid answer.")
 
    # Display feedback
    if st.session_state["answer_feedback"]:
        st.write(st.session_state["answer_feedback"])