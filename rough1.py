
from dotenv import load_dotenv
import os

import vertexai


from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    Image,
    Part,
    SafetySetting,
)

load_dotenv()

PROJECT_ID = os.getenv("VERTEX_PROJECT")  # @param {type: "string", placeholder: "[your-project-id]", isTemplate: true}
# if not PROJECT_ID or PROJECT_ID == "[your-project-id]":
#     PROJECT_ID = str(os.environ.get("GOOGLE_CLOUD_PROJECT"))

LOCATION = os.getenv("VERTEX_LOCATION")

vertexai.init(project=PROJECT_ID, location=LOCATION)
     
    
model = GenerativeModel("gemini-2.0-flash")


response = model.generate_content("Why is the sky blue?")

print(response.text)