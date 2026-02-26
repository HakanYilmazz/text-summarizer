from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from huggingface_hub import InferenceClient

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development only
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hugging Face config
HF_API_KEY = os.getenv("HF_API_KEY")  # make sure your .env has HF_API_KEY
HF_MODEL = "facebook/bart-large-cnn"  # English summarization model

# Initialize HF InferenceClient
client = InferenceClient(api_key=HF_API_KEY)

# Request schema
class SummarizeRequest(BaseModel):
    text: str
    use_key: bool

@app.post("/summarize")
def summarize(req: SummarizeRequest):
    if not req.use_key:
        return {"summary": "API key disabled. Switch ON to generate."}

    try:
        result = client.summarization(req.text, model=HF_MODEL)

        # NEW FIX:
        summary_text = result.summary_text

        print("HF API response:", result)

    except Exception as e:
        summary_text = f"Error calling HF API: {e}"
        print(summary_text)

    return {"summary": summary_text}