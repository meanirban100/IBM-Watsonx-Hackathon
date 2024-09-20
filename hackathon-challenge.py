#!/usr/bin/env python
# coding: utf-8

# ## Install the required libararies

# In[1]:


get_ipython().system('pip install -q datasets ibm-watson pandas tqdm wordcloud')


# ## Import the required libraries

# In[2]:


import pandas as pd
from datasets import load_dataset
from datetime import datetime, timedelta
import random
import os

import requests
from ibm_watson import IAMTokenManager

from tqdm import tqdm

pd.set_option("display.max_rows", None)  # Display all rows
pd.set_option("display.max_columns", None)  # Display all columns
pd.set_option("display.max_colwidth", None)  # Display full content of each cell
tqdm.pandas()


# ## Load the Ecommerce Datasets 
# ## Dataset Type - E-Commerce Customer Support Conversations
# 
# ## Data Source - https://huggingface.co/datasets/NebulaByte/E-Commerce_Customer_Support_Conversations

# In[3]:


dataset = load_dataset("NebulaByte/E-Commerce_Customer_Support_Conversations")
train_data = dataset["train"]
customer_conversation = train_data.to_pandas()[
    ["conversation"]
]  ### Consider the conversation column only


# ## Add Synthetic Data (Add call_recording_date and customer_location)

# In[4]:


def random_date_generation(delta: int = 7):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=delta)
    random_timestamp = start_date + timedelta(
        days=random.randint(0, delta),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )
    return random_timestamp


customer_conversation["recording_date"] = [
    random_date_generation() for _ in range(len(customer_conversation))
]

locations = ["New York, NY",
            "Los Angeles, CA",
            "San Diego, CA",
            "San Francisco, CA",
            "Jacksonville, FL",
            "Seattle, WA",
            "Washington, D.C.",
            "Boston, MA"
            ]

customer_conversation["location"] = [
    random.choice(locations) for _ in range(len(customer_conversation))
]


# ## Preview the data

# In[5]:


customer_conversation.head(2)


# ## Set the Variables

# In[6]:


API_KEY = "######################################" ## Enter the API key genereted from IBM Watson platform
SERVICE_URL = (
    "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
)
INSTRUCT_MODEL_ID = "ibm/granite-13b-instruct-v2"
CHAT_MODEL_ID = "ibm/granite-13b-chat-v2"
PROJECT_ID = "d80ea387-8eaa-42db-8d24-43edef6c6f69"


# ## Function to generate bearer Token

# In[7]:


def get_token(api_key: str) -> str:
    try:
        iam_token_manager = IAMTokenManager(apikey=api_key)
        return iam_token_manager.get_token()
    except Exception as e:
        raise Exception(f"Error obtaining IAM token: {str(e)}")


# ## Request body function

# In[8]:


def create_request_body(model_id: str, input_text: str, max_tokens: int = 900) -> dict:
    """Creates the request body for the API call."""
    return {
        "input": input_text,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": max_tokens,
            "repetition_penalty": 1.05,
        },
        "model_id": model_id,
        "project_id": PROJECT_ID,
        "moderations": {
            "hap": {
                "input": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {"remove_entity_value": True},
                },
                "output": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {"remove_entity_value": True},
                },
            }
        },
    }


# ## API request function

# In[9]:


def make_api_request(body: dict, token: str, url: str) -> dict:
    """Makes the API request to the IBM Watson service."""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")

    return response.json()


# ## Chat message function wrapper

# In[10]:


def get_chat_message(prompt, input, model_id):
    input_text = f"{prompt} \n {input}"

    # print(input_text)

    token = get_token(API_KEY)
    body = create_request_body(model_id, input_text)
    data = make_api_request(body, token, SERVICE_URL)

    # print(data)

    return data["results"][0]["generated_text"]


# ## Sentiment Analysis

# In[11]:


sentiment_analysis_prompt = """Analyze the sentiment of the following text and only return one word: 'positive', 'negative', or 'neutral' without any explanation or 
                               additional information. Text: """

