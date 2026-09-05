from fastapi import HTTPException, Header, status
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get("API_KEY")


def verify_api_key(x_api_key: str = Header()):
    """Verify the API key provided in the request header."""
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )

    return x_api_key
