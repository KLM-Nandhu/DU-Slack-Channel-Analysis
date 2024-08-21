import streamlit as st
import pandas as pd
import openai
from datetime import datetime
import os
from dotenv import load_dotenv

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

    If any information is not available, use "Not specified".
    Format the output as a single line with values separated by ' | '.

    Conversation:
    {conversation}

    Output format:
    Reporter | Report Date | Report Time | Customer | DU | Notes | Resolution Date | Resolution Time
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a Expert helpfull assistant that extracts information from conversations."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message['content'].strip()

def main():
    st.set_page_config(page_title="Conversation Processor", layout="wide")
    st.title("Conversation Processor")

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
            else:
                st.error("Error in processing. Please try again or refine the conversation input.")
        else:
            st.warning("Please enter a conversation to process.")

if __name__ == "__main__":
    main()