customer_conversation["customer_sentiment"] = customer_conversation.progress_apply(
    lambda row: get_chat_message(
        sentiment_analysis_prompt, row["conversation"], INSTRUCT_MODEL_ID
    ),
    axis=1,
)


# In[12]:


customer_conversation.head(2)


# ## Call (Text) Summarization

# In[13]:


call_summary_prompt = (
    "Summarize the below call recording. Maxumum 100 Words. Recording: "
)

customer_conversation["call_summary"] = customer_conversation.progress_apply(
    lambda row: get_chat_message(
        call_summary_prompt, row["conversation"], CHAT_MODEL_ID
    ),
    axis=1,
)


# In[14]:


customer_conversation.head(2)


# ## Feature Extraction

# In[15]:


feature_extraction_prompt = """
For the below conversation i want to do feature extraction.The output should be in json format. 
The output must contains following details issue, action_taken, product_interest, customer_details, resolution,additional_support_needed. 
No explanation needed. Just the json output. 
In case if customer_details are not present populate it as NULL. 
In case any other details are not present populate as NA. But tags must be present. 
Do not make up information if it is not available in the below conversation. Conversation - 
"""
customer_conversation["feature_extraction"] = customer_conversation.progress_apply(
    lambda row: get_chat_message(
        feature_extraction_prompt, row["conversation"], CHAT_MODEL_ID
    ),
    axis=1,
)


# In[16]:


customer_conversation.head(2)


# ## As the feature extraction data contains json data along with text values, we have to do further data manipulation to extract the json data.

# In[17]:


import json
import re

# Function to extract JSON from the text
def extract_json_from_text(text):
    try:
        # Use regular expressions to extract the JSON part
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            json_data = json.loads(json_str)  # Parse the JSON string into a dictionary

            json_data["issue"] = json_data.get("issue", "NA")
            json_data["action_taken"] = json_data.get("action_taken", "NA")
            json_data["product_interest"] = json_data.get("product_interest", "NA")
            json_data["customer_details"] = json_data.get(
                "customer_details", None
            )  
            json_data["resolution"] = json_data.get("resolution", "NA")
            json_data["additional_support_needed"] = json_data.get(
                "additional_support_needed", "NA"
            )

            return json.dumps(json_data)
        else:
            return None
    except (json.JSONDecodeError, TypeError):
        return None  


customer_conversation["feature_extraction"] = customer_conversation[
    "feature_extraction"
].progress_apply(extract_json_from_text)


# In[18]:


customer_conversation.head(2)


# In[19]:


customer_conversation.replace('', 'unknown', inplace=True)


# ## Save the data as json file

# In[20]:


customer_conversation.to_json(
    os.path.join(os.getcwd(), "result.json"),
    orient="records",
    indent=4,
    date_format="iso"
)


# ## Create Metrice

# In[21]:


import plotly.express as px
import pandas as pd
import os
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import warnings
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64

warnings.filterwarnings("ignore")


# ## Customer Sentiment by Day

# In[22]:


df = pd.read_json(os.path.join(os.getcwd(), "result.json"))
df["recording_date"] = pd.to_datetime(df["recording_date"]).dt.date

df_grouped = (
    df.groupby(["recording_date", "customer_sentiment"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)
df_grouped["total_calls"] = df_grouped[
    ["positive", "neutral", "negative", "unknown"]
].sum(axis=1)

df_melted = df_grouped.melt(
    id_vars=["recording_date", "total_calls"],
    value_vars=["positive", "neutral", "negative", "unknown"],
    var_name="Sentiment",
    value_name="Count",
)

fig = px.bar(
    df_melted,
    x="recording_date",
    y="Count",
    color="Sentiment",
    barmode="group",
    title="Customer Sentiment Analysis by Day",
    labels={
        "recording_date": "Date",
    },
    text="Count",
    range_color={"black", "blue", "yellow"},
)

for date, total in zip(df_grouped["recording_date"], df_grouped["total_calls"]):
    fig.add_annotation(
        x=date,
        y=max(df_melted["Count"]),
        text=f"Total:{total}",
        showarrow=False,
        yshift=10,
        font=dict(size=10, color="Black"),
    )

fig.show()


# ## Top 10 User Interest (Categories)

# In[23]:


df = pd.read_json(os.path.join(os.getcwd(), "result.json"))

def extract_categories(json_str):
    try:
        parsed_json = json.loads(json_str)
        return str(parsed_json.get("product_interest", None))
    except (TypeError, json.JSONDecodeError):
        return "Nothing"


df["categories"] = df["feature_extraction"].apply(extract_categories)


# In[26]:


df = df.loc[(df["categories"] != "Nothing")]
category_counts = df["categories"].value_counts()

top_categories = category_counts.head(10)

# Create a bar chart
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=top_categories.index,
        y=top_categories.values,
        # marker_color='blue'
    )
)

