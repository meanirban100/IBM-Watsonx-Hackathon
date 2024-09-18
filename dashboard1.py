import streamlit as st
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import os

import csv
df = pd.read_json(os.path.join(os.getcwd(),'result.json'))
df['recording_date'] = pd.to_datetime(df['recording_date']).dt.date

df_grouped = df.groupby(['recording_date', 'customer_sentiment']).size().unstack(fill_value=0).reset_index()
df_grouped['total_calls'] = df_grouped[['positive', 'neutral', 'negative','unknown']].sum(axis=1)

df_melted = df_grouped.melt(id_vars=['recording_date', 'total_calls'], 
                            value_vars=['positive', 'neutral', 'negative','unknown'], 
                            var_name='Sentiment', value_name='Count')


fig = px.bar(df_melted, x='recording_date', y='Count', color='Sentiment',
             barmode='group', title='Customer Sentiment Analysis by Day',
             labels={'recording_date': 'Date', },
             text='Count')

for date, total in zip(df_grouped['recording_date'], df_grouped['total_calls']):
    fig.add_annotation(x=date, y=max(df_melted['Count']), 
                       text=f"Total: {total}", showarrow=False, 
                       yshift=10, font=dict(size=12, color="black"))


st.title("Customer Sentiment Dashboard")
st.plotly_chart(fig)