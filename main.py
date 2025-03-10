import streamlit as st
import fal_client
from dotenv import load_dotenv
import os 
import vertexai

import requests

from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    Image,
    Part,
    SafetySetting,
)

from google import genai

load_dotenv()

fal_client = None

PROJECT_ID = ""
LOCATION = ""
FAL_KEY =""

if os.getenv("ENVIRONMENT"):
    PROJECT_ID = os.getenv("VERTEX_PROJECT") 

    LOCATION = os.getenv("VERTEX_LOCATION")
    FAL_KEY = os.getenv("FAL_KEY")
else:
    PROJECT_ID = st.secrets["VERTEX_PROJECT"] 

    LOCATION = st.secrets["VERTEX_LOCATION"]
    FAL_KEY = st.secrets["FAL_KEY"]


vertexai.init(project=PROJECT_ID, location=LOCATION)
fal_client.init(api_key=FAL_KEY)
     

text_gen_model = GenerativeModel("gemini-2.0-flash")


st.title("Logo generator")



business_desc = st.text_input(
    "Describe your business shortly",
    placeholder="Example: A Marketing agency focussing on social media marketing",
)

style_of_logo = st.radio(
    "Select the style of logo you want",
    ["Vibrant, Creative", "Minimalistic, Professional", "Elegant, Sophisticated"],
    index=0,
)


def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(log["message"])


result = None


if st.button("Generate Logo", type="primary"):
    try:
        print(business_desc, style_of_logo, " the button is clicked")
        
        resulting_prompt = text_gen_model.generate_content(f"With given information such as a business of description {business_desc} and style preference of {style_of_logo}. Give me a prompt that i can use with a image generative model to get a great logo. Give me only the prompt without any explainations")
        st.markdown(resulting_prompt.text)

        result = fal_client.subscribe(
            "fal-ai/ideogram/v2",
            arguments={
                # "prompt": f"A Logo for a business that can be described as {business_desc} with a style of {style_of_logo}, the logo should not contain any text,t it can have symbols",
                "prompt": f"{resulting_prompt.text}",
                "aspect_ratio": "1:1",
                "style": "design",
                "seed": 42,
            },
            with_logs=True,
            on_queue_update=on_queue_update,
        )

        print(result)
        if result:
            img_url = result["images"][0]["url"]
            st.image(img_url, caption="Generated Logo")
            image_data = requests.get(img_url).content
            st.download_button(
                label="Download Logo",
                data=image_data,
                file_name="generated_logo.png",
                mime="image/png",
            )
    
    except Exception as e:
        st.markdown(f"Error: {e}")