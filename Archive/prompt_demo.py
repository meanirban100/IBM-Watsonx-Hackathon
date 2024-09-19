import requests
from ibm_watson import IAMTokenManager

# API credentials and URL configuration
API_KEY = "utVIQO-z2u-qBcLrxHad15-9cAqxnC9Cl4b0hQigdHtZ"
SERVICE_URL = (
    "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
)
MODEL_ID = "ibm/granite-13b-chat-v2"
PROJECT_ID = "d80ea387-8eaa-42db-8d24-43edef6c6f69"


def get_token(api_key: str) -> str:
    """Generates and returns the IAM token."""
    try:
        iam_token_manager = IAMTokenManager(apikey=api_key)
        return iam_token_manager.get_token()
    except Exception as e:
        raise Exception(f"Error obtaining IAM token: {str(e)}")


def create_request_body(input_text: str, max_tokens: int = 900) -> dict:
    """Creates the request body for the API call."""
    return {
        "input": input_text,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": max_tokens,
            "repetition_penalty": 1.05,
        },
        "model_id": MODEL_ID,
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


def get_chat_message(input_message):
    input_text = f"""<|system|>
            You are Granite Chat, an AI language model developed by IBM. You are a cautious assistant. You carefully follow instructions. 
            You are helpful and harmless and you follow ethical guidelines and promote positive behavior. 
            You always respond to greetings (for example, hi, hello, g'day, morning, afternoon, evening, night, 
            what's up, nice to meet you, sup, etc) with \"Hello! I am Granite Chat, created by IBM. How can I help you today?\". 
            Please do not say anything else and do not start a conversation.
            <|user|>
            {input_message}
    """
    # Get the IAM token
    token = get_token(API_KEY)

    # Create the request body
    body = create_request_body(input_text)

    # Make the API request
    data = make_api_request(body, token, SERVICE_URL)

    return data


if __name__ == "__main__":
    input_message = "tell me joke"
    try:
        result = get_chat_message(input_message)
        print(result["results"][0]["generated_text"])
    except Exception as e:
        print(f"Error: {str(e)}")
