# **🌟 Enhanced Customer Experience & Improved Employee Productivity using IBM-Watsonx 🌟**

![IBM Watsonx](images/image-21.png)

---

## **🎯 Index**
1. [📖 Background](#background)
2. [🚧 Challenges](#challenges)
3. [🛠️ Solution Stack](#solution-stack)
4. [💻 Technical Details](#technical-details)
5. [📊 LLM Model Used](#llm-model-used)
6. [🚀 Way Forward](#way-forward)
7. [🏗️ Solution Architecture](#solution-architecture)
8. [🔍 Application Walkthrough](#application-walkthrough)
9. [🎥 Presentation](#presentation)
10. [📝 Note](#note)
11. [💡 Credits](#credits)

---

## **📖 Background** <a name="background"></a>
An e-commerce platform struggles with its **call center data**, handling a high volume of customer interactions daily. Though it gathers vast feedback and complaint data, this wealth remains underutilized. The challenge lies in analyzing the data effectively to gain insights into **customer satisfaction** and **regional trends**, limiting proactive service improvements.

---

## **🚧 Challenges** <a name="challenges"></a>
- **🧠 Sentiment Analysis**: Accurately identifying customer sentiments from call conversations.
- **📝 Call Summarization**: Summarizing lengthy calls for deeper insights.
- **📍 Regional Insights**: Extracting trends based on customer location.

---

## **🛠️ Solution Stack** <a name="solution-stack"></a>
To tackle these challenges, we leverage **IBM Watsonx Granite** models for sentiment analysis, call summarization, and feature extraction using **prompt engineering**.

---

## **💻 Technical Details** <a name="technical-details"></a>
- **Language**: Python 🐍
  
### **📊 Dataset Used**
- **Name**: `NebulaByte/E-Commerce_Customer_Support_Conversations`
- **Source**: [Hugging Face Dataset](https://huggingface.co/datasets/NebulaByte/E-Commerce_Customer_Support_Conversations)
- **Column Used**: `conversation`

---

## **📊 LLM Model Used** <a name="llm-model-used"></a>
- **Sentiment Analysis**: `ibm/granite-13b-instruct-v2`
- **Call Summary & Feature Extraction**: `ibm/granite-13b-chat-v2`

### **📂 Notebook**
- [Notebook Link](https://github.com/meanirban100/IBM-Watsonx-Hackathon/blob/main/hackathon-challenge.ipynb)  
  *(Generate API key from IBM Cloud platform)*

---

## **🚀 Way Forward** <a name="way-forward"></a>
- **💼 Productivity & Efficiency**: Enhanced call summarization can streamline processes and improve call center efficiency.
- **📈 Performance-Based Compensation**: Operational optimization could enable performance-based pay models.
- **🌐 Cloud Flexibility**: The solution can scale across **AWS**, **Azure**, and **GCP**, offering seamless integration.

---

## **🏗️ Solution Architecture** <a name="solution-architecture"></a>

![Solution Architecture](images/image-20.png)

---

## **🔍 Application Walkthrough** <a name="application-walkthrough"></a>

### **📄 Dataset** (Source: Hugging Face)

![Dataset](images/image-2.png)

### **🧠 Sentiment Analysis** (Model: `granite-13b-instruct-v2`)

![Sentiment Analysis](images/image-3.png)

![Sentiment Analysis](images/image-4.png)

### **📝 Text Summarization** (Model: `granite-13b-chat-v2`)

![Text Summarization](images/image-5.png)

![Text Summarization](images/image-7.png)

### **🔍 Feature Extraction** (Model: `granite-13b-chat-v2`)

![Feature Extraction](images/image-8.png)

![Feature Extraction](images/image-9.png)

### **📅 Customer Sentiment by Day (Plotly)**

![Customer Sentiment Analytics](images/image-10.png)

### **📊 Top 10 User Interest (Categories)**

![User Interest](images/image-11.png)

### **☁️ Word Cloud Dashboard (Plotly)**

![Word Cloud Dashboard](images/image-12.png)

### **📍 Location-Wise Call Records (Plotly)**

![Location Wise Call Records](images/image-13.png)

---

## **🎥 Presentation** <a name="presentation"></a>
[**Deck Presentation**](https://github.com/meanirban100/IBM-Watsonx-Hackathon/blob/main/IBM-Watsonx-Presentation.pptx)

---

## **📝 Note** <a name="note"></a>
This submission is part of the **IBM TechXchange Pre-Conference Watsonx Hackathon**.  

Refer to the [Hackathon Page](https://compete.pretxchack.watsonx-challenge.ibm.com/competitions/pre-txc) for more details.

---

## **💡 Credits** <a name="credits"></a>
- **Anirban Banerjee**  
- **Ajoy Kumar Daga**
