# Enhanced Customer Experience & Improved Employee Productivity using IBM-Watson

![IBM Watson](images/image-1.png)

## Index
1. [Background](#background)
2. [Challenge](#challenge)
3. [Solution Stack](#solution-stack)
4. [Dataset Used](#dataset-used)
5. [LLM Model Used](#llm-model-used)
6. [Way Forward](#way-forward)
7. [Application Walkthorugh](#application-walkthorugh)
8. [Presentation](#Presentation)
9. [Note](#Note)
10. [Credits](##credits)

## Background
An e-commerce platform faces a challenge with its call center data. Each day, the center handles a high volume of customer interactions through customer care calls, generating extensive data files of feedback and complaints. However, this wealth of data remains underutilized, offering limited insights into overall customer satisfaction and regional issues. The platform struggles to effectively analyze this data to identify trends, sentiment, and recurring problems, which hinders its ability to improve service quality and address customer concerns proactively.

## Challenge
- **Real-Time Data Analysis**: Analyze call recordings in real time.
- **Sentiment Analysis**: Accurately determine sentiment from call conversations.
- **Call Summarization**: Summarize calls for further analysis.
- **Regional Insights**: Extract and visualize location-based trends and issues.

## Solution Stack
Integrate IBM Watson Granite model for sentiment analysis, call summarization, and feature extraction to address the challenges along with prompt engineering techniques.


## Tech Artifacts
- **Language**: Python

### Dataset Used
- **Name**: NebulaByte/E-Commerce_Customer_Support_Conversations
- **Source**: [HuggingFace Dataset](https://huggingface.co/datasets/NebulaByte/E-Commerce_Customer_Support_Conversations)
- **Column Used**: conversation

### LLM Model Used
- **Sentiment Analysis**: `ibm/granite-13b-instruct-v2`
- **Call Summary**: `ibm/granite-13b-chat-v2`

### Notebook 
- [hackathon-challenge.ipynb](https://github.com/meanirban100/IBM-Watson-Hackathon/blob/main/hackathon-challenge.ipynb)

## Way Forward
- **Improved Productivity & Efficiency**: Call summary analysis can enhance both call center productivity and overall efficiency.
- **Performance-Based Compensation**: Streamlined operations could lead to improved pay structures based on performance and growth metrics.
- **Real-Time Implementation**: The entire process can be deployed in real time by integrating with an event hub, pipeline orchestration layer, and data transformation layer.
- **Cloud Integration Flexibility**: The solution can seamlessly integrate with other cloud platforms such as AWS, Azure, and GCP, ensuring scalability and flexibility.


## Application Walkthorugh

### Dataset (Source - Huggingface)

![alt text](images/image-2.png)

### Sentiment Analysis (Model - granite-13b-instruct-v)

![Sentiment Analysis](images/image-3.png)

![Sentiment Analysis](images/image-4.png)


### Text Summarization (Model - granite-13b-chat-v2)

![Text Summarization](images/image-5.png)

![Text Summarization](images/image-7.png)

### Feature Extraction(Model - granite-13b-chat-v2)
![Feature Extraction](images/image-8.png)

![Feature Extraction](images/image-9.png)

### Customer Sentiment by Day (Plotly)

![Customer Sentiment Analytis](images/image-10.png)

### Top 10 User Interest (Categories) - Plotly

![User Interest](images/image-11.png)

### Word Cloud Dashboard (Plotly, Wordcloud)

![Word cloud dashboard](images/image-12.png)

### Location Wise call records (Plotly)

![Location wise call record volume](images/image-13.png)

## Presentation
[Deck](https://github.com/meanirban100/IBM-Watson-Hackathon/blob/main/IBM-Watson-Presentation.pptx)

## Note

This submission is intended for the IBM TechXchange Pre-Conference Watsonx Hackathon. 

Refer the [link](https://compete.pretxchack.watsonx-challenge.ibm.com/competitions/pre-txc) for further information. 


## Credits
### Anirban Banerjee
### Ajoy Kumar Daga