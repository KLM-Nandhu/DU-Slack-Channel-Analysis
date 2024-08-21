import streamlit as st
import pandas as pd
import openai
from datetime import datetime
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_gpt_response(conversation):
    prompt = f"""
    Given the following conversation, extract and format the information as follows:
    - Reporter: The person who reported the issue
    - Report Date: The date the issue was reported (format: DD Mon)
    - Report Time: The time the issue was reported (format: HH:MM AM/PM)
    - Customer: The name of the customer
    - DU: The DU number(s) mentioned
    - Notes: A summary of the issue and any actions taken
    - Resolution Date: The date the issue was resolved, if mentioned (format: DD Mon)
    - Resolution Time: The time the issue was resolved, if mentioned (format: HH:MM AM/PM)

    Important instructions:
    1. If any information is not available, use "Not specified".
    2. For the Resolution Date and Resolution Time:
       - If the response indicates the issue is still being checked, worked on, or not yet finished (e.g., "checking", "working on it", "will update"), leave these fields empty.
       - Only provide Resolution Date and Time if there's clear confirmation that the issue has been fully resolved.
       - If someone says it's done or working, but there's no clear confirmation of full resolution, still leave these fields empty.
    3. Include all relevant information in the Notes field, including ongoing status updates.

    Format the output as a single line with values separated by ' | '.

    Conversation:
    {conversation}

    Output format:
    Reporter | Report Date | Report Time | Customer | DU | Notes | Resolution Date | Resolution Time
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a expert helpful assistant that extracts information from conversations."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message['content'].strip()

def save_history(result):
    if 'history' not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append(result)

def show_history():
    st.sidebar.title("Conversation History")
    if 'history' in st.session_state and st.session_state.history:
        for i, item in enumerate(st.session_state.history, 1):
            with st.sidebar.expander(f"Conversation {i}"):
                st.write(item)
    else:
        st.sidebar.write("No history available")

def main():
    st.set_page_config(page_title="Conversation Processor", layout="wide")
    st.title("Conversation Processor")

    # Add a button to show/hide history
    if st.sidebar.button("History"):
        st.session_state.show_history = not st.session_state.get('show_history', False)

    # Show history if the state is true
    if st.session_state.get('show_history', False):
        show_history()

    conversation = st.text_area("Enter the conversation here:", height=300)

    if st.button("Process"):
        if conversation:
            result = get_gpt_response(conversation)
            result_list = result.split(' | ')
            
            if len(result_list) == 8:  # Ensure we have all 8 fields
                df = pd.DataFrame([result_list], columns=["Reporter", "Report Date", "Report Time", "Customer", "DU", "Notes", "Resolution Date", "Resolution Time"])
                st.dataframe(df)
                
                # Display as a formatted string
                formatted_output = f"| {result} |"
                st.text("Formatted Output:")
                st.code(formatted_output, language='markdown')

                # Save to history
                save_history(formatted_output)
            else:
                st.error("Error in processing. Please try again or refine the conversation input.")
        else:
            st.warning("Please enter a conversation to process.")

if __name__ == "__main__":
    main()
