import os
import starkbank
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()


PRIVATE_KEY_CONTENT = os.environ.get("PRIVATE_KEY_CONTENT")
PROJECT_ID = os.environ.get("PROJECT_ID")


project = starkbank.Project(
    environment="sandbox", id=PROJECT_ID, private_key=PRIVATE_KEY_CONTENT
)

starkbank.user = project
