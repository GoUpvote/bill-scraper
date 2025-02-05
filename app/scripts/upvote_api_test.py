import os
import requests
from dotenv import load_dotenv

load_dotenv()

def check_bill_in_upvote(state_code: str, session_id: int, bill_number: str) -> dict:
    """
    Checks if a bill exists using the Upvote API endpoint.

    Endpoint:
        GET /legible/filters/state

    Query Parameters:
        state_code: The two-letter state code (e.g., 'IA')
        session_id: The legislative session ID
        query: The bill number

    Authentication:
        Uses the UPVOTE_API_KEY from the environment as a Bearer token in the Authorization header,
        and sends uid, access_token, and client as additional headers.
    
    Returns:
        dict: Parsed JSON response from the API.
    """
    upvote_api_url = os.getenv("UPVOTE_API_BASE_URL")
    if not upvote_api_url:
        raise EnvironmentError("UPVOTE_API_BASE_URL environment variable not set")
    
    upvote_api_key = os.getenv("UPVOTE_API_KEY")
    if not upvote_api_key:
        raise EnvironmentError("UPVOTE_API_KEY environment variable not set")
    
    uid = os.getenv("UID")
    access_token = os.getenv("ACCESS_TOKEN")
    client = os.getenv("CLIENT")
    if not uid or not access_token or not client:
        raise EnvironmentError("UID, ACCESS_TOKEN, and CLIENT environment variables must be set")
    
    endpoint = f"{upvote_api_url}/legible/filters/state"
    params = {
        "state_code": state_code,
        "session_id": session_id,
        "query": bill_number
    }
    
    headers = {
        "Authorization": f"Bearer {upvote_api_key}",
        "uid": uid,
        "access_token": access_token,
        "client": client
    }
    
    try:
        response = requests.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error while hitting Upvote API: {e}")
        return {}

def main():
    # Set parameters manually to test the Upvote API endpoint
    state_code = "IA"
    session_id = 153  # Example session id; update as needed.
    bill_number = "SF214"  # Example bill number; update as necessary.

    result = check_bill_in_upvote(state_code, session_id, bill_number)
    print("Upvote API response:")
    print(result)

if __name__ == "__main__":
    main() 