# Customize layout
fig.update_layout(
    title="Total Calls Based on Top 10 Categories",
    xaxis_title="Categories",
    yaxis_title="Number of Calls",
    xaxis_tickangle=-45)

# Show the plot
fig.show()


# ## Word Cloud Dashboard

# In[28]:


df = pd.read_json(os.path.join(os.getcwd(), "result.json"))

df["categories"] = df["feature_extraction"].apply(extract_categories)


# In[29]:


words = df["categories"].to_list()
words = " ".join(words)
words = words.replace("/", " ").replace("Nothing", "")

wordcloud = WordCloud(width=800, height=400, background_color="white").generate(words)

img_buffer = BytesIO()
wordcloud.to_image().save(img_buffer, format="PNG")
img_buffer.seek(0)

img_base64 = base64.b64encode(img_buffer.read()).decode("utf-8")

fig = go.Figure()

fig.add_layout_image(
    dict(
        source=f"data:image/png;base64,{img_base64}",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,  # Position at the center
        sizex=1,
        sizey=1,  # Scale to fit
        xanchor="center",
        yanchor="middle",
    )
)

fig.update_layout(
    width=800,
    height=400,
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
)

# Show the figure
fig.show()


# ## Location Wise call records

# In[30]:


df = pd.read_json(os.path.join(os.getcwd(), "result.json"))
calls_per_location = df.groupby("location").size().reset_index(name="total_calls")

calls_per_location


# In[31]:


# Geographical coordinates for the specified locations
location_coords = {
    "New York, NY": (40.7128, -74.0060),
    "Los Angeles, CA": (34.0522, -118.2437),
    "San Diego, CA": (32.7157, -117.1611),
    "San Francisco, CA": (37.7749, -122.4194),
    "Jacksonville, FL": (30.3322, -81.6557),
    "Seattle, WA": (47.6062, -122.3321),
    "Washington, D.C.": (38.9072, -77.0369),
    "Boston, MA": (42.3601, -71.0589)
}

calls_per_location["latitude"] = calls_per_location["location"].map(
    lambda loc: location_coords[loc][0]
)
calls_per_location["longitude"] = calls_per_location["location"].map(
    lambda loc: location_coords[loc][1]
)
calls_per_location.head()


# In[33]:


fig = go.Figure(
    data=go.Scattergeo(
        lat=calls_per_location["latitude"],
        lon=calls_per_location["longitude"],
        mode="markers",
        marker=dict(
            size=calls_per_location[
                "total_calls"
            ]/2.5,  
            color=calls_per_location["total_calls"],
            colorscale="Viridis",
            colorbar=dict(title="Number of Calls"),
        ),
        text=calls_per_location["location"],  
    )
)

fig.update_layout(
    title="Heatmap of Calls by Location",
    geo=dict(
        scope="usa",
        projection=dict(type="albers usa"),
        showland=True,
        landcolor="rgb(240, 240, 240)",
        countrycolor="rgb(255, 255, 255)",
        showocean=True,
        oceancolor="rgb(0, 204, 255)",
        showcoastlines=True,
        coastlinecolor="rgb(0, 0, 0)",
    ),
)

fig.show()


# In[ ]:




