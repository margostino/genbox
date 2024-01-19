import streamlit as st
import pandas as pd
import json
import openai
import os
import re
import matplotlib.pyplot as plt
from langchain_experimental.agents import create_csv_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


def csv_agent_func(file_path, user_message):
    """Run the CSV agent with the given file path and user message."""
    agent = create_csv_agent(
        ChatOpenAI(
            temperature=0, model="gpt-4-1106-preview", openai_api_key=OPENAI_API_KEY
        ),
        file_path,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )

    try:
        # Properly format the user's input and wrap it with the required "input" key
        tool_input = {"input": {"name": "python", "arguments": user_message}}

        response = agent.run(tool_input)
        return response
    except Exception as e:
        st.write(f"Error: {e}")
        return None


def display_content_from_json(json_response):
    """
    Display content to Streamlit based on the structure of the provided JSON.
    """

    # Check if the response has plain text.
    if "answer" in json_response:
        st.write(json_response["answer"])

    # Check if the response has a bar chart.
    if "bar" in json_response:
        data = json_response["bar"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.bar_chart(df)

    # Check if the response has a table.
    if "table" in json_response:
        data = json_response["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)


file_path = "/Users/margostino/workspace/data/owid-datasets/datasets/Air pollution emissions by fuel (CEDS, 2022)/Air pollution emissions by fuel (CEDS, 2022).csv"
df = pd.read_csv(file_path)
st.dataframe(df)

user_input = "tell me some random pollution datapoint"

response = csv_agent_func(file_path, user_input)
print(response)