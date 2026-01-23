# AI Tutor
# To run
# streamlit run AI_Tutor.py

from openai import OpenAI
from dotenv import load_dotenv
import os
import streamlit as st

# Creat a .env file with a secret key to use OpenAI for this program
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("AI Tutor!")
with st.chat_message("assistant"):
    st.markdown("Hi! What can I help you with?")

SYSTEM_ROLE = """
    You are an AI tutor for introductory Python. ALWAYS follow the format specified by the prompt.
    If the conversation gets too off topic, suggest 8 python topics the user can ask and learn about. 
    """

def chat(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages 
    )
    return response.choices[0].message.content

def generate_prompt(user_input):
    # Identify mode:
    system_role = """decide based on input whether the user wants feedback for a 
        specific topic or practice problem the student tried, for example if 
        the student is asking about how they performed (mode = feedback), help debbugging code (mode=debug), 
        an explanation of a concept (mode = explain), an exercise example for practice (mode = exercise), 
        or if the student wants a coding example (mode = code). 
        If the content does not fit into any category (debug, explain, exercise, feedback, code), 
        then the mode is 'help'.
        respond with one word, the mode. 
        """
    messages_1 = [{'role':'system','content':system_role},
        {'role':'user','content':user_input}]
    mode = chat(messages_1).strip().lower()
    print("Mode:",mode)
    
    
    if mode == 'explain':
        system_input = f"""
            Your job is Concept Explainer. Your function is to explain Python concepts simply.
            Please format your response as follows:
            **Concept explanation:** ...
            **Code Example:** ...
            **Practice Excercise:** ...
            Here is my question: 
            {user_input} 
            """
    elif mode == 'code':
        system_input = f"""
            Your job is Code Example Generator. Your function is to create annotated Python examples.
            Format your response as follows:
            **Quick explanation:** ...
            **Code Example:** ... 
            **Practice Exercises:** ...
            Here is what I want an example of: 
            {user_input} 
            """
    elif mode == 'debug':
        system_input = f"""
            Your job is Error Debugger. Your function is to identify and explain errors in the student' code.
            Format your response as follows:
            **Code explanation:** ...
            **Possible Issues:** ... (if any)
            **Feedback:** ...
            Do not mention issues having to do with spacing and indentatin. 
            Here is my code: 
            {user_input} 
            """
    elif mode == 'exercise':
        system_input = f"""
            Your job is Exercise Creator. Your function is to generate short coding exercises.
            Format your response as follows:
            **Quick explanation:** ...
            **Practice Excercises:** 
            1. 
            2.
            ... Give 6 exercises 
            Then ask the student if they would like more practice problems and if they want the answers.
            I am the student and this is my query: 
            {user_input} 
            """
    elif mode == 'feedback':
        system_input = f"""
            Your job is Feedback Provider. Your function is to gives constructive, motivating feedback. 
            Format your response as follows: 
            **Quick explanation:** ...
            **Feedback:** ...
            Ignore any lack of spacing or indentation. 
            Provide feedback for: 
            {user_input} 
            """
    else: 
        system_input = user_input
    
    return system_input

if __name__ == "__main__":
    # Initialize memory
    if "memory" not in st.session_state:
        st.session_state.memory = []
        
    for msg in st.session_state.memory:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Learn python")
    if user_input:
        # Store user message
        st.session_state.memory.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)
    
        prompt = generate_prompt(user_input)
        print("prompt:",prompt)
        messages = [{"role": "system", "content": SYSTEM_ROLE}] + st.session_state.memory + [{"role": "user", "content": prompt}]

        response = chat(messages)
        st.session_state.memory.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown(response)

    # Clear button

    st.button("Clear Chat", on_click=lambda: st.session_state.update({"memory": []}))
