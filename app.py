import streamlit as st
import pandas as pd
from datetime import datetime

def process_conversation(conversation):
    lines = conversation.split('\n')
    reporter = lines[0].split()[0]
    date_time = ' '.join(lines[0].split()[1:4])
    try:
        date_time = datetime.strptime(date_time, '%d %b at %I:%M %p')
        report_date = date_time.strftime('%d %b')
        report_time = date_time.strftime('%I:%M %p')
    except ValueError:
        report_date = "Date not specified"
        report_time = "Time not specified"
    
    customer = next((line.split(': ')[1].strip() for line in lines if 'Customer:' in line), "Not specified")
    du = next((line.split('DU:')[1].strip() for line in lines if 'DU:' in line), "Not specified")
    
    notes = ' '.join(lines[1:])
    resolution_date = ""
    resolution_time = ""
    
    last_line = lines[-1].strip()
    if ":" in last_line and not last_line.startswith(reporter):
        resolution_parts = last_line.split()
        if len(resolution_parts) >= 3:
            resolution_date = ' '.join(resolution_parts[:2])
            resolution_time = ' '.join(resolution_parts[2:])

    return [reporter, report_date, report_time, customer, du, notes, resolution_date, resolution_time]

def main():
    st.set_page_config(page_title="Conversation Processor", layout="wide")
    st.title("Conversation Processor")

    conversation = st.text_area("Enter the conversation here:", height=300)

    if st.button("Process"):
        if conversation:
            result = process_conversation(conversation)
            df = pd.DataFrame([result], columns=["Reporter", "Report Date", "Report Time", "Customer", "DU", "Notes", "Resolution Date", "Resolution Time"])
            st.dataframe(df)
            
            # Display as a formatted string
            formatted_output = f"| {' | '.join(result)} |"
            st.text("Formatted Output:")
            st.code(formatted_output, language='markdown')
        else:
            st.warning("Please enter a conversation to process.")

if __name__ == "__main__":
    main()
